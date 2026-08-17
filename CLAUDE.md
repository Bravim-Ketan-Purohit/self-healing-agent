# CLAUDE.md — Self-Healing Code-Generation Agent

Operating instructions for a Claude Code session in this repo. Read `SPEC.md` before writing code —
especially §1 (what the percentage means) and §4 (the sandbox is a security boundary). `ROADMAP.md` has
the order.

## What this is

An agent that generates code, runs it in a locked-down per-attempt Docker container, parses the failure
into structured form, feeds that back, and iterates — measured on a first-party graded task suite with
held-out tests. It exists to prove one resume bullet, quoted in `SPEC.md` §1.

## Hard rules

1. **Stay inside this directory.** Independent git repo; the parent is deliberately not a repo and seven
   sibling projects sit beside it. Never read, write, or `git` above `self-healing-agent/`.
2. **The sandbox ships before the agent.** M1 before M3. This repo's entire job is executing untrusted
   generated code on the user's laptop; the containment tests come first, not last.
3. **Never bind-mount host paths into a sandbox container.** Copy the working tree in with
   `put_archive`. A bind mount is a write primitive into the host filesystem.
4. **No secrets in the sandbox.** LLM calls happen in the orchestrator. The container gets an explicit
   env allow-list and `network_mode="none"` by default.
5. **Guaranteed teardown, always.** `try/finally` + force remove + watchdog + a label-based reaper on
   start and exit. Never leave a container running because a run crashed.
6. **Namespace every container and image** with `shc-` plus the run id. Seven sibling projects share this
   Docker daemon.
7. **Never invent a measurement.** Numbers come from committed run JSON in `runs/`. Report pass@1,
   pass@N, and the raw failure counts — never the resolution rate alone.
8. **Never let the agent see the hidden tests**, and never relax tamper detection to raise the score. If
   the agent found a way to game the harness, that is a finding worth writing down, not a bug to hide.
9. **Never touch the resume.** Different repo. Don't edit the `.tex`, don't uncomment the GitHub link.
10. **Keys in `.env` only**, `.env.example` committed empty. Never log a key.

## Environment (this machine: arm64 macOS, 11 cores, 18 GB)

`python3` on the PATH is **3.8.10 and unusable here**. Use `uv` (0.12 installed):

```bash
uv venv --python 3.12
source .venv/bin/activate
uv pip install -e ".[dev]"
```

Docker 28.0.1 + compose v2.33 are installed. Note two arm64 realities:

- **Pin task images by digest and pull them once**, for `linux/arm64`. If a task image is amd64-only it
  runs under emulation, which is slow and makes timeouts meaningless — either find an arm64 image or
  record the platform in the run manifest and raise that task's timeout deliberately.
- Container memory comes out of Docker Desktop's VM allocation, not the full 18 GB. With 512 MB per
  sandbox, keep concurrency modest (≤ 4) and check Docker Desktop's assigned memory before a full sweep.

`.env` keys: `OPENROUTER_API_KEY` (required). Optional direct providers for comparison.

Web viewer (`web/`, M7): Node 22 / npm 10 installed.

## Ports — this project owns 7400–7499

Sandbox containers publish **no ports** (that's the point). Only the orchestrator binds.

| Port | Use |
| --- | --- |
| 7400 | `web/` run viewer dev server |
| 7401 | API (FastAPI) |
| 7402 | Postgres, run store (→ 5432) |

Never bind outside this block; never bind :3000, :8000, :5432.

## Commands

```bash
uvicorn shc.api.app:app --reload --port 7401
python -m shc.suite.validate                       # references pass, unsolvables fail
python -m shc.sandbox.reap                          # remove orphaned shc-* containers
python -m shc.run --models anthropic/claude-…,openai/… --tiers T0,T1,T2,T3 --seeds 3
python -m shc.metrics.report --run <run_id>
pytest -q
pytest -q -m containment                            # adversarial sandbox tests
```

`shc.sandbox.reap` should also run automatically at orchestrator start and exit.

## Conventions

- Python 3.12, full type hints, `mypy --strict` on `shc/sandbox`, `shc/parse`, `shc/grade`, `shc/metrics`.
  Ruff for lint + format.
- Pydantic v2 for `Failure`, `Attempt`, `TaskSpec`, `Verdict` and every LLM-facing schema.
- Prompts live in versioned files under `shc/prompts/` with ids recorded in each run manifest. An
  unrecorded prompt change makes two runs incomparable.
- Disk-cache LLM calls keyed by `sha256(model, prompt, params)` under `.cache/` (gitignored). Sweeps get
  re-run; don't re-bill them.
- Every task-scoped log line carries `run_id`, `task_id`, `attempt`, `model`.
- Tests: pytest. The containment suite is marked `containment` and must be green before any full sweep.
  Unit-test the traceback parser against committed fixture logs — that parser is load-bearing and silent
  when it degrades.
- Commits: imperative, ≤ 72 chars, scoped — `parse: extract expected/actual from pytest assertion diff`.
- Git identity is already set for this repo (`bravimpurohit1305@gmail.com`). Leave it.

## Definition of done, and when to stop

Milestones per `SPEC.md` §10. CI green on push; the nightly suite workflow lands in M7.

**Stop and ask the user** when:

- pass@1 comes out so high that the resolution-rate denominator is tiny (fewer than ~30 first-attempt
  failures). The fix is harder tasks, but which direction to take the suite is the user's call.
- The agent games the harness in a way tamper detection didn't anticipate. Report the mechanism.
- An OpenRouter sweep is about to cost more than a few tens of dollars.
- A `SPEC.md` requirement looks wrong, or you want a dependency it doesn't name.
- Anything would need to run outside a sandbox to work.

Report honestly, with denominators: "pass@1 61 % (82/134 tasks), 87 of 52 first-attempt failures resolved"
is nonsense a reader will catch — get the arithmetic right, quote the counts, and give the CI. A bare
"resolves 78 % of failures" is not a result.
