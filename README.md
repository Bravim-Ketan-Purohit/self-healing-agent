# Self-Healing Code-Generation Agent

Writes code, executes it in **per-run Docker sandboxes**, parses tracebacks back into the prompt loop,
and iterates until tests pass.

**Stack:** Python · Docker SDK · GitHub Actions · OpenRouter
**Resume target:** `Bravim_Purohit_AI_Engineer.tex` → Projects & Publications
**Role:** AI Engineer

---

## The claim this repo must prove

> Writes code, executes it in per-run Docker sandboxes, parses tracebacks back into the prompt loop, and
> iterates until tests pass — resolving **[XX]%** of generated-code failures autonomously across a
> graded task suite.

The load-bearing engineering here is **the sandbox, not the prompting.** Per `projects-ref.md`: study
the Docker implementation, not the prompts. The prompt loop is a hundred lines; the isolation,
resource limits, timeout handling, and output streaming are where the real work is — and they're what
distinguishes this from a toy.

## Benchmarks this repo owes the resume

| Metric | Resume placeholder | Measured | Method |
| --- | --- | --- | --- |
| Autonomous failure resolution | `[XX]%` | — | TBD |

Define precisely, because this number is easy to inflate by accident:

- **The graded task suite** — how many tasks, what difficulty spread, and **is it fixed before you
  start measuring?** Tuning the agent and the task set together produces a meaningless score.
- **"Resolved"** — all tests pass, on a **held-out** test file the agent never saw. If the agent can
  read the tests it is optimizing against, it will overfit to them, and the number is fiction.
- **Iteration cap** — resolution rate at 1, 3, 5 attempts. One number hides the curve, and the curve is
  the interesting result.
- **Model + cost** — which model via OpenRouter, and tokens/dollars per resolved task. Report per-model
  numbers if you test several.
- **Include unsolvable tasks.** A suite with no impossible tasks can't distinguish "gives up correctly"
  from "loops forever."

**Do not uncomment** the GitHub link at `Bravim_Purohit_AI_Engineer.tex:141` until this is filled and
the repo is public.

## Architecture

```
 task spec
    │
    ▼
 ┌────────────────── agent loop (bounded) ──────────────────┐
 │                                                          │
 │  generate ──► write to workspace ──► run in sandbox      │
 │      ▲                                     │             │
 │      │                                     ▼             │
 │      └──── structured failure ◄──── parse stdout/stderr   │
 │            (error type, file, line, message)             │
 │                                                          │
 └──────────────────────────┬───────────────────────────────┘
                            ▼
                     tests pass, or cap hit → give up honestly

 ┌─────────── sandbox (per run, disposable) ───────────────┐
 │ no network · cpu + memory caps · wall-clock timeout      │
 │ read-only base, writable workspace mount                 │
 │ non-root user · always torn down, even on crash          │
 └─────────────────────────────────────────────────────────┘
```

## Sandbox requirements

This runs LLM-generated code. Treat every generated program as hostile by default — not because the
model is malicious, but because a plausible-looking `rm -rf` or a runaway `while True` is one sampling
accident away.

- [ ] Network disabled by default (`network_mode=none`), enabled only by explicit opt-in
- [ ] Memory and CPU limits set on the container
- [ ] Wall-clock timeout with forced kill
- [ ] Non-root user inside the container
- [ ] No host bind mounts beyond the dedicated workspace directory
- [ ] Container removed on every exit path — success, failure, timeout, or crash of the orchestrator
- [ ] Output size capped, so a task printing infinitely can't exhaust host memory

## Traceback parsing is the differentiator

Feeding raw stderr back to the model is the naive version. The better version parses failures into
structure — error type, file, line, failing assertion, the relevant source span — and gives the model
exactly the context it needs. Build the naive version first, then measure whether structured parsing
actually improves resolution rate. That A/B **is** the interesting result of this project.

## Getting started

```bash
python -m venv .venv && source .venv/bin/activate   # needs Python 3.11+
pip install -r requirements.txt
cp .env.example .env                                # OPENROUTER_API_KEY
docker info                                         # daemon must be running
pytest -q
```

## Layout

```
agent/         generation loop, iteration control, stop conditions
sandbox/       Docker lifecycle, limits, teardown  ← the core of this repo
parsing/       traceback → structured failure
tasks/         graded task suite (trivial → unsolvable)
eval/          resolution-rate runner, per-iteration curves
docs/STUDY.md  notes from OpenHands and SWE-agent
```

## Status

Scaffold. See [ROADMAP.md](ROADMAP.md) and [docs/STUDY.md](docs/STUDY.md).
