import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

interface RunSummary {
  run_id: string;
  models: string[];
  tiers: string[];
  seed: number;
  timestamp: string;
  total_tasks: number;
  passed: number;
  pass_rate: number;
  total_cost_usd: number;
}

export default function RunsList() {
  const [runs, setRuns] = useState<RunSummary[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/runs")
      .then((r) => r.json())
      .then((data) => {
        setRuns(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  if (loading) {
    return <div className="text-gray-400">Loading runs...</div>;
  }

  if (runs.length === 0) {
    return (
      <div className="text-center py-12">
        <h2 className="text-xl text-gray-400">No runs yet</h2>
        <p className="text-gray-500 mt-2">
          Run <code className="text-emerald-400">shc run --models ...</code> to generate data.
        </p>
      </div>
    );
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Runs</h1>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-gray-800 text-gray-400">
              <th className="text-left py-3 px-2">Run ID</th>
              <th className="text-left py-3 px-2">Model</th>
              <th className="text-left py-3 px-2">Seed</th>
              <th className="text-right py-3 px-2">Tasks</th>
              <th className="text-right py-3 px-2">Passed</th>
              <th className="text-right py-3 px-2">Rate</th>
              <th className="text-right py-3 px-2">Cost</th>
              <th className="text-left py-3 px-2">Time</th>
            </tr>
          </thead>
          <tbody>
            {runs.map((run) => (
              <tr
                key={run.run_id}
                className="border-b border-gray-800/50 hover:bg-gray-900/50"
              >
                <td className="py-3 px-2">
                  <Link
                    to={`/runs/${run.run_id}`}
                    className="text-emerald-400 hover:underline font-mono text-xs"
                  >
                    {run.run_id}
                  </Link>
                </td>
                <td className="py-3 px-2 text-gray-300">
                  {run.models.map((m) => m.split("/").pop()).join(", ")}
                </td>
                <td className="py-3 px-2 text-gray-400">{run.seed}</td>
                <td className="py-3 px-2 text-right">{run.total_tasks}</td>
                <td className="py-3 px-2 text-right text-emerald-400">
                  {run.passed}
                </td>
                <td className="py-3 px-2 text-right">
                  {(run.pass_rate * 100).toFixed(1)}%
                </td>
                <td className="py-3 px-2 text-right text-yellow-400">
                  ${run.total_cost_usd.toFixed(4)}
                </td>
                <td className="py-3 px-2 text-gray-500 text-xs">
                  {run.timestamp ? new Date(run.timestamp).toLocaleString() : "-"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
