"""Task suite validator.

Verifies suite integrity before any run:
  1. Every task has required files.
  2. Reference solutions for solvable tasks PASS both visible and hidden tests.
  3. Unsolvable (T5) tasks have no reference that passes - they must be unsatisfiable.
  4. Visible and hidden tests are distinct (no leakage).
  5. Hidden tests actually test something beyond visible.

This runs in CI. A suite that fails validation blocks the run.
"""

from __future__ import annotations

import logging
import sys
from dataclasses import dataclass, field
from pathlib import Path

from shc.models import TaskSpec
from shc.sandbox.config import SandboxConfig
from shc.sandbox.executor import run_tests_in_sandbox
from shc.suite.loader import (
    REQUIRED_FILES,
    TASKS_ROOT,
    get_hidden_tests,
    get_reference_solution,
    get_visible_tests,
    load_suite,
    task_dir_for_spec,
)

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Result of validating the task suite."""

    total_tasks: int = 0
    passed: int = 0
    failed: int = 0
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return self.failed == 0 and len(self.errors) == 0


def _check_required_files(spec: TaskSpec, task_dir: Path, result: ValidationResult) -> bool:
    """Check that all required files exist for a task."""
    ok = True
    for required in REQUIRED_FILES:
        if not (task_dir / required).exists():
            result.errors.append(f"{spec.id}: missing {required}")
            ok = False
    return ok


def _check_test_distinctness(task_dir: Path, spec: TaskSpec, result: ValidationResult) -> None:
    """Warn if visible and hidden tests are identical (no held-out coverage)."""
    visible = get_visible_tests(task_dir).get("tests_visible.py", "")
    hidden = get_hidden_tests(task_dir).get("tests_hidden.py", "")

    if not hidden.strip():
        result.warnings.append(f"{spec.id}: tests_hidden.py is empty")
        return

    # Normalize whitespace for comparison
    vis_norm = "".join(visible.split())
    hid_norm = "".join(hidden.split())
    if vis_norm == hid_norm:
        result.warnings.append(
            f"{spec.id}: visible and hidden tests are identical - no held-out coverage"
        )


def _run_reference(
    spec: TaskSpec,
    task_dir: Path,
    run_id: str,
) -> tuple[bool, bool, str]:
    """Run the reference solution against visible and hidden tests.

    Returns:
        (visible_passed, hidden_passed, detail)
    """
    reference = get_reference_solution(task_dir)
    if reference is None:
        return (False, False, "no reference solution")

    config = SandboxConfig(
        image=spec.image,
        image_digest=spec.image_digest,
        timeout_s=spec.timeout,
    )

    # Run against visible tests
    visible_tests = get_visible_tests(task_dir)
    vis_result = run_tests_in_sandbox(
        run_id=run_id,
        task_id=f"{spec.id}-ref-vis",
        attempt=0,
        code_files=reference,  # type: ignore[arg-type]
        test_files=visible_tests,  # type: ignore[arg-type]
        config=config,
    )
    visible_passed = vis_result.exit_code == 0

    # Run against hidden tests
    hidden_tests = get_hidden_tests(task_dir)
    hid_result = run_tests_in_sandbox(
        run_id=run_id,
        task_id=f"{spec.id}-ref-hid",
        attempt=0,
        code_files=reference,  # type: ignore[arg-type]
        test_files=hidden_tests,  # type: ignore[arg-type]
        config=config,
    )
    hidden_passed = hid_result.exit_code == 0

    detail = ""
    if not visible_passed:
        detail += f"visible failed (exit {vis_result.exit_code}): {vis_result.stdout[-500:]}"
    if not hidden_passed:
        detail += f" hidden failed (exit {hid_result.exit_code}): {hid_result.stdout[-500:]}"

    return (visible_passed, hidden_passed, detail)


def validate_suite(
    root: Path | None = None,
    tiers: list[str] | None = None,
    skip_sandbox: bool = False,
) -> ValidationResult:
    """Validate the entire task suite.

    Args:
        root: override tasks root
        tiers: optional filter to specific tiers
        skip_sandbox: if True, only do static checks (no reference execution)

    Returns:
        ValidationResult with pass/fail counts and errors
    """
    if root is None:
        root = TASKS_ROOT

    result = ValidationResult()
    specs = load_suite(root=root, tiers=tiers)
    result.total_tasks = len(specs)

    run_id = "validate"

    for spec in specs:
        task_dir = task_dir_for_spec(spec, root=root)

        # Static checks
        if not _check_required_files(spec, task_dir, result):
            result.failed += 1
            continue

        _check_test_distinctness(task_dir, spec, result)

        if skip_sandbox:
            result.passed += 1
            continue

        # Dynamic checks: run reference solution
        visible_passed, hidden_passed, detail = _run_reference(spec, task_dir, run_id)

        if spec.solvable:
            # Solvable task: reference MUST pass both visible and hidden
            if visible_passed and hidden_passed:
                result.passed += 1
                logger.info("PASS %s (%s): reference passes all tests", spec.id, spec.tier.value)
            else:
                result.failed += 1
                result.errors.append(
                    f"{spec.id}: solvable but reference fails - {detail}"
                )
        else:
            # Unsolvable task (T5): reference should NOT pass (task is contradictory)
            # We expect NO reference, or a reference that cannot pass hidden tests
            if hidden_passed:
                result.failed += 1
                result.errors.append(
                    f"{spec.id}: marked unsolvable but hidden tests pass - not actually unsolvable"
                )
            else:
                result.passed += 1
                logger.info(
                    "PASS %s (%s): unsolvable, correctly fails", spec.id, spec.tier.value
                )

    return result


def print_validation_report(result: ValidationResult) -> None:
    """Print a human-readable validation report."""
    print("\n" + "=" * 60)
    print("TASK SUITE VALIDATION")
    print("=" * 60)
    print(f"Total tasks:  {result.total_tasks}")
    print(f"Passed:       {result.passed}")
    print(f"Failed:       {result.failed}")

    if result.warnings:
        print(f"\nWarnings ({len(result.warnings)}):")
        for w in result.warnings:
            print(f"  ! {w}")

    if result.errors:
        print(f"\nErrors ({len(result.errors)}):")
        for e in result.errors:
            print(f"  x {e}")

    print("\n" + ("VALIDATION PASSED" if result.ok else "VALIDATION FAILED"))
    print("=" * 60 + "\n")


def main() -> None:
    """CLI entry point for suite validation."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    import argparse

    parser = argparse.ArgumentParser(description="Validate the task suite")
    parser.add_argument("--tiers", help="Comma-separated tier filter")
    parser.add_argument("--skip-sandbox", action="store_true", help="Static checks only")
    args = parser.parse_args()

    tiers = args.tiers.split(",") if args.tiers else None
    result = validate_suite(tiers=tiers, skip_sandbox=args.skip_sandbox)
    print_validation_report(result)
    sys.exit(0 if result.ok else 1)


if __name__ == "__main__":
    main()
