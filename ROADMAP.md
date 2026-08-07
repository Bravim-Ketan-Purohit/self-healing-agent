# Roadmap — Self-Healing Code-Generation Agent

Sandbox first, agent second. An agent without isolation is a liability running on your laptop, and the
isolation is also the part worth talking about in an interview.

## M1 — Sandbox, standalone

Buildable and testable with no LLM involved at all.

- [ ] Docker SDK wrapper: create → run → capture stdout/stderr/exit code → destroy
- [ ] Resource limits: memory cap, CPU quota, wall-clock timeout with forced kill
- [ ] `network_mode=none` by default
- [ ] Non-root user inside the container
- [ ] Workspace mount, nothing else from the host
- [ ] Output size cap
- [ ] **Adversarial tests** — hand-written hostile programs, no LLM:
  - [ ] infinite loop → killed by timeout
  - [ ] memory bomb → OOM-killed, host unaffected
  - [ ] fork bomb → contained
  - [ ] network call → fails
  - [ ] attempt to write outside the workspace → denied
  - [ ] orchestrator killed mid-run → container still cleaned up

## M2 — Task suite, frozen before measurement

- [ ] Task format: spec, starter files, hidden test file
- [ ] **Tests hidden from the agent** — resolution is measured on tests it never saw
- [ ] Difficulty spread: trivial → moderate → hard → **intentionally unsolvable**
- [ ] Freeze the suite and commit it before tuning anything

## M3 — Naive loop, measured

- [ ] Generate → write → run → feed raw stderr back → retry
- [ ] Bounded iterations with an explicit give-up
- [ ] Resolution-rate runner reporting at 1 / 3 / 5 iterations
- [ ] **Record this as the baseline.** Structured parsing is judged against it

## M4 — Structured traceback parsing

- [ ] Parse into error type, file, line, failing assertion, relevant source span
- [ ] Feed structured context instead of raw text
- [ ] Re-run the suite; **A/B against M3's baseline**
- [ ] Report the honest answer — including "structured parsing didn't help much," if that's the result

## M5 — Loop quality

- [ ] Detect repeated identical failures and stop instead of burning iterations
- [ ] Track cost per task and per resolved task
- [ ] Verify the agent gives up correctly on unsolvable tasks rather than looping
- [ ] Optional: compare 2–3 models via OpenRouter, report per-model resolution and cost

## M6 — Fill in the number

- [ ] Final run over the frozen suite
- [ ] **Fill the Benchmarks table**: resolution rate, iteration curve, model, cost per resolved task
- [ ] Publish the task suite so the number is reproducible

## M7 — Presentable

- [ ] README sandbox-requirements checklist fully ticked, with tests backing each line
- [ ] GitHub Actions CI running the sandbox tests
- [ ] Flip repo public, then uncomment `Bravim_Purohit_AI_Engineer.tex:141`

## Gate before the resume link goes live

`[XX]%` measured on held-out tests · every adversarial sandbox test in M1 passing · task suite frozen
before measurement and published · iteration curve reported, not just a single headline number.
