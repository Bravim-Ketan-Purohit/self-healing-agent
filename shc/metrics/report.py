"""Report generation from run manifests.

Loads run data from disk and produces formatted reports with all
required metrics: pass@1, pass@N, resolution rate with raw counts
and CIs, false-success on T5, cost per resolved failure.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

from rich.console import Console
from rich.table import Table

from shc.metrics.compute import MetricsReport, compute_metrics
from shc.models import RunManifest

logger = logging.getLogger(__name__)

RUNS_DIR = Path(__file__).resolve().parent.parent.parent / "runs"


def load_run(run_id: str) -> RunManifest:
    """Load a run manifest from disk."""
    manifest_path = RUNS_DIR / run_id / "manifest.json"
    if not manifest_path.exists():
        msg = f"Run not found: {run_id}"
        raise FileNotFoundError(msg)

    with open(manifest_path) as f:
        data = json.load(f)
    return RunManifest(**data)


def load_all_runs() -> list[RunManifest]:
    """Load all run manifests from the runs directory."""
    manifests: list[RunManifest] = []
    if not RUNS_DIR.exists():
        return manifests

    for run_dir in sorted(RUNS_DIR.iterdir()):
        manifest_path = run_dir / "manifest.json"
        if manifest_path.exists():
            try:
                with open(manifest_path) as f:
                    data = json.load(f)
                manifests.append(RunManifest(**data))
            except (json.JSONDecodeError, ValueError) as e:
                logger.warning("Skipping invalid manifest %s: %s", manifest_path, e)

    return manifests


def format_report(report: MetricsReport) -> str:
    """Format a metrics report as a plain text string."""
    lines: list[str] = []
    lines.append("=" * 70)
    lines.append("SELF-HEALING AGENT - METRICS REPORT")
    lines.append("=" * 70)
    lines.append("")

    # --- Summary ---
    lines.append("SUMMARY")
    lines.append("-" * 40)
    lines.append(f"Total tasks evaluated:  {report.total_tasks}")
    lines.append(f"  Solvable (T0-T4):     {report.total_solvable}")
    lines.append(f"  Unsolvable (T5):      {report.total_unsolvable}")
    lines.append("")

    # --- pass@1 ---
    lines.append("PASS@1 (solved on first attempt, no repair)")
    lines.append(f"  {report.pass_at_1_count} of {report.total_solvable} solvable tasks")
    lines.append(f"  Rate: {report.pass_at_1_rate}")
    lines.append("")

    # --- pass@N ---
    lines.append("PASS@N (solved within max attempts)")
    lines.append(f"  {report.pass_at_n_count} of {report.total_solvable} solvable tasks")
    lines.append(f"  Rate: {report.pass_at_n_rate}")
    lines.append("")

    # --- Resolution rate ---
    lines.append("RESOLUTION RATE (failures resolved / first-attempt failures)")
    lines.append(
        f"  {report.resolved_count} of {report.first_attempt_failures} "
        f"first-attempt failures resolved"
    )
    lines.append(f"  Rate: {report.resolution_rate}")
    lines.append("")

    # --- T5 false success ---
    lines.append("T5 FALSE SUCCESS (unsolvable tasks incorrectly 'solved')")
    lines.append(f"  {report.t5_false_success_count} of {report.t5_total} unsolvable tasks")
    lines.append(f"  Rate: {report.false_success_rate}")
    lines.append("")

    # --- Tamper ---
    lines.append(f"TAMPER DETECTIONS: {report.tamper_count}")
    lines.append("")

    # --- Cost ---
    lines.append("COST")
    lines.append(f"  Total:           ${report.total_cost_usd:.4f}")
    lines.append(f"  Per resolved:    ${report.cost_per_resolved_usd:.4f}")
    lines.append("")

    # --- Per-tier ---
    if report.per_tier:
        lines.append("PER-TIER BREAKDOWN")
        lines.append("-" * 40)
        for tier, data in sorted(report.per_tier.items()):
            lines.append(
                f"  {tier}: pass@1={data['pass_at_1']:.2%}, "
                f"pass@N={data['pass_at_n']:.2%}, "
                f"cost=${data['cost_usd']:.4f} "
                f"(n={int(data['solvable'])})"
            )
        lines.append("")

    # --- Per-model ---
    if report.per_model:
        lines.append("PER-MODEL BREAKDOWN")
        lines.append("-" * 40)
        for model, data in sorted(report.per_model.items()):
            lines.append(
                f"  {model}:"
            )
            lines.append(
                f"    pass@1={data['pass_at_1']:.2%}, "
                f"pass@N={data['pass_at_n']:.2%}, "
                f"resolution={data['resolution_rate']:.2%}, "
                f"cost=${data['cost_usd']:.4f}"
            )
        lines.append("")

    lines.append("=" * 70)
    return "\n".join(lines)


def print_report_rich(report: MetricsReport) -> None:
    """Print a metrics report using rich formatting."""
    console = Console()

    console.print("\n[bold]SELF-HEALING AGENT - METRICS REPORT[/bold]\n")

    # Summary table
    summary = Table(title="Summary")
    summary.add_column("Metric", style="cyan")
    summary.add_column("Value", style="green")
    summary.add_column("95% CI", style="yellow")

    summary.add_row(
        "pass@1",
        f"{report.pass_at_1_count}/{report.total_solvable} ({report.pass_at_1_rate.estimate:.1%})",
        f"[{report.pass_at_1_rate.lower:.3f}, {report.pass_at_1_rate.upper:.3f}]",
    )
    summary.add_row(
        "pass@N",
        f"{report.pass_at_n_count}/{report.total_solvable} ({report.pass_at_n_rate.estimate:.1%})",
        f"[{report.pass_at_n_rate.lower:.3f}, {report.pass_at_n_rate.upper:.3f}]",
    )
    res_val = (
        f"{report.resolved_count}/{report.first_attempt_failures}"
        f" ({report.resolution_rate.estimate:.1%})"
    )
    summary.add_row(
        "Resolution rate",
        res_val,
        f"[{report.resolution_rate.lower:.3f}, {report.resolution_rate.upper:.3f}]",
    )
    fs_val = (
        f"{report.t5_false_success_count}/{report.t5_total}"
        f" ({report.false_success_rate.estimate:.1%})"
    )
    summary.add_row(
        "T5 false success",
        fs_val,
        f"[{report.false_success_rate.lower:.3f}, {report.false_success_rate.upper:.3f}]",
    )
    summary.add_row("Tamper detections", str(report.tamper_count), "")
    summary.add_row("Total cost", f"${report.total_cost_usd:.4f}", "")
    summary.add_row("Cost per resolved", f"${report.cost_per_resolved_usd:.4f}", "")

    console.print(summary)

    # Per-tier table
    if report.per_tier:
        tier_table = Table(title="\nPer-Tier Breakdown")
        tier_table.add_column("Tier")
        tier_table.add_column("Tasks")
        tier_table.add_column("pass@1")
        tier_table.add_column("pass@N")
        tier_table.add_column("Cost")

        for tier, data in sorted(report.per_tier.items()):
            tier_table.add_row(
                tier,
                str(int(data["solvable"])),
                f"{data['pass_at_1']:.1%}",
                f"{data['pass_at_n']:.1%}",
                f"${data['cost_usd']:.4f}",
            )
        console.print(tier_table)

    # Per-model table
    if report.per_model:
        model_table = Table(title="\nPer-Model Breakdown")
        model_table.add_column("Model")
        model_table.add_column("pass@1")
        model_table.add_column("pass@N")
        model_table.add_column("Resolution")
        model_table.add_column("Cost")

        for model, data in sorted(report.per_model.items()):
            model_table.add_row(
                model.split("/")[-1],
                f"{data['pass_at_1']:.1%}",
                f"{data['pass_at_n']:.1%}",
                f"{data['resolution_rate']:.1%}",
                f"${data['cost_usd']:.4f}",
            )
        console.print(model_table)

    console.print("")


def generate_report(run_id: str) -> None:
    """Generate and print a metrics report for a specific run or all runs.

    Args:
        run_id: specific run ID, or "all" to aggregate all runs
    """
    logging.basicConfig(level=logging.INFO)

    if run_id == "all":
        manifests = load_all_runs()
        if not manifests:
            print("No runs found in runs/ directory")
            return
    else:
        manifests = [load_run(run_id)]

    report = compute_metrics(manifests)
    print_report_rich(report)
    print(format_report(report))
