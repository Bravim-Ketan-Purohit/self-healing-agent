"""Container reaper - removes orphaned shc-* containers.

This runs at orchestrator startup and shutdown to guarantee no containers
are left running from a crashed previous run. Also provides a standalone
CLI via `python -m shc.sandbox.reap`.
"""

from __future__ import annotations

import logging

import docker
from docker.errors import NotFound

from shc.sandbox.config import CONTAINER_PREFIX, LABEL_MANAGED

logger = logging.getLogger(__name__)


def reap_all(client: docker.DockerClient | None = None) -> int:
    """Remove all containers with the shc managed label.

    Returns the number of containers removed.
    """
    if client is None:
        client = docker.from_env()

    removed = 0
    containers = client.containers.list(
        all=True,
        filters={"label": f"{LABEL_MANAGED}=true"},
    )

    for container in containers:
        name = container.name or container.short_id
        try:
            container.remove(force=True)
            logger.info("Reaped container: %s", name)
            removed += 1
        except NotFound:
            pass  # race condition, already gone
        except Exception as e:
            logger.error("Failed to reap container %s: %s", name, e)

    if removed:
        logger.info("Reaped %d orphaned container(s)", removed)
    else:
        logger.debug("No orphaned containers found")

    return removed


def reap_by_run_id(run_id: str, client: docker.DockerClient | None = None) -> int:
    """Remove all containers for a specific run ID.

    Returns the number of containers removed.
    """
    if client is None:
        client = docker.from_env()

    removed = 0
    containers = client.containers.list(
        all=True,
        filters={"label": f"shc.run_id={run_id}"},
    )

    for container in containers:
        name = container.name or container.short_id
        try:
            container.remove(force=True)
            logger.info("Reaped container for run %s: %s", run_id, name)
            removed += 1
        except NotFound:
            pass
        except Exception as e:
            logger.error("Failed to reap container %s: %s", name, e)

    return removed


def reap_by_prefix(client: docker.DockerClient | None = None) -> int:
    """Fallback reaper: remove all containers whose name starts with shc-.

    This catches containers that might have been created without the managed label.
    """
    if client is None:
        client = docker.from_env()

    removed = 0
    containers = client.containers.list(all=True)

    for container in containers:
        name = container.name or ""
        if name.startswith(f"{CONTAINER_PREFIX}-"):
            try:
                container.remove(force=True)
                logger.info("Reaped by prefix: %s", name)
                removed += 1
            except NotFound:
                pass
            except Exception as e:
                logger.error("Failed to reap container %s: %s", name, e)

    return removed


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    total = reap_all()
    total += reap_by_prefix()
    print(f"Reaper complete: {total} container(s) removed")
