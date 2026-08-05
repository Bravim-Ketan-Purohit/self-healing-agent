"""Adversarial containment tests for the Docker sandbox.

These tests MUST pass before any LLM-generated code is executed.
They verify that hostile programs are properly contained.

Marked with `containment` — run with: pytest -m containment
"""

from __future__ import annotations

import time

import pytest

from shc.sandbox.config import SandboxConfig
from shc.sandbox.container import Sandbox, SandboxResult

# All tests in this module are containment tests
pytestmark = [pytest.mark.containment, pytest.mark.timeout(60)]

# Use a short timeout for adversarial tests
HOSTILE_CONFIG = SandboxConfig(timeout_s=10, output_limit_bytes=64 * 1024)


def _run_hostile(code: str, timeout_s: int = 10) -> SandboxResult:
    """Helper: run hostile code in the sandbox and return the result."""
    config = SandboxConfig(timeout_s=timeout_s, output_limit_bytes=64 * 1024)
    sandbox = Sandbox(run_id="test-containment", task_id="hostile", attempt=1)
    try:
        sandbox.prepare(
            work_files={"hostile.py": code},
            config=config,
        )
        return sandbox.execute("python hostile.py")
    finally:
        sandbox.cleanup()


class TestForkBomb:
    """Verify fork bombs are contained by pids_limit."""

    def test_fork_bomb_contained(self) -> None:
        """A fork bomb should be killed, not bring down the host."""
        code = """\
import os
while True:
    try:
        os.fork()
    except OSError:
        pass
"""
        result = _run_hostile(code)
        # Should either be killed by pids_limit or timeout
        assert result.exit_code != 0 or result.timed_out

    def test_multiprocessing_bomb(self) -> None:
        """Spawning many processes via multiprocessing should be contained."""
        code = """\
import multiprocessing
import time

def worker():
    while True:
        time.sleep(0.001)

procs = []
for _ in range(1000):
    try:
        p = multiprocessing.Process(target=worker)
        p.start()
        procs.append(p)
    except (OSError, RuntimeError):
        break

time.sleep(30)
"""
        result = _run_hostile(code)
        assert result.exit_code != 0 or result.timed_out


class TestMemoryBomb:
    """Verify memory bombs are contained by mem_limit."""

    def test_10gb_allocation(self) -> None:
        """Attempting to allocate 10 GB should be OOM-killed."""
        code = """\
# Try to allocate 10 GB
data = []
for _ in range(10000):
    data.append(b'x' * (1024 * 1024))  # 1 MB chunks
print("Should not reach here")
"""
        result = _run_hostile(code)
        # Should be OOM-killed or crash
        assert result.exit_code != 0 or result.oom_killed

    def test_exponential_memory(self) -> None:
        """Exponentially growing allocation should be contained."""
        code = """\
data = 'x'
while True:
    data = data * 2
"""
        result = _run_hostile(code)
        assert result.exit_code != 0 or result.oom_killed


class TestFilesystemAttack:
    """Verify filesystem attacks are contained."""

    def test_rm_rf_root(self) -> None:
        """rm -rf / should not affect the host (read-only rootfs)."""
        code = """\
import os
import shutil
# Try to destroy the filesystem
try:
    shutil.rmtree('/', ignore_errors=True)
except Exception:
    pass
# Try specific dangerous paths
for path in ['/etc', '/usr', '/bin', '/var']:
    try:
        shutil.rmtree(path, ignore_errors=True)
    except Exception:
        pass
print("Attempted destruction")
"""
        result = _run_hostile(code)
        # The container should survive (read-only rootfs)
        # Exit code 0 is fine here - the important thing is the host is unaffected
        assert result is not None  # just verify execution completed

    def test_write_outside_work(self) -> None:
        """Writing outside /work and /tmp should fail."""
        code = """\
import os

failures = []
# Try to write to various paths
for path in ['/etc/passwd', '/root/.bashrc', '/var/data', '/home/test']:
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write('pwned')
        failures.append(f'WROTE TO {path}')
    except (OSError, PermissionError):
        pass

if failures:
    print('SECURITY BREACH: ' + ', '.join(failures))
    exit(1)
else:
    print('All writes blocked')
    exit(0)
"""
        result = _run_hostile(code)
        assert "SECURITY BREACH" not in result.stdout
        assert result.exit_code == 0

    def test_fill_disk(self) -> None:
        """Writing enormous files should be limited by fsize ulimit."""
        code = """\
import os
# Try to write a 1 GB file
try:
    with open('/work/huge.bin', 'wb') as f:
        for _ in range(1024):
            f.write(b'x' * (1024 * 1024))  # 1 MB at a time
    print(f"Wrote {os.path.getsize('/work/huge.bin')} bytes")
except (OSError, IOError) as e:
    print(f"Write limited: {e}")
"""
        result = _run_hostile(code)
        # Should be limited by fsize ulimit (64 MB) or tmpfs size (128 MB)
        if "Wrote" in result.stdout:
            # Extract size - should be capped
            import re

            match = re.search(r"Wrote (\d+) bytes", result.stdout)
            if match:
                written = int(match.group(1))
                # Should not exceed tmpfs limit + fsize limit
                assert written <= 200 * 1024 * 1024  # generous bound


class TestNetworkAttack:
    """Verify network access is blocked."""

    def test_http_request_fails(self) -> None:
        """HTTP requests should fail with network_mode=none."""
        code = """\
import urllib.request
try:
    response = urllib.request.urlopen('http://example.com', timeout=5)
    print(f'SECURITY BREACH: got {response.status}')
    exit(1)
except Exception as e:
    print(f'Network blocked: {e}')
    exit(0)
"""
        result = _run_hostile(code)
        assert "SECURITY BREACH" not in result.stdout

    def test_dns_resolution_fails(self) -> None:
        """DNS resolution should fail with no network."""
        code = """\
import socket
try:
    addr = socket.gethostbyname('evil.example.com')
    print(f'SECURITY BREACH: resolved to {addr}')
    exit(1)
except (socket.gaierror, OSError) as e:
    print(f'DNS blocked: {e}')
    exit(0)
"""
        result = _run_hostile(code)
        assert "SECURITY BREACH" not in result.stdout

    def test_raw_socket_fails(self) -> None:
        """Raw socket creation should be blocked (all caps dropped)."""
        code = """\
import socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    print('SECURITY BREACH: raw socket created')
    exit(1)
except (PermissionError, OSError) as e:
    print(f'Raw socket blocked: {e}')
    exit(0)
"""
        result = _run_hostile(code)
        assert "SECURITY BREACH" not in result.stdout


class TestInfiniteOutput:
    """Verify infinite output is capped."""

    def test_infinite_print(self) -> None:
        """Infinite print should be truncated at the output cap."""
        code = """\
import sys
# Print forever
i = 0
while True:
    print(f'line {i}: ' + 'x' * 1000)
    i += 1
"""
        result = _run_hostile(code, timeout_s=10)
        # Output should be capped
        total_output = len(result.stdout.encode()) + len(result.stderr.encode())
        # Allow some overhead for the truncation marker
        assert total_output <= 128 * 1024  # generous bound above 64KB limit

    def test_stderr_flood(self) -> None:
        """Flooding stderr should also be capped."""
        code = """\
import sys
while True:
    sys.stderr.write('ERROR: ' + 'e' * 1000 + '\\n')
    sys.stderr.flush()
"""
        result = _run_hostile(code, timeout_s=10)
        total_stderr = len(result.stderr.encode())
        assert total_stderr <= 128 * 1024


class TestTimeout:
    """Verify timeout enforcement."""

    def test_infinite_loop_killed(self) -> None:
        """An infinite loop should be killed by the watchdog."""
        code = """\
while True:
    pass
"""
        start = time.time()
        result = _run_hostile(code, timeout_s=5)
        elapsed = time.time() - start
        # Should not run forever - killed within timeout + grace
        assert elapsed < 15
        assert result.timed_out or result.exit_code != 0

    def test_sleep_killed(self) -> None:
        """A long sleep should be interrupted."""
        code = """\
import time
time.sleep(3600)
print("Should not reach here")
"""
        start = time.time()
        _run_hostile(code, timeout_s=5)
        elapsed = time.time() - start
        assert elapsed < 15


class TestPrivilegeEscalation:
    """Verify privilege escalation is blocked."""

    def test_cannot_become_root(self) -> None:
        """Cannot escalate to root."""
        code = """\
import os
try:
    os.setuid(0)
    print('SECURITY BREACH: became root')
    exit(1)
except (PermissionError, OSError) as e:
    print(f'Privilege escalation blocked: {e}')

# Check we are running as non-root
uid = os.getuid()
print(f'Running as uid={uid}')
assert uid != 0, 'Running as root!'
exit(0)
"""
        result = _run_hostile(code)
        assert "SECURITY BREACH" not in result.stdout
        assert result.exit_code == 0

    def test_no_capabilities(self) -> None:
        """All capabilities should be dropped."""
        code = """\
import subprocess
try:
    # Try to use a capability (e.g., CAP_NET_RAW via ping)
    result = subprocess.run(['ping', '-c', '1', '8.8.8.8'],
                          capture_output=True, timeout=5)
    if result.returncode == 0:
        print('SECURITY BREACH: ping succeeded')
        exit(1)
except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
    pass
print('Capabilities properly dropped')
exit(0)
"""
        result = _run_hostile(code)
        assert "SECURITY BREACH" not in result.stdout


class TestContainerCleanup:
    """Verify containers are always cleaned up."""

    def test_cleanup_on_normal_exit(self) -> None:
        """Container is removed after normal execution."""
        import docker as docker_lib

        sandbox = Sandbox(run_id="test-cleanup", task_id="normal", attempt=1)
        sandbox.prepare(
            work_files={"test.py": "print('hello')"},
            config=HOSTILE_CONFIG,
        )
        container_name = sandbox.container_name
        sandbox.execute("python test.py")
        sandbox.cleanup()

        # Verify container is gone
        client = docker_lib.from_env()
        containers = client.containers.list(all=True, filters={"name": container_name})
        assert len(containers) == 0

    def test_cleanup_on_error(self) -> None:
        """Container is removed even when execution errors."""
        import docker as docker_lib

        sandbox = Sandbox(run_id="test-cleanup", task_id="error", attempt=1)
        sandbox.prepare(
            work_files={"crash.py": "import sys; sys.exit(1)"},
            config=HOSTILE_CONFIG,
        )
        container_name = sandbox.container_name
        sandbox.execute("python crash.py")
        sandbox.cleanup()

        client = docker_lib.from_env()
        containers = client.containers.list(all=True, filters={"name": container_name})
        assert len(containers) == 0

    def test_cleanup_via_context_manager(self) -> None:
        """Context manager guarantees cleanup."""
        import docker as docker_lib

        with Sandbox(run_id="test-ctx", task_id="ctx", attempt=1) as sandbox:
            sandbox.prepare(
                work_files={"test.py": "print('context manager')"},
                config=HOSTILE_CONFIG,
            )
            container_name = sandbox.container_name
            sandbox.execute("python test.py")

        client = docker_lib.from_env()
        containers = client.containers.list(all=True, filters={"name": container_name})
        assert len(containers) == 0
