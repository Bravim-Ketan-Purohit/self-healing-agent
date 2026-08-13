"""Run orchestrator: executes the full benchmark across models, tasks, and seeds.

This is the top-level entry point that:
  1. Reaps orphaned containers (safety)
  2. Loads the task suite
  3. For each (model, seed) combination, runs all tasks through the repair loop
  4. Saves results to runs/{run_id}/
  5. Final reap (safety)
"""

from __future__ import annotations

import json
import logging
import uuid
from datetime import datetime, timezone
from pathlib import Path

from shc.agent.loop import run_task
from shc.llm.client import LLMClient
from shc.models import RunManifest, Tier
from shc.prompts.templates import PROMPT_VERSION
from shc.sandbox.reaper import reap_all, reap_by_prefix
from shc.suite.loader import load_suite

logger = logging.getLogger(__name__)

RUNS_DIR = Path(__file__).resolve().parent.parent / "runs"


def execute_run(
    models: list[str],
    tiers: list[str] | None = None,
    seeds: int = 3,
    max_attempts: int = 5,
    temperature: float = 0.0,
) -> None:
    """Execute a full benchmark run.

    Args:
        models: list of OpenRouter model identifiers
        tiers: optional tier filter (defaults to all)
        seeds: number of seed repetitions
        max_attempts: max repair attempts per task
        temperature: sampling temperature
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    # Safety: reap any orphaned containers
    logger.info("Reaping orphaned containers...")
    reap_all()
    reap_by_prefix()

    # Load tasks
    tasks = load_suite(tiers=tiers)
    logger.info("Loaded %d tasks across tiers: %s", len(tasks), tiers or "all")

    # Estimate cost before proceeding
    client = LLMClient()
    estimate = client.estimate_sweep_cost(
        models=models,
        num_tasks=len(tasks),
        max_attempts=max_attempts,
        seeds=seeds,
    )
    logger.info("Cost estimate: $%.2f total", estimate["total_estimated_usd"])
    for model_name, cost in estimate["breakdown_by_model"].items():
        logger.info("  %s: $%.2f", model_name, cost)

    # Execute per seed and model
    for seed in range(seeds):
        for model in models:
            run_id = f"{uuid.uuid4().hex[:8]}_{model.split('/')[-1]}_{seed}"
            logger.info("=" * 60)
            logger.info("RUN: %s (model=%s, seed=%d)", run_id, model, seed)
            logger.info("=" * 60)

            manifest = RunManifest(
                run_id=run_id,
                models=[model],
                tiers=tiers or [t.value for t in Tier],
                seed=seed,
                max_attempts=max_attempts,
                temperature=temperature,
                timestamp=datetime.now(timezone.utc).isoformat(),
                prompt_version=PROMPT_VERSION,
            )

            for task in tasks:
                try:
                    task_result = run_task(
                        task=task,
                        run_id=run_id,
                        model=model,
                        client=client,
                        max_attempts=max_attempts,
                        temperature=temperature,
                        seed=seed,
                    )
                    manifest.task_results.append(task_result)

                    logger.info(
                        "  %s: %s (attempts=%d, cost=$%.4f)",
                        task.id,
                        task_result.verdict.value,
                        task_result.total_attempts,
                        task_result.total_cost_usd,
                    )
                except Exception as e:
                    logger.error("  %s: ERROR - %s", task.id, e)

            # Save run manifest
            _save_run(manifest)
            logger.info(
                "Run %s complete. Total cost: $%.4f",
                run_id,
                client.total_cost,
            )

    # Final safety: reap all containers
    logger.info("Final reap...")
    reap_all()
    reap_by_prefix()

    # Print summary
    logger.info("=" * 60)
    logger.info("ALL RUNS COMPLETE")
    logger.info("Total LLM cost: $%.4f", client.total_cost)
    logger.info("LLM stats: %s", client.stats)


def _save_run(manifest: RunManifest) -> None:
    """Save a run manifest to disk."""
    run_dir = RUNS_DIR / manifest.run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    manifest_path = run_dir / "manifest.json"
    with open(manifest_path, "w") as f:
        json.dump(manifest.model_dump(), f, indent=2)

    logger.info("Saved run manifest: %s", manifest_path)
