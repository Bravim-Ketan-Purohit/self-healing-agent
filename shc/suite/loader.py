"""Task suite loader.

Loads tasks from the tasks/ directory hierarchy. Each task is a directory
containing task.yaml, prompt.md, starter/ code, tests_visible.py, tests_hidden.py,
and optionally reference/ with a known-good solution.
"""

from __future__ import annotations

import logging
from pathlib import Path

import yaml

from shc.models import TaskSpec, Tier

logger = logging.getLogger(__name__)

TASKS_ROOT = Path(__file__).resolve().parent.parent.parent / "tasks"

REQUIRED_FILES = ["task.yaml", "prompt.md", "tests_visible.py", "tests_hidden.py"]


def load_task(task_dir: Path) -> TaskSpec:
    """Load a single task from its directory.

    Args:
        task_dir: path to a task directory (e.g. tasks/T1/reverse_words)

    Returns:
        TaskSpec model

    Raises:
        FileNotFoundError: if required files are missing
        ValueError: if task.yaml is malformed
    """
    yaml_path = task_dir / "task.yaml"
    if not yaml_path.exists():
        msg = f"Missing task.yaml in {task_dir}"
        raise FileNotFoundError(msg)

    with open(yaml_path) as f:
        raw = yaml.safe_load(f)

    if not isinstance(raw, dict):
        msg = f"task.yaml in {task_dir} must be a mapping"
        raise ValueError(msg)

    # Inject the task ID from directory name if not specified
    if "id" not in raw:
        raw["id"] = task_dir.name

    # Inject tier from parent directory if not specified
    if "tier" not in raw:
        parent_name = task_dir.parent.name
        if parent_name in [t.value for t in Tier]:
            raw["tier"] = parent_name

    # Load prompt from prompt.md
    prompt_path = task_dir / "prompt.md"
    if prompt_path.exists():
        raw["prompt"] = prompt_path.read_text(encoding="utf-8")
    elif "prompt" not in raw:
        msg = f"No prompt.md or prompt field in {task_dir}"
        raise FileNotFoundError(msg)

    return TaskSpec(**raw)


def load_suite(
    root: Path | None = None,
    tiers: list[str] | None = None,
) -> list[TaskSpec]:
    """Load all tasks from the task suite.

    Args:
        root: override for the tasks root directory
        tiers: optional filter to specific tiers (e.g. ["T0", "T1"])

    Returns:
        list of TaskSpec models, sorted by tier then id
    """
    if root is None:
        root = TASKS_ROOT

    tasks: list[TaskSpec] = []
    tier_dirs = sorted(root.iterdir())

    for tier_dir in tier_dirs:
        if not tier_dir.is_dir():
            continue
        if tier_dir.name not in [t.value for t in Tier]:
            continue
        if tiers and tier_dir.name not in tiers:
            continue

        for task_dir in sorted(tier_dir.iterdir()):
            if not task_dir.is_dir():
                continue
            if task_dir.name.startswith(".") or task_dir.name.startswith("_"):
                continue

            try:
                spec = load_task(task_dir)
                tasks.append(spec)
            except (FileNotFoundError, ValueError) as e:
                logger.warning("Skipping %s: %s", task_dir, e)

    logger.info("Loaded %d tasks from %s", len(tasks), root)
    return tasks


def get_task_files(task_dir: Path) -> dict[str, str]:
    """Get the starter files for a task (everything in starter/ or just the prompt).

    Returns:
        mapping of filename -> content for the initial code files
    """
    starter_dir = task_dir / "starter"
    files: dict[str, str] = {}

    if starter_dir.exists():
        for f in starter_dir.rglob("*"):
            if f.is_file():
                rel = str(f.relative_to(starter_dir))
                files[rel] = f.read_text(encoding="utf-8")

    return files


def get_visible_tests(task_dir: Path) -> dict[str, str]:
    """Get visible test files for a task."""
    tests_path = task_dir / "tests_visible.py"
    if tests_path.exists():
        return {"tests_visible.py": tests_path.read_text(encoding="utf-8")}
    return {}


def get_hidden_tests(task_dir: Path) -> dict[str, str]:
    """Get hidden test files for a task. Never shown to the agent."""
    tests_path = task_dir / "tests_hidden.py"
    if tests_path.exists():
        return {"tests_hidden.py": tests_path.read_text(encoding="utf-8")}
    return {}


def get_reference_solution(task_dir: Path) -> dict[str, str] | None:
    """Get the reference solution for a task (used for validation only)."""
    ref_dir = task_dir / "reference"
    if not ref_dir.exists():
        return None
    files: dict[str, str] = {}
    for f in ref_dir.rglob("*"):
        if f.is_file() and "__pycache__" not in str(f) and not f.suffix == ".pyc":
            rel = str(f.relative_to(ref_dir))
            try:
                files[rel] = f.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue  # skip binary files
    return files if files else None


def task_dir_for_spec(spec: TaskSpec, root: Path | None = None) -> Path:
    """Get the directory path for a task spec."""
    if root is None:
        root = TASKS_ROOT
    return root / spec.tier.value / spec.id
