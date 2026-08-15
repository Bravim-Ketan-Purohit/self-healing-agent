import { useEffect, useState } from "react";

interface ModelEntry {
  model: string;
  pass_at_1: number;
  pass_at_n: number;
  resolution_rate: number;
  false_success_rate: number;
  total_cost_usd: number;
  cost_per_resolved_usd: number;
  total_tasks: number;
  runs: number;
}

export default function Leaderboard() {
  const [data, setData] = useState<ModelEntry[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/leaderboard")
      .then((r) => r.json())
      .then((d) => { setData(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="text-gray-400">Loading...</div>;

  if (data.length === 0) {
    return (
      <div className="text-center py-12">
        <h2 className="text-xl text-gray-400">No data yet</h2>
        <p className="text-gray-500 mt-2">Complete runs with multiple models to see the leaderboard.</p>
      </div>
    );
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Model Leaderboard</h1>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-gray-800 text-gray-400">
              <th className="text-left py-3 px-2">#</th>
              <th className="text-left py-3 px-2">Model</th>
              <th className="text-right py-3 px-2">pass@1</th>
              <th className="text-right py-3 px-2">pass@N</th>
              <th className="text-right py-3 px-2">Resolution</th>
              <th className="text-right py-3 px-2">T5 False+</th>
              <th className="text-right py-3 px-2">Cost/Resolved</th>
              <th className="text-right py-3 px-2">Total Cost</th>
              <th className="text-right py-3 px-2">Tasks</th>
              <th className="text-right py-3 px-2">Runs</th>
            </tr>
          </thead>
          <tbody>
            {data.map((entry, idx) => (
              <tr key={entry.model} className="border-b border-gray-800/50 hover:bg-gray-900/50">
                <td className="py-3 px-2 text-gray-500">{idx + 1}</td>
                <td className="py-3 px-2 font-medium">
                  {entry.model.split("/").pop()}
                </td>
                <td className="py-3 px-2 text-right">
                  {(entry.pass_at_1 * 100).toFixed(1)}%
                </td>
                <td className="py-3 px-2 text-right text-emerald-400">
                  {(entry.pass_at_n * 100).toFixed(1)}%
                </td>
                <td className="py-3 px-2 text-right text-blue-400">
                  {(entry.resolution_rate * 100).toFixed(1)}%
                </td>
                <td className="py-3 px-2 text-right text-yellow-400">
                  {(entry.false_success_rate * 100).toFixed(1)}%
                </td>
                <td className="py-3 px-2 text-right">
                  ${entry.cost_per_resolved_usd.toFixed(4)}
                </td>
                <td className="py-3 px-2 text-right text-yellow-400">
                  ${entry.total_cost_usd.toFixed(4)}
                </td>
                <td className="py-3 px-2 text-right text-gray-400">
                  {entry.total_tasks}
                </td>
                <td className="py-3 px-2 text-right text-gray-400">
                  {entry.runs}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
