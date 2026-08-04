"""High-level sandbox executor that orchestrates container lifecycle.

Provides the main interface for running code/tests in the sandbox with
guaranteed cleanup, reaping, and proper error handling.
"""

from __future__ import annotations

import logging

from shc.sandbox.config import SandboxConfig
from shc.sandbox.container import Sandbox, SandboxResult
from shc.sandbox.reaper import reap_by_run_id

logger = logging.getLogger(__name__)


def run_code_in_sandbox(
    *,
    run_id: str,
    task_id: str,
    attempt: int,
    code_files: dict[str, str | bytes],
    command: str = "python solution.py",
    config: SandboxConfig | None = None,
) -> SandboxResult:
    """Run code in an isolated sandbox container.

    This is the primary interface for executing untrusted code. It:
    1. Creates a container with all security limits
    2. Copies code in via put_archive (never bind-mount)
    3. Executes the command
    4. Captures output with byte limits
    5. Guarantees container removal via try/finally

    Args:
        run_id: unique identifier for this run
        task_id: task being executed
        attempt: attempt number (1-indexed)
        code_files: mapping of filename -> content to place in /work
        command: command to execute in /work
        config: sandbox configuration (uses defaults if None)

    Returns:
        SandboxResult with exit code, stdout, stderr, timing, and error flags
    """
    if config is None:
        config = SandboxConfig()

    sandbox = Sandbox(run_id=run_id, task_id=task_id, attempt=attempt)

    try:
        sandbox.prepare(work_files=code_files, config=config)
        result = sandbox.execute(command)
        return result
    finally:
        # GUARANTEED teardown - this is a safety property
        sandbox.cleanup()


def run_tests_in_sandbox(
    *,
    run_id: str,
    task_id: str,
    attempt: int,
    code_files: dict[str, str | bytes],
    test_files: dict[str, str | bytes],
    config: SandboxConfig | None = None,
    pytest_args: str = "-x -q",
    deps: list[str] | None = None,
) -> SandboxResult:
    """Run pytest against code in an isolated sandbox.

    Merges code_files and test_files, then runs pytest. The test files
    are placed alongside the code in /work.

    Args:
        run_id: unique identifier for this run
        task_id: task being executed
        attempt: attempt number
        code_files: the agent's submitted code
        test_files: test files to run against
        config: sandbox configuration
        pytest_args: additional pytest arguments
        deps: additional pip packages to install (pytest always included)

    Returns:
        SandboxResult from pytest execution
    """
    # Merge code and test files
    all_files = {**code_files, **test_files}

    # Add a minimal conftest if not present
    if "conftest.py" not in all_files:
        all_files["conftest.py"] = ""

    # Build install + test command
    # Our shc-sandbox image already has pytest. If extra deps needed, install them.
    # Note: network_mode=none means pip install won't work unless image is custom.
    if deps:
        # For tasks with extra deps, we'd need a custom image or pre-install
        install_cmd = f"pip install -q {' '.join(deps)} 2>/dev/null && "
    else:
        install_cmd = ""

    # Explicitly pass test file paths to pytest since they may not match
    # the default test_*.py / *_test.py discovery pattern
    test_file_names = " ".join(test_files.keys())
    test_cmd = f"python -m pytest {test_file_names} {pytest_args}"
    command = f"{install_cmd}{test_cmd}"

    return run_code_in_sandbox(
        run_id=run_id,
        task_id=task_id,
        attempt=attempt,
        code_files=all_files,
        command=command,
        config=config,
    )


def run_with_reap_guard(
    run_id: str,
    fn: callable,  # type: ignore[type-arg]
) -> None:
    """Run a function with reaper guards at start and end.

    Reaps any leftover containers from this run_id before and after execution.
    This is the outer safety net: even if the orchestrator crashes mid-run,
    the next startup will clean up.
    """
    logger.info("Reaping any leftover containers for run %s", run_id)
    reap_by_run_id(run_id)

    try:
        fn()
    finally:
        logger.info("Final reap for run %s", run_id)
        reap_by_run_id(run_id)
