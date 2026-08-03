"""Core data models for the self-healing agent.

All LLM-facing schemas and persistent data structures use Pydantic v2.
"""

from __future__ import annotations

import hashlib
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class Tier(str, Enum):
    """Task difficulty tiers."""

    T0 = "T0"  # trivial: string/list manipulation
    T1 = "T1"  # standard: algorithmic with edge cases
    T2 = "T2"  # stateful: class with invariants
    T3 = "T3"  # subtle: off-by-one, float precision, mutation aliasing
    T4 = "T4"  # integration: two modules that must agree
    T5 = "T5"  # unsolvable: contradictory requirements


class TaskSpec(BaseModel):
    """Specification for a single task in the graded suite."""

    id: str
    tier: Tier
    prompt: str
    entrypoint: str = "solution.py"
    timeout: int = 30  # seconds
    deps: list[str] = Field(default_factory=list)
    solvable: bool = True
    image: str = "shc-sandbox:latest"
    image_digest: str | None = None


class Frame(BaseModel):
    """A single frame in a parsed traceback."""

    file: str
    line: int
    function: str
    code: str | None = None
    is_project: bool = False  # True if this frame is in the user's code


class Failure(BaseModel):
    """Typed record of a classified failure from sandbox execution."""

    kind: Literal[
        "syntax",
        "import",
        "assertion",
        "exception",
        "timeout",
        "oom",
        "tamper",
        "no_output",
    ]
    exc_type: str | None = None
    message: str = ""
    file: str | None = None
    line: int | None = None
    frames: list[Frame] = Field(default_factory=list)
    failing_tests: list[str] = Field(default_factory=list)
    expected: str | None = None
    actual: str | None = None
    signature: str = ""

    def compute_signature(self) -> str:
        """Compute a stable hash for no-progress detection."""
        content = f"{self.kind}:{self.exc_type}:{self.message}:{self.file}:{self.line}"
        content += ":" + ",".join(self.failing_tests)
        self.signature = hashlib.sha256(content.encode()).hexdigest()[:16]
        return self.signature


class Verdict(str, Enum):
    """Final verdict for a task in a run."""

    PASSED_AT_1 = "passed@1"  # passed on first attempt, no repair needed
    RESOLVED = "resolved"  # failed initially, repaired successfully
    UNRESOLVED = "unresolved"  # failed, could not repair
    TAMPERED = "tampered"  # agent modified test files
    FALSE_SUCCESS = "false_success"  # T5 unsolvable claimed as solved
    ERROR = "error"  # infrastructure error


class Attempt(BaseModel):
    """Record of a single attempt at a task."""

    attempt_number: int
    model: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    cost_usd: float = 0.0
    wall_time_s: float = 0.0
    submitted_code: str = ""
    diff_from_previous: str = ""
    failure: Failure | None = None
    sandbox_exit_code: int | None = None
    passed_visible: bool = False
    passed_hidden: bool = False
    tampered: bool = False
    cheat_flags: list[str] = Field(default_factory=list)


class TaskResult(BaseModel):
    """Complete result for one task in a run."""

    task_id: str
    tier: Tier
    solvable: bool = True
    verdict: Verdict = Verdict.ERROR
    attempts: list[Attempt] = Field(default_factory=list)
    pass_at_1: bool = False
    pass_at_n: bool = False
    total_cost_usd: float = 0.0
    total_attempts: int = 0


class RunManifest(BaseModel):
    """Metadata for a complete run."""

    run_id: str
    models: list[str]
    tiers: list[str]
    seed: int
    max_attempts: int = 5
    temperature: float = 0.0
    timestamp: str = ""
    prompt_version: str = ""
    task_results: list[TaskResult] = Field(default_factory=list)
    aggregate_metrics: dict[str, float] = Field(default_factory=dict)
