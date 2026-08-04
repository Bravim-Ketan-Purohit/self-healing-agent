"""Sandbox configuration constants.

All security-relevant defaults live here. Never import from elsewhere.
"""

from __future__ import annotations

from dataclasses import dataclass

# Container naming prefix - seven sibling projects share this Docker daemon
CONTAINER_PREFIX = "shc"

# Default resource limits
DEFAULT_MEMORY_LIMIT = "512m"
DEFAULT_MEMORY_SWAP = "512m"
DEFAULT_NANO_CPUS = 1_000_000_000  # 1 CPU
DEFAULT_PIDS_LIMIT = 128
DEFAULT_TIMEOUT_S = 30
DEFAULT_OUTPUT_LIMIT_BYTES = 256 * 1024  # 256 KB

# Filesystem limits
FSIZE_LIMIT_BYTES = 64 * 1024 * 1024  # 64 MB
NOFILE_LIMIT = 256

# tmpfs mounts inside the container
TMPFS_MOUNTS = {
    "/tmp": "size=64m,mode=1777",
    "/work": "size=128m,mode=0755",
}

# Security: non-root user
SANDBOX_USER = "10001:10001"

# Label keys for identification and cleanup
LABEL_RUN_ID = "shc.run_id"
LABEL_TASK = "shc.task"
LABEL_MANAGED = "shc.managed"


@dataclass(frozen=True)
class SandboxConfig:
    """Per-task sandbox configuration."""

    image: str = "shc-sandbox:latest"
    image_digest: str | None = None
    memory_limit: str = DEFAULT_MEMORY_LIMIT
    memory_swap: str = DEFAULT_MEMORY_SWAP
    nano_cpus: int = DEFAULT_NANO_CPUS
    pids_limit: int = DEFAULT_PIDS_LIMIT
    timeout_s: int = DEFAULT_TIMEOUT_S
    output_limit_bytes: int = DEFAULT_OUTPUT_LIMIT_BYTES
    network_mode: str = "none"
    user: str = SANDBOX_USER
    env_allowlist: list[str] | None = None  # explicit env vars to pass (never secrets)
