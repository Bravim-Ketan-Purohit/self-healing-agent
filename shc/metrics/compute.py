"""Metrics computation for self-healing agent runs.

Computes:
  - pass@1: fraction of tasks solved on first attempt (no repair)
  - pass@N: fraction of tasks solved within N attempts
  - resolution_rate: fraction of FAILURES (not tasks) that were resolved
  - false_success_rate: fraction of T5 unsolvable tasks incorrectly "solved"
  - cost_per_resolved: average cost per resolved failure
  - Wilson score confidence intervals
  - Bootstrap CIs for resolution rate
  - Per-model and per-tier breakdowns

IMPORTANT: The headline denominator is FAILURES, not tasks. A task that passed
on first attempt (pass@1) is not a "failure" and does not contribute to the
resolution rate denominator.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

from shc.models import RunManifest, TaskResult, Tier, Verdict


@dataclass
class ConfidenceInterval:
    """A point estimate with confidence interval."""

    estimate: float
    lower: float
    upper: float
    confidence: float = 0.95
    n: int = 0

    def __str__(self) -> str:
        return f"{self.estimate:.3f} [{self.lower:.3f}, {self.upper:.3f}] (n={self.n})"


@dataclass
class MetricsReport:
    """Complete metrics report for a set of runs."""

    # Raw counts
    total_tasks: int = 0
    total_solvable: int = 0
    total_unsolvable: int = 0

    # pass@1: solved on first attempt (no repair needed)
    pass_at_1_count: int = 0
    pass_at_1_rate: ConfidenceInterval = field(
        default_factory=lambda: ConfidenceInterval(0, 0, 0)
    )

    # pass@N: solved within max attempts
    pass_at_n_count: int = 0
    pass_at_n_rate: ConfidenceInterval = field(
        default_factory=lambda: ConfidenceInterval(0, 0, 0)
    )

    # Resolution rate: failures resolved / total first-attempt failures
    first_attempt_failures: int = 0
    resolved_count: int = 0
    resolution_rate: ConfidenceInterval = field(
        default_factory=lambda: ConfidenceInterval(0, 0, 0)
    )

    # T5 false success
    t5_total: int = 0
    t5_false_success_count: int = 0
    false_success_rate: ConfidenceInterval = field(
        default_factory=lambda: ConfidenceInterval(0, 0, 0)
    )

    # Tamper
    tamper_count: int = 0

    # Cost
    total_cost_usd: float = 0.0
    cost_per_resolved_usd: float = 0.0

    # Per-tier breakdown
    per_tier: dict[str, dict[str, float]] = field(default_factory=dict)

    # Per-model breakdown
    per_model: dict[str, dict[str, float]] = field(default_factory=dict)


def _norm_ppf(p: float) -> float:
    """Approximate inverse normal CDF (percent point function).

    Uses the rational approximation from Abramowitz & Stegun.
    Accurate to ~4.5e-4 for 0.5 < p < 1.
    """
    # For p > 0.5, use the symmetry property
    if p < 0.5:
        return -_norm_ppf(1 - p)
    if p == 0.5:
        return 0.0

    t = math.sqrt(-2 * math.log(1 - p))
    # Rational approximation constants
    c0, c1, c2 = 2.515517, 0.802853, 0.010328
    d1, d2, d3 = 1.432788, 0.189269, 0.001308
    return t - (c0 + c1 * t + c2 * t**2) / (1 + d1 * t + d2 * t**2 + d3 * t**3)


def wilson_ci(successes: int, trials: int, confidence: float = 0.95) -> ConfidenceInterval:
    """Compute Wilson score confidence interval for a proportion.

    Wilson intervals are preferred over normal approximation for small samples
    and extreme proportions. They never produce intervals outside [0, 1].
    """
    if trials == 0:
        return ConfidenceInterval(estimate=0.0, lower=0.0, upper=0.0, confidence=confidence, n=0)

    z = _norm_ppf(1 - (1 - confidence) / 2)
    p_hat = successes / trials
    denominator = 1 + z**2 / trials

    center = (p_hat + z**2 / (2 * trials)) / denominator
    margin = (z / denominator) * math.sqrt(
        p_hat * (1 - p_hat) / trials + z**2 / (4 * trials**2)
    )

    return ConfidenceInterval(
        estimate=p_hat,
        lower=max(0.0, center - margin),
        upper=min(1.0, center + margin),
        confidence=confidence,
        n=trials,
    )


def bootstrap_ci(
    successes: int,
    trials: int,
    confidence: float = 0.95,
    n_bootstrap: int = 10000,
    seed: int = 42,
) -> ConfidenceInterval:
    """Compute bootstrap confidence interval for a proportion.

    Used as a secondary CI method alongside Wilson for robustness.
    """
    if trials == 0:
        return ConfidenceInterval(estimate=0.0, lower=0.0, upper=0.0, confidence=confidence, n=0)

    rng = np.random.default_rng(seed)
    p_hat = successes / trials

    # Create binary outcome array
    outcomes = np.zeros(trials)
    outcomes[:successes] = 1.0

    # Bootstrap
    boot_proportions = np.zeros(n_bootstrap)
    for i in range(n_bootstrap):
        sample = rng.choice(outcomes, size=trials, replace=True)
        boot_proportions[i] = sample.mean()

    alpha = 1 - confidence
    lower = float(np.percentile(boot_proportions, 100 * alpha / 2))
    upper = float(np.percentile(boot_proportions, 100 * (1 - alpha / 2)))

    return ConfidenceInterval(
        estimate=p_hat,
        lower=lower,
        upper=upper,
        confidence=confidence,
        n=trials,
    )


def compute_metrics(
    manifests: list[RunManifest],
    confidence: float = 0.95,
) -> MetricsReport:
    """Compute aggregate metrics from one or more run manifests.

    Args:
        manifests: list of completed run manifests
        confidence: confidence level for intervals (default 95%)

    Returns:
        MetricsReport with all computed metrics
    """
    report = MetricsReport()

    # Collect all task results across runs
    all_results: list[TaskResult] = []
    for manifest in manifests:
        all_results.extend(manifest.task_results)

    if not all_results:
        return report

    report.total_tasks = len(all_results)

    # Separate solvable and unsolvable
    solvable = [r for r in all_results if r.solvable]
    unsolvable = [r for r in all_results if not r.solvable]
    report.total_solvable = len(solvable)
    report.total_unsolvable = len(unsolvable)

    # --- pass@1 (among solvable tasks) ---
    pass_at_1_results = [r for r in solvable if r.pass_at_1]
    report.pass_at_1_count = len(pass_at_1_results)
    report.pass_at_1_rate = wilson_ci(
        report.pass_at_1_count, report.total_solvable, confidence
    )

    # --- pass@N (among solvable tasks) ---
    pass_at_n_results = [r for r in solvable if r.pass_at_n]
    report.pass_at_n_count = len(pass_at_n_results)
    report.pass_at_n_rate = wilson_ci(
        report.pass_at_n_count, report.total_solvable, confidence
    )

    # --- Resolution rate ---
    # Denominator: tasks that FAILED on first attempt (not tasks that passed@1)
    # Numerator: of those failures, how many were resolved
    first_failures = [r for r in solvable if not r.pass_at_1]
    report.first_attempt_failures = len(first_failures)
    resolved = [r for r in first_failures if r.verdict == Verdict.RESOLVED]
    report.resolved_count = len(resolved)
    report.resolution_rate = wilson_ci(
        report.resolved_count, report.first_attempt_failures, confidence
    )

    # --- T5 false success rate ---
    report.t5_total = len(unsolvable)
    false_successes = [r for r in unsolvable if r.verdict == Verdict.FALSE_SUCCESS]
    report.t5_false_success_count = len(false_successes)
    report.false_success_rate = wilson_ci(
        report.t5_false_success_count, report.t5_total, confidence
    )

    # --- Tamper count ---
    report.tamper_count = sum(1 for r in all_results if r.verdict == Verdict.TAMPERED)

    # --- Cost ---
    report.total_cost_usd = sum(r.total_cost_usd for r in all_results)
    if report.resolved_count > 0:
        # Cost per resolved = cost of failures that were resolved / number resolved
        resolved_cost = sum(r.total_cost_usd for r in resolved)
        report.cost_per_resolved_usd = resolved_cost / report.resolved_count
    else:
        report.cost_per_resolved_usd = 0.0

    # --- Per-tier breakdown ---
    for tier in Tier:
        tier_results = [r for r in all_results if r.tier == tier]
        if not tier_results:
            continue
        tier_solvable = [r for r in tier_results if r.solvable]
        tier_p1 = sum(1 for r in tier_solvable if r.pass_at_1)
        tier_pn = sum(1 for r in tier_solvable if r.pass_at_n)
        n_solvable = len(tier_solvable)

        report.per_tier[tier.value] = {
            "total": len(tier_results),
            "solvable": n_solvable,
            "pass_at_1": tier_p1 / n_solvable if n_solvable else 0,
            "pass_at_n": tier_pn / n_solvable if n_solvable else 0,
            "cost_usd": sum(r.total_cost_usd for r in tier_results),
        }

    # --- Per-model breakdown (from manifest metadata) ---
    model_results: dict[str, list[TaskResult]] = {}
    for manifest in manifests:
        for model in manifest.models:
            if model not in model_results:
                model_results[model] = []
            model_results[model].extend(manifest.task_results)

    for model, results in model_results.items():
        m_solvable = [r for r in results if r.solvable]
        m_p1 = sum(1 for r in m_solvable if r.pass_at_1)
        m_pn = sum(1 for r in m_solvable if r.pass_at_n)
        n_solv = len(m_solvable)
        m_failures = [r for r in m_solvable if not r.pass_at_1]
        m_resolved = sum(1 for r in m_failures if r.verdict == Verdict.RESOLVED)

        report.per_model[model] = {
            "total_tasks": len(results),
            "solvable": n_solv,
            "pass_at_1": m_p1 / n_solv if n_solv else 0,
            "pass_at_n": m_pn / n_solv if n_solv else 0,
            "resolution_rate": m_resolved / len(m_failures) if m_failures else 0,
            "cost_usd": sum(r.total_cost_usd for r in results),
        }

    return report
