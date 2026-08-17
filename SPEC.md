# SPEC — Self-Healing Code-Generation Agent

**Authoritative technical specification.** `ROADMAP.md` gives the order; this gives the contents. Where
they disagree, this wins. If a requirement here looks wrong, say so and stop.

---

## 1. The claim

> Writes code, executes it in per-run Docker sandboxes, parses tracebacks back into the prompt loop, and
> iterates until tests pass — **resolving [XX]% of generated-code failures autonomously** across a graded
> task suite.

Resume stack string the build must match: *Python, Docker SDK, GitHub Actions, OpenRouter*
(`Bravim_Purohit_AI_Engineer.tex:138`).

### What the number actually means

`[XX]%` is **not** pass rate. Read the bullet literally: the denominator is *failures*, not tasks.

```
resolution_rate = tasks that failed on attempt 1 but passed by attempt N
                  ─────────────────────────────────────────────────────
                          tasks that failed on attempt 1
```

So the harness must record two distinct results per task: **pass@1** (single attempt, no repair — the
baseline) and **pass@N with repair**. The headline number is the recovery rate between them. A system with
a 95 % pass@1 has almost no failures to resolve and a noisy resolution rate; report both numbers and the
raw counts (`87 of 134 first-attempt failures resolved`) so nobody has to guess the denominator.

## 2. Non-goals

- Not an IDE plugin, not a PR-opening bot, not an SWE-bench leaderboard entry.
- No multi-file repository-scale refactoring. Task scope is one module plus its tests.
- **Amended 2026-08-17:** fine-tuning is now in scope as an M8 capstone, but *only* on repair traces this
  system generated itself — never on a public code dataset. See §12.
- No agent-controlled network access by default (see §4 — this is a security boundary, not a limitation).
- No human-in-the-loop. "Autonomously" is in the bullet; if a human intervenes, the run doesn't count.

## 3. The graded task suite

The benchmark is the product here. If the suite is easy or self-serving, the number is worthless.

### Tiers

| Tier | Description | Purpose |
| --- | --- | --- |
| T0 trivial | string/list manipulation, one function | smoke test; near-100 % pass@1 expected |
| T1 standard | algorithmic with edge cases (parsing, dates, ranges) | the bulk of measurable failures |
| T2 stateful | class with invariants, multi-method interaction | tests reasoning across calls |
| T3 subtle | off-by-one, float precision, mutation aliasing, encoding | where traceback-driven repair should shine |
| T4 integration | two modules that must agree on a contract | multi-file coordination |
| T5 **unsolvable** | contradictory or impossible requirements | measures *overclaiming*, not skill |

T5 is the tier that makes the suite credible. An agent that "solves" a contradictory spec has hallucinated
a success, and the false-success rate on T5 is a headline metric in its own right. Report it next to the
resolution rate.

### Anti-gaming requirements — non-negotiable

An agent that can see the tests it's graded on will special-case them, and every naive harness measures
that instead of competence.

1. **Held-out tests.** The agent sees `tests_visible.py`. Grading runs `tests_hidden.py`, which the agent
   never sees and which lives outside the sandbox's copied working tree.
2. **Test tampering is a failed task.** Hash every visible test file before and after each attempt. A
   modified test file, a deleted test, an added `@pytest.mark.skip`, or a `conftest.py` that monkeypatches
   assertions ⇒ task recorded as `TAMPERED`, not passed. Log the diff.
3. **Cheat-pattern detection.** Static scan of submitted code for: bare `except: pass` around the whole
   body, hardcoded returns matching visible test expectations, `sys.exit(0)`, writes to the test directory,
   `os.environ` manipulation of pytest behaviour. Flag, don't silently fail — a flagged-but-passing task
   is reported separately.
4. **No network in the sandbox** by default, so a task can't be solved by fetching the answer.

Every task is a directory:

```
tasks/T3/float_accumulate/
  task.yaml          id, tier, prompt, entrypoint, timeout, deps, solvable: true|false
  prompt.md          what the agent is told
  starter/           files the agent starts from (may be empty)
  tests_visible.py   agent can read and run these
  tests_hidden.py    grading only — never enters the sandbox with the agent
  reference/         a known-good solution (for suite validation, never shown to the agent)
```

**Validate the suite before trusting it:** every `solvable: true` task must pass with its reference
solution, and every `solvable: false` task must fail with any solution. That's a CI job.

## 4. Sandbox — the security surface

This repo runs LLM-generated code on the developer's machine. Treat that as the threat model it is.

Per-run container, created and destroyed for each attempt:

```python
container = client.containers.create(
    image=task.image,                      # pinned digest, not :latest
    command=["/bin/sh", "-c", run_script],
    network_mode="none",                   # default; opt-in per task, never global
    mem_limit="512m", memswap_limit="512m",
    nano_cpus=1_000_000_000,               # 1 CPU
    pids_limit=128,
    user="10001:10001",                    # non-root
    read_only=True,                        # rootfs read-only
    tmpfs={"/tmp": "size=64m,mode=1777", "/work": "size=128m,mode=0755"},
    cap_drop=["ALL"],
    security_opt=["no-new-privileges:true"],
    ulimits=[docker.types.Ulimit(name="fsize", soft=64<<20, hard=64<<20),
             docker.types.Ulimit(name="nofile", soft=256, hard=256)],
    labels={"shc.run_id": run_id, "shc.task": task.id},
    name=f"shc-{run_id[:8]}-{task.id}-{attempt}",
)
```

Hard requirements:

- **Code is copied in, never bind-mounted.** `put_archive` a tar of the working tree into `/work`. A bind
  mount of a host path is a write primitive into the host filesystem; there is no version of that which is
  acceptable here.
- **No host env passthrough.** The container gets an explicit allow-list of environment variables. API keys
  never enter the sandbox — the agent's LLM calls happen in the orchestrator, not in the container.
- **Guaranteed teardown.** `try/finally` with `container.remove(force=True)`, plus a wall-clock watchdog
  that kills a container past its timeout, plus a **reaper** at startup and shutdown that removes any
  container carrying the `shc.run_id` label. A crashed orchestrator must not leave containers running.
- **Container names namespaced** with `shc-` and the run id — seven sibling projects share this Docker
  daemon and a name collision must be impossible.
- **Output caps.** Truncate captured stdout/stderr at a fixed byte limit (e.g. 256 KB) with a marker. An
  infinite print loop must not exhaust host memory or the LLM context.
- **Images pinned by digest** and pre-pulled. A build step that downloads packages at attempt time makes
  runs non-reproducible and non-deterministic in duration.

The README should say plainly that this is a *hardened developer sandbox*, not a multi-tenant one — no
gVisor/Firecracker, so a kernel escape is out of scope. Overclaiming isolation is worse than scoping it.

## 5. The repair loop

```
   generate ──► sandbox run ──► capture ──► classify ──► repair prompt ──► generate ──► …
                                    │
                                    └─► pass ⇒ verify against hidden tests ⇒ done
```

### Failure classification

Parsing tracebacks *into structure* is the core mechanic named in the bullet, so it can't be a regex
grabbing the last line. Produce a typed record:

```python
class Failure(BaseModel):
    kind: Literal["syntax","import","assertion","exception","timeout","oom","tamper","no_output"]
    exc_type: str | None
    message: str
    file: str | None
    line: int | None
    frames: list[Frame]              # parsed traceback frames, project frames marked
    failing_tests: list[str]         # node ids
    expected: str | None             # extracted from pytest assertion diff when present
    actual: str | None
    signature: str                   # stable hash for no-progress detection
```

The repair prompt gets the structured failure, the relevant source lines around the failing frame, and the
diff from the previous attempt — not a raw log dump. Context budget is finite and a 40 KB pytest log spends
it all on noise.

### Stop conditions

- Visible tests pass → run hidden tests → record final verdict.
- `max_attempts` reached (default 5, configurable per tier).
- **No-progress detection:** identical `Failure.signature` twice in a row ⇒ escalate strategy once (e.g.
  instruct a different approach, or raise reasoning effort), then abort. Looping on the same error five
  times burns tokens and inflates nothing.
- Cost ceiling per task exceeded.

### Recorded per attempt

Attempt number, model, prompt tokens, completion tokens, cost, wall time, the full submitted diff, the
classified failure, and the sandbox exit code. This is what the run viewer renders and what makes the
resolution number auditable.

## 6. Module layout

```
shc/
  suite/        task loading, validation, tier definitions, hashing
  sandbox/      docker lifecycle, tar transfer, limits, reaper, output capture
  parse/        traceback + pytest output → Failure
  agent/        generate / repair prompts, loop control, no-progress detection
  llm/          OpenRouter adapter, multi-model routing, disk cache, cost accounting
  grade/        hidden-test execution, tamper + cheat detection, verdicts
  metrics/      pass@1, pass@N, resolution rate, false-success, per-tier breakdown
  api/          FastAPI: runs, tasks, attempts, leaderboard
tasks/          the graded suite, by tier
runs/           committed result JSON — the source of every resume number
web/            run viewer (Vite + React + TS)
.github/workflows/  nightly suite run
```

## 7. API

```
POST /api/runs        {models[], tiers[], max_attempts, seed} → {run_id}
GET  /api/runs/{id}   → progress, per-task verdicts, aggregate metrics
GET  /api/runs/{id}/tasks/{task_id} → attempt timeline: diff, failure, patch, test output per attempt
GET  /api/leaderboard → per-model pass@1, pass@N, resolution rate, false-success rate, cost/task
GET  /api/tasks       → the suite with tiers and solvability
GET  /api/events/{run_id} → SSE progress for the live view
```

## 8. Run viewer (`web/`)

Vite + React + TypeScript + Tailwind.

1. **Runs.** List with model set, date, aggregate metrics.
2. **Run detail.** Task grid coloured by verdict (passed@1 / resolved / unresolved / tampered / false
   success on T5), grouped by tier.
3. **Task timeline** — the important screen. Per attempt: the diff the model produced, the structured
   failure it got back, the repair prompt's failure summary, and the next diff. A reader should be able to
   watch a bug get fixed across three attempts.
4. **Leaderboard.** Per-model comparison across OpenRouter models, with cost per resolved failure — the
   number a hiring engineer will find genuinely interesting.

M6 work. No engine code imports from `web/`.

## 9. Measurement protocol

- ≥ 60 tasks across T0–T5, with T5 at least 8 tasks (false-success needs a real denominator).
- ≥ 3 seeds per model; temperature fixed and recorded.
- Report per model **and** aggregate: pass@1, pass@N, resolution rate with raw counts, false-success rate
  on T5, tamper count, mean attempts-to-resolution, cost per resolved failure, per-tier breakdown.
- Wilson or bootstrap 95 % CI on the resolution rate. With 134 failures a point estimate has a ±8 pt
  interval, and quoting a bare figure implies precision the sample size doesn't support.
- **Contamination note.** If any task is adapted from HumanEval/MBPP/public exercises, say so in the suite
  manifest. Optionally run HumanEval+ or MBPP+ as an external anchor, clearly labelled as
  possibly-contaminated and reported separately from the first-party suite.
- Suite validation (references pass, unsolvables fail) must be green in the same CI run.

Commit the full run JSON. Fill the README Benchmarks table from a specific committed file and name it.

## 10. Milestone acceptance criteria

- **M1 Sandbox.** Container lifecycle with all limits from §4; reaper works; a deliberately hostile task
  (`while True: fork()`, 10 GB allocation, `rm -rf /`, network call) is contained and torn down. **Write
  these adversarial tests first** — they are the ones that protect the developer's machine.
- **M2 Suite v1.** ≥ 20 tasks across T0–T3 with visible/hidden split; suite validation job green.
- **M3 Single-shot baseline.** Generate → run → grade, no repair. pass@1 recorded per model. This is the
  baseline the headline number is measured against.
- **M4 Repair loop.** Structured `Failure` parsing, repair prompting, no-progress detection, cost ceiling.
  Attempt history persisted.
- **M5 Anti-gaming.** Tamper detection, cheat-pattern scan, T5 tasks with false-success reporting.
- **M6 Measurement.** Full suite ≥ 60 tasks, ≥ 3 seeds, ≥ 3 models; committed run JSON; **README
  Benchmarks table filled**; CIs reported.
- **M7 Presentable.** Run viewer, nightly GitHub Actions run, README diagram accurate, CI green.

## 11. Honest-claims register

| Claim | Status | Backed by |
| --- | --- | --- |
| writes code | ☐ | generation path with committed diffs per attempt |
| per-run Docker sandboxes | ☐ | §4 limits enforced; adversarial containment tests pass |
| parses tracebacks back into the prompt loop | ☐ | typed `Failure` records; repair prompts show structured input |
| iterates until tests pass | ☐ | attempt timelines with stop conditions and no-progress aborts |
| resolves `[XX]%` of failures autonomously | ☐ | `runs/…json`: pass@1 and pass@N with raw counts + CI |
| graded task suite | ☐ | ≥ 60 tasks, T0–T5, hidden tests, validation job green |
| genuinely autonomous | ☐ | no human intervention in any counted run |
| not gamed | ☐ | tamper count reported; T5 false-success rate reported |

Any unchecked row ⇒ `Bravim_Purohit_AI_Engineer.tex:141` stays commented and `[XX]` stays bracketed.

---

## 12. Extended stack (added 2026-08-17)

### 12.1 Fine-tuning on the agent's own repair traces — the capstone

This reverses the original non-goal, and it's worth it, because the training data is a **by-product this
project already produces**. Every resolved task is a triple: broken code, structured failure, working fix.
After a full sweep you have hundreds of them, generated and *verified by the hidden tests* — labels that
are correct by construction rather than by annotation.

So the M8 experiment is:

1. **Mine the corpus.** Export `(context, structured_failure, successful_patch)` from every resolved
   attempt in committed runs. Deduplicate by task and by near-identical diff.
2. **Split by task, never by example.** Tasks in the training set must not appear in the eval set in any
   form. Splitting by example leaks — two attempts on the same task land on both sides, and the result is
   meaningless.
3. **Fine-tune a small open model** — PyTorch + HF `transformers`, **QLoRA** via `peft` + `bitsandbytes`,
   4-bit base. A small model is the right target: the interesting claim is "a 7B specialist matches a
   frontier model at repair for a fraction of the cost", not "a bigger model is better".
4. **Evaluate as a first-class arm.** Run the same graded suite, same seeds, same anti-gaming checks.
   Report resolution rate, cost per resolved failure, and latency against the prompted frontier baseline.
5. **Report the negative result if that's what happens.** A fine-tune that fails to beat prompting is a
   legitimate, publishable finding — and a candidate who can say "it didn't work, here's why" is more
   credible than one whose every experiment succeeded.

Contamination check: the base model may already have seen tasks resembling your suite. Note it in the
manifest, and lean on the T5 unsolvable tier and held-out hidden tests, which are yours alone.

GPU requirement: a QLoRA fine-tune of a small model is a few hours on one rented instance. Same
infrastructure pattern as the sibling gateway project — provision, train, evaluate, destroy.

### 12.2 DSPy for the repair prompt

The repair prompt is the highest-leverage string in the project. Compile it with DSPy against the **dev
tier subset only**, and report the resolution-rate delta on the held-out tiers. Same discipline as the
fine-tune: optimise on dev, report on test, commit the compiled artefact with the optimiser and metric
recorded.

DSPy and the fine-tune are also a genuinely interesting comparison — prompt optimisation versus weight
adaptation on the same task, with cost per resolved failure as the shared axis.

### 12.3 Braintrust + LangSmith

- **Braintrust** — eval run tracking, the per-model leaderboard, and regression detection across sweeps.
  It replaces hand-rolled result comparison and gives permanent links you can show someone.
- **LangSmith** — trace the generate → run → classify → repair loop, so a single task's full history is one
  inspectable trace.

Both are instrumentation, not measurement. `runs/*.json` in this repo remains the source of truth for every
resume number; a dashboard is a view of it.

### 12.4 OpenTelemetry

Spans: `generate`, `sandbox_create`, `sandbox_exec`, `parse_failure`, `grade`, `repair`, plus one parent
span per task and one per run. Attributes: model, tier, attempt number, failure kind, tokens, cost, exit
code, container id. Sandbox containers stay unin­strumented — no network, and no agent-controlled code
should be emitting telemetry.

The most useful thing this buys: a flamegraph of a run showing where wall-clock actually goes. It is almost
always container startup and test execution rather than inference, which is a counter-intuitive and very
tellable finding.

## 13. Additional milestones

- **M8 Fine-tune.** Trace corpus exported with task-level splits; QLoRA fine-tune of a small model;
  evaluated as a full arm on the graded suite; resolution rate, cost per resolved failure, and latency
  reported against the prompted baseline; negative result reported if that's the outcome.
- **M9 Prompt optimisation.** DSPy-compiled repair prompt, dev-tier only, delta reported on held-out tiers;
  compiled artefact committed. DSPy vs fine-tune comparison written up.
- **M10 Observability.** OTel end to end; Braintrust leaderboard live; LangSmith traces linked from the run
  viewer.

### Honest-claims additions

| Claim | Status | Backed by |
| --- | --- | --- |
| fine-tuned on self-generated traces | ☐ | corpus export, task-level split, no example leakage |
| specialist model competitive with frontier | ☐ | same suite, same seeds, cost per resolved failure |
| prompt optimisation measured, not assumed | ☐ | DSPy compiled on dev tiers, delta on held-out tiers |
| no train/test leakage | ☐ | split by task; contamination noted in the manifest |
