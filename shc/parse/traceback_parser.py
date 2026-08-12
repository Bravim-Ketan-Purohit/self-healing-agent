"""Structured traceback and pytest output parser.

Parses raw pytest/Python output into typed Failure records that the
repair prompt can use to give the LLM targeted feedback.
"""

from __future__ import annotations

import re
from typing import Literal

from shc.models import Failure, Frame

# --- Regex patterns ---

# Matches: "File "/work/solution.py", line 42, in my_function"
FRAME_RE = re.compile(
    r'File "(?P<file>[^"]+)", line (?P<line>\d+), in (?P<function>\S+)'
)

# Matches pytest short test summary: "FAILED test_visible.py::test_foo - AssertionError: ..."
PYTEST_FAIL_RE = re.compile(
    r"FAILED\s+(?P<file>\S+)::(?P<test>\S+)\s*[-–]\s*(?P<exc>\w+):\s*(?P<msg>.*)"
)

# Matches: "E       AssertionError: assert 3 == 4"
ASSERTION_RE = re.compile(r"E\s+AssertionError:\s*(.*)")

# Matches: "E       assert X == Y"
ASSERT_EQ_RE = re.compile(r"E\s+assert\s+(.+?)\s*==\s*(.+)")

# Matches: "ModuleNotFoundError: No module named 'foo'"
IMPORT_ERROR_RE = re.compile(r"(ModuleNotFoundError|ImportError):\s*(.*)")

# Matches: "SyntaxError: ..."
SYNTAX_ERROR_RE = re.compile(r"SyntaxError:\s*(.*)")

# Matches pytest summary line: "X failed, Y passed in Z seconds"
SUMMARY_RE = re.compile(r"(\d+) failed")

# Matches timeout messages
TIMEOUT_RE = re.compile(r"(timed?\s*out|TimeoutError|TIMEOUT)", re.IGNORECASE)

# Matches OOM messages
OOM_RE = re.compile(r"(MemoryError|OOM|killed|Cannot allocate memory)", re.IGNORECASE)


def classify_failure_kind(
    output: str,
    exit_code: int,
    timed_out: bool = False,
    oom_killed: bool = False,
) -> Literal["syntax", "import", "assertion", "exception", "timeout", "oom", "no_output"]:
    """Classify the failure kind from output and metadata."""
    if timed_out or TIMEOUT_RE.search(output):
        return "timeout"
    if oom_killed or OOM_RE.search(output):
        return "oom"
    if not output.strip():
        return "no_output"
    if SYNTAX_ERROR_RE.search(output):
        return "syntax"
    if IMPORT_ERROR_RE.search(output):
        return "import"
    if "AssertionError" in output or "assert" in output.lower():
        return "assertion"
    return "exception"


def parse_frames(output: str) -> list[Frame]:
    """Extract stack frames from traceback output."""
    frames: list[Frame] = []
    lines = output.split("\n")

    for i, line in enumerate(lines):
        match = FRAME_RE.search(line)
        if match:
            code_line = None
            # Next line is usually the code
            if i + 1 < len(lines):
                candidate = lines[i + 1].strip()
                if candidate and not candidate.startswith("File "):
                    code_line = candidate

            frame = Frame(
                file=match.group("file"),
                line=int(match.group("line")),
                function=match.group("function"),
                code=code_line,
                is_project="/work/" in match.group("file"),
            )
            frames.append(frame)

    return frames


def parse_failing_tests(output: str) -> list[str]:
    """Extract the names of failing test functions."""
    tests: list[str] = []
    for match in PYTEST_FAIL_RE.finditer(output):
        tests.append(match.group("test"))

    # Also check for the = FAILURES = section
    failure_section = re.findall(r"_+ (\w+) _+", output)
    for name in failure_section:
        if name not in tests:
            tests.append(name)

    return tests


def parse_assertion_details(output: str) -> tuple[str | None, str | None]:
    """Extract expected and actual values from assertion failures."""
    # Look for "assert X == Y" patterns
    for match in ASSERT_EQ_RE.finditer(output):
        actual = match.group(1).strip()
        expected = match.group(2).strip()
        return expected, actual

    # Look for more general assertion messages
    for match in ASSERTION_RE.finditer(output):
        msg = match.group(1)
        if "==" in msg:
            parts = msg.split("==", 1)
            return parts[1].strip(), parts[0].strip().replace("assert ", "")
        return None, msg

    return None, None


def parse_exception_type(output: str) -> str | None:
    """Extract the primary exception type from the output."""
    # Look for the last exception in the traceback
    exc_re = re.compile(r"^(\w+(?:Error|Exception|Warning)):", re.MULTILINE)
    matches = list(exc_re.finditer(output))
    if matches:
        return matches[-1].group(1)
    return None


def parse_failure(
    output: str,
    exit_code: int = 1,
    timed_out: bool = False,
    oom_killed: bool = False,
) -> Failure:
    """Parse raw pytest/execution output into a structured Failure record.

    This is the main entry point for the parser. It classifies the failure,
    extracts frames, failing tests, assertion details, and computes a
    signature for no-progress detection.

    Args:
        output: combined stdout+stderr from the sandbox
        exit_code: process exit code
        timed_out: whether the execution timed out
        oom_killed: whether the process was OOM-killed

    Returns:
        Failure record with all extracted information
    """
    kind = classify_failure_kind(output, exit_code, timed_out, oom_killed)
    frames = parse_frames(output)
    failing_tests = parse_failing_tests(output)
    expected, actual = parse_assertion_details(output)
    exc_type = parse_exception_type(output)

    # Extract file and line from the most relevant frame (user code)
    project_frames = [f for f in frames if f.is_project]
    file = project_frames[-1].file if project_frames else None
    line = project_frames[-1].line if project_frames else None

    # Build message
    if kind == "timeout":
        message = "Execution timed out"
    elif kind == "oom":
        message = "Out of memory"
    elif kind == "no_output":
        message = "No output produced"
    elif kind == "syntax":
        match = SYNTAX_ERROR_RE.search(output)
        message = match.group(1) if match else "Syntax error"
    elif kind == "import":
        match = IMPORT_ERROR_RE.search(output)
        message = match.group(2) if match else "Import error"
    elif exc_type:
        # Get the message after the exception type
        exc_msg_re = re.compile(rf"{exc_type}:\s*(.*)", re.MULTILINE)
        exc_match = exc_msg_re.search(output)
        message = exc_match.group(1) if exc_match else ""
    else:
        message = ""

    failure = Failure(
        kind=kind,
        exc_type=exc_type,
        message=message[:500],  # cap message length
        file=file,
        line=line,
        frames=frames,
        failing_tests=failing_tests,
        expected=expected,
        actual=actual,
    )
    failure.compute_signature()
    return failure
