# Study notes — Self-Healing Code-Generation Agent

Reference material, carried over from `projects-ref.md`.

## The instruction from `projects-ref.md`

> **Do not focus on their LLM prompts. Focus on their Docker implementation.**

Worth restating because the pull toward prompt-tweaking is strong and it is the low-value half of this
project. The prompts are replaceable in an afternoon. The sandbox is the engineering.

## References

### [`All-Hands-AI/OpenHands`](https://github.com/All-Hands-AI/OpenHands) (formerly OpenDevin)

**What to study:** the `runtime` / `sandbox` directory. Specifically how they use the Docker SDK to:

1. Spin up an isolated container
2. Run the LLM's generated code inside it
3. Pipe terminal output back to the Python process safely

Pay attention to the container **lifecycle** — creation, reuse across steps, and teardown. Note whether
they keep one container alive across an episode or create one per action, and what that trades off
(startup latency vs. state leaking between steps). That's a real design decision this repo has to make
too.

Also look at how they stream output while a process is still running, rather than waiting for exit.
Blocking until exit means an infinite loop gives you nothing to act on.

### [`princeton-nlp/SWE-agent`](https://github.com/princeton-nlp/SWE-agent)

**What to study:** their environment abstraction and how they define the action space the agent can
take. Also their evaluation setup — SWE-bench is the reference for *how to score a coding agent
honestly*, and the design decision to keep tests hidden from the agent is exactly the discipline the
task suite here needs.

## Also worth reading

- **Docker resource-constraint docs** — `--memory`, `--cpus`, `--pids-limit`, `--network none`. These
  flags are the actual security boundary; know what each one does and doesn't prevent.
- **SWE-bench** methodology — particularly how they avoid test leakage. The failure mode where an agent
  reads the tests it's graded on is the single easiest way to produce a fake number.

## Questions to answer before coding

1. One container per run, or one reused across iterations? What leaks in the reuse case?
2. How is output streamed from a process that never exits?
3. What guarantees teardown when the *orchestrator* crashes, not the container?
4. Does a Docker container actually contain hostile code, or does it need gVisor / a VM? What's the
   honest answer, and what threat model is this repo assuming?
5. If the agent can see the tests, what stops it from special-casing them instead of fixing the bug?
6. What distinguishes "correctly gave up" from "silently failed" in the metrics?

## Deliberate divergences from the references

| Area | OpenHands / SWE-agent does | This repo does | Why |
| --- | --- | --- | --- |
| | | | |
