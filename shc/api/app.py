"""FastAPI application for the run viewer.

Provides REST endpoints for:
  - GET /api/runs - list all runs
  - GET /api/runs/{run_id} - get run details with task results
  - GET /api/runs/{run_id}/tasks/{task_id} - get task detail with attempts
  - GET /api/leaderboard - model leaderboard
  - GET /api/events - SSE stream for live run progress
"""

from __future__ import annotations

import asyncio
import json
import logging
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sse_starlette.sse import EventSourceResponse

from shc.metrics.compute import compute_metrics
from shc.metrics.report import load_all_runs, load_run
from shc.models import RunManifest

logger = logging.getLogger(__name__)

RUNS_DIR = Path(__file__).resolve().parent.parent.parent / "runs"
WEB_DIST = Path(__file__).resolve().parent.parent.parent / "web" / "dist"

app = FastAPI(
    title="Self-Healing Agent - Run Viewer",
    version="0.1.0",
    docs_url="/api/docs",
)

# CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- API Routes ---


@app.get("/api/runs")
async def list_runs() -> list[dict[str, Any]]:
    """List all runs with summary metadata."""
    manifests = load_all_runs()
    runs = []
    for m in manifests:
        total_tasks = len(m.task_results)
        passed = sum(1 for r in m.task_results if r.pass_at_n)
        runs.append({
            "run_id": m.run_id,
            "models": m.models,
            "tiers": m.tiers,
            "seed": m.seed,
            "timestamp": m.timestamp,
            "total_tasks": total_tasks,
            "passed": passed,
            "pass_rate": passed / total_tasks if total_tasks else 0,
            "total_cost_usd": sum(r.total_cost_usd for r in m.task_results),
        })
    return runs


@app.get("/api/runs/{run_id}")
async def get_run(run_id: str) -> dict[str, Any]:
    """Get full run details including all task results."""
    try:
        manifest = load_run(run_id)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e

    # Compute metrics for this single run
    report = compute_metrics([manifest])

    return {
        "manifest": manifest.model_dump(),
        "metrics": {
            "pass_at_1": {
                "count": report.pass_at_1_count,
                "total": report.total_solvable,
                "rate": report.pass_at_1_rate.estimate,
                "ci_lower": report.pass_at_1_rate.lower,
                "ci_upper": report.pass_at_1_rate.upper,
            },
            "pass_at_n": {
                "count": report.pass_at_n_count,
                "total": report.total_solvable,
                "rate": report.pass_at_n_rate.estimate,
                "ci_lower": report.pass_at_n_rate.lower,
                "ci_upper": report.pass_at_n_rate.upper,
            },
            "resolution_rate": {
                "count": report.resolved_count,
                "total": report.first_attempt_failures,
                "rate": report.resolution_rate.estimate,
                "ci_lower": report.resolution_rate.lower,
                "ci_upper": report.resolution_rate.upper,
            },
            "false_success": {
                "count": report.t5_false_success_count,
                "total": report.t5_total,
                "rate": report.false_success_rate.estimate,
            },
            "tamper_count": report.tamper_count,
            "total_cost_usd": report.total_cost_usd,
            "cost_per_resolved_usd": report.cost_per_resolved_usd,
            "per_tier": report.per_tier,
        },
    }


@app.get("/api/runs/{run_id}/tasks/{task_id}")
async def get_task_detail(run_id: str, task_id: str) -> dict[str, Any]:
    """Get detailed task result with all attempts."""
    try:
        manifest = load_run(run_id)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e

    task_result = next(
        (r for r in manifest.task_results if r.task_id == task_id), None
    )
    if task_result is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found in run {run_id}")

    return task_result.model_dump()


@app.get("/api/leaderboard")
async def get_leaderboard() -> list[dict[str, Any]]:
    """Get model leaderboard across all runs."""
    manifests = load_all_runs()
    if not manifests:
        return []

    # Group results by model
    model_data: dict[str, list[RunManifest]] = {}
    for m in manifests:
        for model in m.models:
            if model not in model_data:
                model_data[model] = []
            model_data[model].append(m)

    leaderboard = []
    for model, model_manifests in model_data.items():
        report = compute_metrics(model_manifests)
        leaderboard.append({
            "model": model,
            "pass_at_1": report.pass_at_1_rate.estimate,
            "pass_at_n": report.pass_at_n_rate.estimate,
            "resolution_rate": report.resolution_rate.estimate,
            "false_success_rate": report.false_success_rate.estimate,
            "total_cost_usd": report.total_cost_usd,
            "cost_per_resolved_usd": report.cost_per_resolved_usd,
            "total_tasks": report.total_solvable,
            "runs": len(model_manifests),
        })

    # Sort by resolution rate descending
    leaderboard.sort(key=lambda x: x["resolution_rate"], reverse=True)
    return leaderboard


@app.get("/api/events")
async def event_stream() -> EventSourceResponse:
    """SSE endpoint for live run progress updates."""

    async def generate():
        """Watch the runs directory for new/updated manifests."""
        seen_mtimes: dict[str, float] = {}

        while True:
            if RUNS_DIR.exists():
                for run_dir in RUNS_DIR.iterdir():
                    manifest_path = run_dir / "manifest.json"
                    if manifest_path.exists():
                        mtime = manifest_path.stat().st_mtime
                        if (
                            manifest_path.name not in seen_mtimes
                            or seen_mtimes[manifest_path.name] < mtime
                        ):
                            seen_mtimes[manifest_path.name] = mtime
                            try:
                                with open(manifest_path) as f:
                                    data = json.load(f)
                                yield {
                                    "event": "run_update",
                                    "data": json.dumps({
                                        "run_id": data.get("run_id"),
                                        "total_tasks": len(data.get("task_results", [])),
                                        "timestamp": data.get("timestamp"),
                                    }),
                                }
                            except (json.JSONDecodeError, OSError):
                                pass

            await asyncio.sleep(2)

    return EventSourceResponse(generate())


# Serve frontend static files if they exist
if WEB_DIST.exists():
    app.mount("/", StaticFiles(directory=str(WEB_DIST), html=True), name="static")


def start_server(host: str = "0.0.0.0", port: int = 8000) -> None:
    """Start the API server."""
    import uvicorn

    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    start_server()
