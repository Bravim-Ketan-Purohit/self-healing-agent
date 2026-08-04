"""Docker container lifecycle management.

This is the security boundary of the project. Every generated program is treated as hostile.
Code is copied in via put_archive (never bind-mounted). Containers are always torn down.
"""

from __future__ import annotations

import io
import logging
import tarfile
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import docker
import docker.types
from docker.models.containers import Container

from shc.sandbox.config import (
    CONTAINER_PREFIX,
    FSIZE_LIMIT_BYTES,
    LABEL_MANAGED,
    LABEL_RUN_ID,
    LABEL_TASK,
    NOFILE_LIMIT,
    SandboxConfig,
)

logger = logging.getLogger(__name__)

# Truncation marker appended when output exceeds the cap
TRUNCATION_MARKER = "\n\n[OUTPUT TRUNCATED - exceeded byte limit]\n"


@dataclass
class SandboxResult:
    """Result of running code in the sandbox."""

    exit_code: int
    stdout: str
    stderr: str
    timed_out: bool = False
    oom_killed: bool = False
    wall_time_s: float = 0.0


@dataclass
class Sandbox:
    """Manages a single sandboxed container execution.

    Usage:
        sandbox = Sandbox(run_id="abc123", task_id="float_accumulate", attempt=1)
        sandbox.prepare(work_dir=Path("path/to/files"), config=SandboxConfig())
        result = sandbox.execute("python solution.py")
        sandbox.cleanup()  # always called, even on exception

    The recommended pattern is via the context manager or try/finally.
    """

    run_id: str
    task_id: str
    attempt: int
    config: SandboxConfig = field(default_factory=SandboxConfig)
    _container: Container | None = field(default=None, init=False, repr=False)
    _client: Any = field(default=None, init=False, repr=False)
    _watchdog: threading.Timer | None = field(default=None, init=False, repr=False)

    @property
    def container_name(self) -> str:
        """Generate namespaced container name: shc-{run_id[:8]}-{task_id}-{attempt}."""
        return f"{CONTAINER_PREFIX}-{self.run_id[:8]}-{self.task_id}-{self.attempt}"

    @property
    def labels(self) -> dict[str, str]:
        """Container labels for identification and reaper."""
        return {
            LABEL_RUN_ID: self.run_id,
            LABEL_TASK: self.task_id,
            LABEL_MANAGED: "true",
        }

    def _get_client(self) -> Any:
        """Get or create Docker client."""
        if self._client is None:
            self._client = docker.from_env()
        return self._client

    def prepare(
        self, work_files: dict[str, str | bytes], config: SandboxConfig | None = None
    ) -> None:
        """Create the container with all security limits.

        Args:
            work_files: mapping of filename -> content to place in /work
            config: optional override for sandbox configuration
        """
        if config is not None:
            object.__setattr__(self, "config", config)

        client = self._get_client()
        cfg = self.config

        # Resolve image reference
        image_ref = cfg.image
        if cfg.image_digest:
            image_ref = f"{cfg.image}@{cfg.image_digest}"

        # Build ulimits
        ulimits = [
            docker.types.Ulimit(name="fsize", soft=FSIZE_LIMIT_BYTES, hard=FSIZE_LIMIT_BYTES),
            docker.types.Ulimit(name="nofile", soft=NOFILE_LIMIT, hard=NOFILE_LIMIT),
        ]

        # Create container - does NOT start it yet
        # Security model: no bind-mounts (NEVER), network_mode=none,
        # all caps dropped, non-root user, resource limits, no-new-privileges.
        # We don't use read_only=True because Docker's put_archive API rejects
        # writes to any path (including tmpfs) when rootfs is marked read-only.
        # Instead we rely on: ephemeral container (always force-removed),
        # non-root user, caps=NONE, no network, resource limits, and tmpfs
        # for writable paths. The container overlay is write-only to the
        # container itself with no host exposure.
        self._container = client.containers.create(
            image=image_ref,
            command="sleep infinity",  # keep alive for exec
            stdin_open=True,
            network_mode=cfg.network_mode,
            mem_limit=cfg.memory_limit,
            memswap_limit=cfg.memory_swap,
            nano_cpus=cfg.nano_cpus,
            pids_limit=cfg.pids_limit,
            user=cfg.user,
            read_only=False,
            tmpfs={"/tmp": "size=64m,mode=1777"},
            working_dir="/work",
            cap_drop=["ALL"],
            security_opt=["no-new-privileges:true"],
            ulimits=ulimits,
            labels=self.labels,
            name=self.container_name,
            environment=self._build_env(),
        )

        # Start the container
        self._container.start()

        # Create /work directory owned by sandbox user (needed if using python:3.12-slim)
        # For shc-sandbox:latest image, /work already exists but this is idempotent
        self._container.exec_run(
            cmd=["/bin/sh", "-c", "mkdir -p /work && chown 10001:10001 /work"],
            user="root",
        )

        # Copy work files into /work via put_archive (NEVER bind-mount)
        self._copy_files_to_container(work_files)

    def _build_env(self) -> dict[str, str]:
        """Build the environment for the container. No secrets ever."""
        env: dict[str, str] = {
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONUNBUFFERED": "1",
        }
        # Only pass explicitly allowlisted vars
        if self.config.env_allowlist:
            import os

            for key in self.config.env_allowlist:
                val = os.environ.get(key)
                if val is not None:
                    env[key] = val
        return env

    def _copy_files_to_container(self, files: dict[str, str | bytes]) -> None:
        """Copy files into the container's /work directory using put_archive.

        This is the critical security boundary: we NEVER bind-mount host paths.
        """
        if not self._container:
            msg = "Container not created"
            raise RuntimeError(msg)

        tar_buffer = io.BytesIO()
        with tarfile.open(fileobj=tar_buffer, mode="w") as tar:
            for filename, content in files.items():
                if isinstance(content, str):
                    data = content.encode("utf-8")
                else:
                    data = content

                info = tarfile.TarInfo(name=filename)
                info.size = len(data)
                info.mode = 0o644
                info.uid = 10001
                info.gid = 10001
                tar.addfile(info, io.BytesIO(data))

        tar_buffer.seek(0)
        self._container.put_archive("/work", tar_buffer)

    def execute(self, command: str) -> SandboxResult:
        """Execute a command inside the sandbox with timeout and output caps.

        Args:
            command: shell command to run (e.g. "python solution.py" or "pytest")

        Returns:
            SandboxResult with captured output and metadata
        """
        if not self._container:
            msg = "Container not prepared"
            raise RuntimeError(msg)

        start_time = time.monotonic()
        timed_out = False

        # Start watchdog timer for hard kill
        self._watchdog = threading.Timer(
            self.config.timeout_s + 2,  # 2s grace after soft timeout
            self._force_kill,
        )
        self._watchdog.daemon = True
        self._watchdog.start()

        try:
            # Execute command via exec_run
            exec_result = self._container.exec_run(
                cmd=["/bin/sh", "-c", f"cd /work && {command}"],
                stdout=True,
                stderr=True,
                demux=True,
                user=self.config.user,
            )

            wall_time = time.monotonic() - start_time

            # Parse output
            stdout_raw, stderr_raw = exec_result.output or (None, None)
            stdout = self._cap_output(stdout_raw)
            stderr = self._cap_output(stderr_raw)
            exit_code = exec_result.exit_code

            # Check if container was OOM-killed
            oom_killed = self._check_oom()

            # Check timeout (exit code 137 = SIGKILL, often from timeout or OOM)
            if wall_time >= self.config.timeout_s:
                timed_out = True

            return SandboxResult(
                exit_code=exit_code if exit_code is not None else -1,
                stdout=stdout,
                stderr=stderr,
                timed_out=timed_out,
                oom_killed=oom_killed,
                wall_time_s=wall_time,
            )

        except Exception as e:
            wall_time = time.monotonic() - start_time
            logger.error("Sandbox execution error: %s", e)
            return SandboxResult(
                exit_code=-1,
                stdout="",
                stderr=f"Sandbox execution error: {e}",
                timed_out=wall_time >= self.config.timeout_s,
                wall_time_s=wall_time,
            )
        finally:
            if self._watchdog:
                self._watchdog.cancel()
                self._watchdog = None

    def _cap_output(self, raw: bytes | None) -> str:
        """Cap output at the configured byte limit."""
        if raw is None:
            return ""
        limit = self.config.output_limit_bytes
        if len(raw) > limit:
            truncated = raw[:limit]
            try:
                text = truncated.decode("utf-8", errors="replace")
            except Exception:
                text = truncated.decode("latin-1")
            return text + TRUNCATION_MARKER
        try:
            return raw.decode("utf-8", errors="replace")
        except Exception:
            return raw.decode("latin-1")

    def _check_oom(self) -> bool:
        """Check if the container was OOM-killed."""
        if not self._container:
            return False
        try:
            self._container.reload()
            state = self._container.attrs.get("State", {})
            return bool(state.get("OOMKilled", False))
        except Exception:
            return False

    def _force_kill(self) -> None:
        """Watchdog callback: force-kill the container if it exceeds timeout."""
        logger.warning("Watchdog triggered for %s - force killing", self.container_name)
        try:
            if self._container:
                self._container.kill(signal="SIGKILL")
        except Exception as e:
            logger.error("Failed to kill container %s: %s", self.container_name, e)

    def cleanup(self) -> None:
        """Remove the container. MUST be called - use try/finally or context manager."""
        if self._watchdog:
            self._watchdog.cancel()
            self._watchdog = None

        if self._container:
            try:
                self._container.remove(force=True)
                logger.debug("Removed container %s", self.container_name)
            except docker.errors.NotFound:
                pass  # already removed
            except Exception as e:
                logger.error("Failed to remove container %s: %s", self.container_name, e)
            finally:
                self._container = None

    def __enter__(self) -> "Sandbox":
        return self

    def __exit__(self, *_: Any) -> None:
        self.cleanup()


def copy_directory_to_files(directory: Path) -> dict[str, str | bytes]:
    """Recursively read a directory into a filename -> content mapping.

    Used to prepare work_files for Sandbox.prepare().
    """
    files: dict[str, str | bytes] = {}
    if not directory.exists():
        return files

    for path in directory.rglob("*"):
        if path.is_file():
            rel = str(path.relative_to(directory))
            try:
                files[rel] = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                files[rel] = path.read_bytes()
    return files
