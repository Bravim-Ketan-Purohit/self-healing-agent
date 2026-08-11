"""Versioned prompt templates for code generation and repair.

These templates are the core interface between the LLM and the task.
Version strings are recorded with each run for reproducibility.
"""

from __future__ import annotations

PROMPT_VERSION = "v1.0"

SYSTEM_GENERATE = """\
You are an expert Python programmer. Your task is to write a complete, correct \
implementation that passes all tests.

Rules:
- Write ONLY the implementation code. No tests, no explanations, no markdown.
- The code must be a complete Python file that can be imported.
- Follow the function/class signatures exactly as specified in the prompt.
- Handle edge cases carefully.
- Do not import anything that isn't in the Python standard library unless told otherwise.

Respond with ONLY the Python code, nothing else."""

SYSTEM_REPAIR = """\
You are an expert Python programmer debugging code. You will be shown:
1. The original task prompt
2. Your previous implementation
3. The test failures and traceback

Your task is to fix the implementation so ALL tests pass.

Rules:
- Write ONLY the complete fixed implementation. No tests, no explanations, no markdown.
- The code must be a complete Python file that can be imported.
- Fix the specific failures indicated by the traceback.
- Do not modify the function/class signatures.
- Do not import anything that isn't in the Python standard library unless told otherwise.
- Think carefully about what the traceback tells you.

Respond with ONLY the corrected Python code, nothing else."""


def build_generate_prompt(
    task_prompt: str,
    visible_tests: str,
    starter_code: str | None = None,
) -> str:
    """Build the user message for initial code generation.

    Args:
        task_prompt: the full task description from prompt.md
        visible_tests: the visible test file content (shown as feedback spec)
        starter_code: optional starter code skeleton

    Returns:
        formatted user prompt
    """
    parts = [
        "## Task\n",
        task_prompt.strip(),
        "\n\n## Tests (your code must pass these)\n",
        "```python\n" + visible_tests.strip() + "\n```\n",
    ]

    if starter_code and starter_code.strip():
        parts.append("\n## Starter Code\n")
        parts.append("```python\n" + starter_code.strip() + "\n```\n")

    parts.append(
        "\nWrite the complete implementation. "
        "Respond with ONLY Python code, no markdown fences."
    )

    return "".join(parts)


def build_repair_prompt(
    task_prompt: str,
    visible_tests: str,
    previous_code: str,
    failure_output: str,
    attempt_number: int,
    max_attempts: int,
) -> str:
    """Build the user message for a repair attempt.

    Args:
        task_prompt: the full task description
        visible_tests: the visible test file content
        previous_code: the code from the last attempt
        failure_output: pytest output showing failures
        attempt_number: current attempt (1-indexed)
        max_attempts: total allowed attempts

    Returns:
        formatted repair prompt
    """
    parts = [
        f"## Repair Attempt {attempt_number}/{max_attempts}\n\n",
        "## Task\n",
        task_prompt.strip(),
        "\n\n## Tests\n",
        "```python\n" + visible_tests.strip() + "\n```\n",
        "\n## Your Previous Implementation\n",
        "```python\n" + previous_code.strip() + "\n```\n",
        "\n## Test Failures\n",
        "```\n" + failure_output.strip()[-3000:] + "\n```\n",  # cap output
        "\nAnalyze the failures carefully, then write the COMPLETE corrected "
        "implementation. Respond with ONLY Python code, no markdown fences.",
    ]

    return "".join(parts)
