import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

interface Failure {
  kind: string;
  exc_type: string | null;
  message: string;
  file: string | null;
  line: number | null;
  failing_tests: string[];
  expected: string | null;
  actual: string | null;
}

interface Attempt {
  attempt_number: number;
  model: string;
  prompt_tokens: number;
  completion_tokens: number;
  cost_usd: number;
  wall_time_s: number;
  submitted_code: string;
  failure: Failure | null;
  passed_visible: boolean;
  passed_hidden: boolean;
  tampered: boolean;
  cheat_flags: string[];
}

interface TaskData {
  task_id: string;
  tier: string;
  solvable: boolean;
  verdict: string;
  attempts: Attempt[];
  pass_at_1: boolean;
  pass_at_n: boolean;
  total_cost_usd: number;
  total_attempts: number;
}

function AttemptTimeline({ attempts }: { attempts: Attempt[] }) {
  return (
    <div className="relative">
      {/* Timeline line */}
      <div className="absolute left-4 top-0 bottom-0 w-0.5 bg-gray-800" />

      {attempts.map((attempt, idx) => {
        const passed = attempt.passed_hidden;
        const color = passed ? "bg-emerald-500" : "bg-red-500";

        return (
          <div key={idx} className="relative pl-10 pb-8">
            {/* Timeline dot */}
            <div className={`absolute left-3 top-1 w-3 h-3 rounded-full ${color}`} />

            <div className="bg-gray-900 border border-gray-800 rounded-lg p-4">
              {/* Header */}
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-3">
                  <span className="text-sm font-bold">
                    Attempt {attempt.attempt_number}
                  </span>
                  <span className={`text-xs px-2 py-0.5 rounded ${
                    passed ? "bg-emerald-900 text-emerald-300" : "bg-red-900 text-red-300"
                  }`}>
                    {passed ? "PASS" : "FAIL"}
                  </span>
                  {attempt.tampered && (
                    <span className="text-xs px-2 py-0.5 rounded bg-purple-900 text-purple-300">
                      TAMPERED
                    </span>
                  )}
                </div>
                <div className="text-xs text-gray-500">
                  {attempt.wall_time_s.toFixed(1)}s | ${attempt.cost_usd.toFixed(4)} |{" "}
                  {attempt.prompt_tokens + attempt.completion_tokens} tok
                </div>
              </div>

              {/* Failure info */}
              {attempt.failure && (
                <div className="mb-3 p-3 bg-red-950/30 border border-red-900/30 rounded text-sm">
                  <div className="text-red-300 font-medium">
                    {attempt.failure.kind}: {attempt.failure.exc_type || ""}
                  </div>
                  {attempt.failure.message && (
                    <div className="text-red-200/70 mt-1 text-xs">{attempt.failure.message}</div>
                  )}
                  {attempt.failure.failing_tests.length > 0 && (
                    <div className="text-gray-400 mt-1 text-xs">
                      Failing: {attempt.failure.failing_tests.join(", ")}
                    </div>
                  )}
                  {attempt.failure.expected && attempt.failure.actual && (
                    <div className="mt-2 text-xs">
                      <span className="text-gray-500">Expected:</span>{" "}
                      <span className="text-emerald-300">{attempt.failure.expected}</span>
                      <br />
                      <span className="text-gray-500">Actual:</span>{" "}
                      <span className="text-red-300">{attempt.failure.actual}</span>
                    </div>
                  )}
                </div>
              )}

              {/* Code (collapsible) */}
              <details className="text-xs">
                <summary className="cursor-pointer text-gray-400 hover:text-gray-200">
                  Show code ({attempt.submitted_code.split("\n").length} lines)
                </summary>
                <pre className="mt-2 p-3 bg-gray-950 rounded overflow-x-auto text-gray-300 max-h-64 overflow-y-auto">
                  {attempt.submitted_code}
                </pre>
              </details>
            </div>
          </div>
        );
      })}
    </div>
  );
}

export default function TaskDetail() {
  const { runId, taskId } = useParams<{ runId: string; taskId: string }>();
  const [data, setData] = useState<TaskData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!runId || !taskId) return;
    fetch(`/api/runs/${runId}/tasks/${taskId}`)
      .then((r) => r.json())
      .then((d) => { setData(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, [runId, taskId]);

  if (loading) return <div className="text-gray-400">Loading...</div>;
  if (!data) return <div className="text-red-400">Task not found</div>;

  return (
    <div>
      <div className="flex items-center gap-3 mb-6">
        <Link to={`/runs/${runId}`} className="text-gray-400 hover:text-white">&larr; Run</Link>
        <h1 className="text-xl font-bold">{data.task_id}</h1>
        <span className="text-sm text-gray-400">{data.tier}</span>
        <span className={`text-xs px-2 py-0.5 rounded ${
          data.verdict === "passed@1" || data.verdict === "resolved"
            ? "bg-emerald-900 text-emerald-300"
            : data.verdict === "tampered"
            ? "bg-purple-900 text-purple-300"
            : "bg-red-900 text-red-300"
        }`}>
          {data.verdict}
        </span>
      </div>

      {/* Summary */}
      <div className="grid grid-cols-4 gap-4 mb-8 text-sm">
        <div className="bg-gray-900 border border-gray-800 rounded p-3">
          <div className="text-gray-400 text-xs">Attempts</div>
          <div className="text-lg font-bold">{data.total_attempts}</div>
        </div>
        <div className="bg-gray-900 border border-gray-800 rounded p-3">
          <div className="text-gray-400 text-xs">Cost</div>
          <div className="text-lg font-bold text-yellow-400">${data.total_cost_usd.toFixed(4)}</div>
        </div>
        <div className="bg-gray-900 border border-gray-800 rounded p-3">
          <div className="text-gray-400 text-xs">Solvable</div>
          <div className="text-lg font-bold">{data.solvable ? "Yes" : "No (T5)"}</div>
        </div>
        <div className="bg-gray-900 border border-gray-800 rounded p-3">
          <div className="text-gray-400 text-xs">pass@1</div>
          <div className="text-lg font-bold">{data.pass_at_1 ? "Yes" : "No"}</div>
        </div>
      </div>

      {/* Attempt timeline */}
      <h2 className="text-lg font-bold mb-4">Attempt Timeline</h2>
      <AttemptTimeline attempts={data.attempts} />
    </div>
  );
}
