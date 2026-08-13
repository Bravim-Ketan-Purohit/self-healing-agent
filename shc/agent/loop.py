"""Repair loop: generate → run → parse → repair → generate.

Implements the core self-healing cycle with no-progress detection.
The loop stops when:
  - Tests pass (success)
  - Max attempts reached
  - No progress detected (same failure signature repeated)
  - Tampering detected
"""

from __future__ import annotations

import logging
import time
from pathlib import Path

from shc.grade.grader import compute_verdict, grade_hidden, grade_visible
from shc.llm.client import LLMClient, Message
from shc.models import Attempt, Failure, TaskResult, TaskSpec
from shc.parse.traceback_parser import parse_failure
from shc.prompts.templates import (
    SYSTEM_GENERATE,
    SYSTEM_REPAIR,
    build_generate_prompt,
    build_repair_prompt,
)
from shc.suite.loader import TASKS_ROOT, get_visible_tests, task_dir_for_spec

logger = logging.getLogger(__name__)

# No-progress: if same signature seen this many times, stop
MAX_SAME_SIGNATURE = 2


def _extract_code(response: str) -> str:
    """Extract Python code from LLM response, stripping markdown fences if present."""
    content = response.strip()

    # Remove markdown code fences if present
    if content.startswith("```python"):
        content = content[len("```python") :].strip()
    elif content.startswith("```"):
        content = content[3:].strip()

    if content.endswith("```"):
        content = content[:-3].strip()

    return content


def run_task(
    *,
    task: TaskSpec,
    run_id: str,
    model: str,
    client: LLMClient,
    max_attempts: int = 5,
    temperature: float = 0.0,
    seed: int | None = None,
    root: Path | None = None,
) -> TaskResult:
    """Execute the full generate-test-repair loop for a single task.

    Args:
        task: the task specification
        run_id: unique run identifier
        model: OpenRouter model to use
        client: LLM client instance
        max_attempts: maximum repair attempts
        temperature: sampling temperature
        seed: optional reproducibility seed
        root: override for tasks root directory

    Returns:
        TaskResult with all attempts and final verdict
    """
    if root is None:
        root = TASKS_ROOT

    task_dir = task_dir_for_spec(task, root=root)
    visible_tests = get_visible_tests(task_dir)
    visible_content = visible_tests.get("tests_visible.py", "")

    result = TaskResult(
        task_id=task.id,
        tier=task.tier,
        solvable=task.solvable,
    )

    # Track failure signatures for no-progress detection
    seen_signatures: list[str] = []
    current_code = ""

    for attempt_num in range(1, max_attempts + 1):
        start_time = time.monotonic()

        # --- Generate or Repair ---
        if attempt_num == 1:
            # Initial generation
            user_msg = build_generate_prompt(
                task_prompt=task.prompt,
                visible_tests=visible_content,
            )
            system_msg = SYSTEM_GENERATE
        else:
            # Repair: use the failure output from the previous attempt
            prev_attempt = result.attempts[-1]
            failure_output = ""
            if prev_attempt.failure:
                failure_output = _format_failure_for_prompt(prev_attempt.failure)

            user_msg = build_repair_prompt(
                task_prompt=task.prompt,
                visible_tests=visible_content,
                previous_code=current_code,
                failure_output=failure_output,
                attempt_number=attempt_num,
                max_attempts=max_attempts,
            )
            system_msg = SYSTEM_REPAIR

        # Call LLM
        llm_response = client.generate(
            model=model,
            messages=[
                Message(role="system", content=system_msg),
                Message(role="user", content=user_msg),
            ],
            temperature=temperature,
            max_tokens=4096,
            seed=seed,
        )

        current_code = _extract_code(llm_response.content)

        # --- Run visible tests ---
        vis_passed, vis_output = grade_visible(
            run_id=run_id,
            task=task,
            code=current_code,
            attempt=attempt_num,
            root=root,
        )

        # --- Parse failure if tests didn't pass ---
        failure: Failure | None = None
        if not vis_passed:
            failure = parse_failure(vis_output, exit_code=1)

        # --- Run hidden tests (for scoring, never shown to agent) ---
        hid_passed, _ = grade_hidden(
            run_id=run_id,
            task=task,
            code=current_code,
            attempt=attempt_num,
            root=root,
        )

        wall_time = time.monotonic() - start_time

        # Record attempt
        attempt = Attempt(
            attempt_number=attempt_num,
            model=model,
            prompt_tokens=llm_response.prompt_tokens,
            completion_tokens=llm_response.completion_tokens,
            cost_usd=llm_response.cost_usd,
            wall_time_s=wall_time,
            submitted_code=current_code,
            failure=failure,
            passed_visible=vis_passed,
            passed_hidden=hid_passed,
        )
        result.attempts.append(attempt)
        result.total_cost_usd += llm_response.cost_usd
        result.total_attempts = attempt_num

        logger.info(
            "%s attempt %d/%d: vis=%s hid=%s (%.1fs, $%.4f)",
            task.id,
            attempt_num,
            max_attempts,
            "PASS" if vis_passed else "FAIL",
            "PASS" if hid_passed else "FAIL",
            wall_time,
            llm_response.cost_usd,
        )

        # --- Stop conditions ---

        # Success: both visible and hidden pass
        if vis_passed and hid_passed:
            break

        # Visible passes but hidden fails: keep going (might be overfitting)
        # Hidden passes but visible fails: shouldn't happen, but continue

        # No-progress detection
        if failure:
            sig = failure.signature
            seen_signatures.append(sig)
            same_count = seen_signatures.count(sig)
            if same_count >= MAX_SAME_SIGNATURE:
                logger.info(
                    "%s: no progress detected (signature %s seen %d times), stopping",
                    task.id,
                    sig[:8],
                    same_count,
                )
                break

    # --- Compute verdict ---
    result.pass_at_1 = result.attempts[0].passed_hidden if result.attempts else False
    result.pass_at_n = any(a.passed_hidden for a in result.attempts)
    result.verdict = compute_verdict(result, task)

    return result


def _format_failure_for_prompt(failure: Failure) -> str:
    """Format a Failure record into text suitable for the repair prompt."""
    parts = [f"Error type: {failure.kind}"]

    if failure.exc_type:
        parts.append(f"Exception: {failure.exc_type}: {failure.message}")

    if failure.file and failure.line:
        parts.append(f"Location: {failure.file}:{failure.line}")

    if failure.failing_tests:
        parts.append(f"Failing tests: {', '.join(failure.failing_tests)}")

    if failure.expected and failure.actual:
        parts.append(f"Expected: {failure.expected}")
        parts.append(f"Actual: {failure.actual}")

    if failure.frames:
        parts.append("\nTraceback (most recent call last):")
        for frame in failure.frames[-5:]:  # Last 5 frames
            parts.append(f'  File "{frame.file}", line {frame.line}, in {frame.function}')
            if frame.code:
                parts.append(f"    {frame.code}")

    return "\n".join(parts)
