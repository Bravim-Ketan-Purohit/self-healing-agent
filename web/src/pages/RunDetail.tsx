import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

interface Metrics {
  pass_at_1: { count: number; total: number; rate: number; ci_lower: number; ci_upper: number };
  pass_at_n: { count: number; total: number; rate: number; ci_lower: number; ci_upper: number };
  resolution_rate: { count: number; total: number; rate: number; ci_lower: number; ci_upper: number };
  false_success: { count: number; total: number; rate: number };
  tamper_count: number;
  total_cost_usd: number;
  cost_per_resolved_usd: number;
  per_tier: Record<string, { pass_at_1: number; pass_at_n: number; cost_usd: number; solvable: number }>;
}

interface TaskResult {
  task_id: string;
  tier: string;
  solvable: boolean;
  verdict: string;
  total_attempts: number;
  total_cost_usd: number;
  pass_at_1: boolean;
  pass_at_n: boolean;
}

interface RunData {
  manifest: {
    run_id: string;
    models: string[];
    seed: number;
    max_attempts: number;
    timestamp: string;
    task_results: TaskResult[];
  };
  metrics: Metrics;
}

function VerdictBadge({ verdict }: { verdict: string }) {
  const colors: Record<string, string> = {
    "passed@1": "bg-emerald-900 text-emerald-300",
    resolved: "bg-blue-900 text-blue-300",
    unresolved: "bg-red-900 text-red-300",
    tampered: "bg-purple-900 text-purple-300",
    false_success: "bg-yellow-900 text-yellow-300",
    error: "bg-gray-700 text-gray-300",
  };
  return (
    <span className={`px-2 py-0.5 rounded text-xs font-medium ${colors[verdict] || colors.error}`}>
      {verdict}
    </span>
  );
}

function MetricCard({ label, value, sub }: { label: string; value: string; sub?: string }) {
  return (
    <div className="bg-gray-900 border border-gray-800 rounded-lg p-4">
      <div className="text-gray-400 text-xs uppercase tracking-wide">{label}</div>
      <div className="text-2xl font-bold mt-1">{value}</div>
      {sub && <div className="text-gray-500 text-xs mt-1">{sub}</div>}
    </div>
  );
}

export default function RunDetail() {
  const { runId } = useParams<{ runId: string }>();
  const [data, setData] = useState<RunData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!runId) return;
    fetch(`/api/runs/${runId}`)
      .then((r) => r.json())
      .then((d) => { setData(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, [runId]);

  if (loading) return <div className="text-gray-400">Loading...</div>;
  if (!data) return <div className="text-red-400">Run not found</div>;

  const { manifest, metrics } = data;

  return (
    <div>
      <div className="flex items-center gap-3 mb-6">
        <Link to="/runs" className="text-gray-400 hover:text-white">&larr; Runs</Link>
        <h1 className="text-xl font-bold font-mono">{manifest.run_id}</h1>
      </div>

      {/* Metrics cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <MetricCard
          label="pass@1"
          value={`${(metrics.pass_at_1.rate * 100).toFixed(1)}%`}
          sub={`${metrics.pass_at_1.count}/${metrics.pass_at_1.total} [${metrics.pass_at_1.ci_lower.toFixed(2)}, ${metrics.pass_at_1.ci_upper.toFixed(2)}]`}
        />
        <MetricCard
          label="pass@N"
          value={`${(metrics.pass_at_n.rate * 100).toFixed(1)}%`}
          sub={`${metrics.pass_at_n.count}/${metrics.pass_at_n.total} [${metrics.pass_at_n.ci_lower.toFixed(2)}, ${metrics.pass_at_n.ci_upper.toFixed(2)}]`}
        />
        <MetricCard
          label="Resolution"
          value={`${(metrics.resolution_rate.rate * 100).toFixed(1)}%`}
          sub={`${metrics.resolution_rate.count}/${metrics.resolution_rate.total} failures resolved`}
        />
        <MetricCard
          label="Cost"
          value={`$${metrics.total_cost_usd.toFixed(4)}`}
          sub={`$${metrics.cost_per_resolved_usd.toFixed(4)}/resolved`}
        />
      </div>

      {/* T5 + tamper */}
      <div className="flex gap-4 mb-8 text-sm">
        <div className="text-gray-400">
          T5 false success: <span className="text-yellow-400">{metrics.false_success.count}/{metrics.false_success.total}</span>
        </div>
        <div className="text-gray-400">
          Tamper: <span className="text-purple-400">{metrics.tamper_count}</span>
        </div>
      </div>

      {/* Task results table */}
      <h2 className="text-lg font-bold mb-4">Task Results</h2>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-gray-800 text-gray-400">
              <th className="text-left py-2 px-2">Task</th>
              <th className="text-left py-2 px-2">Tier</th>
              <th className="text-left py-2 px-2">Verdict</th>
              <th className="text-right py-2 px-2">Attempts</th>
              <th className="text-right py-2 px-2">Cost</th>
            </tr>
          </thead>
          <tbody>
            {manifest.task_results.map((task) => (
              <tr key={task.task_id} className="border-b border-gray-800/50 hover:bg-gray-900/50">
                <td className="py-2 px-2">
                  <Link
                    to={`/runs/${runId}/tasks/${task.task_id}`}
                    className="text-emerald-400 hover:underline"
                  >
                    {task.task_id}
                  </Link>
                </td>
                <td className="py-2 px-2 text-gray-400">{task.tier}</td>
                <td className="py-2 px-2">
                  <VerdictBadge verdict={task.verdict} />
                </td>
                <td className="py-2 px-2 text-right">{task.total_attempts}</td>
                <td className="py-2 px-2 text-right text-yellow-400">
                  ${task.total_cost_usd.toFixed(4)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
