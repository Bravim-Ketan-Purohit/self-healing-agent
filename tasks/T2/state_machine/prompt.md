# State Machine

Implement a `StateMachine` class that defines states and transitions, then processes events:

- `__init__(self, initial_state: str)` — Create a state machine with the given initial state.
- `add_transition(self, from_state: str, event: str, to_state: str) -> None` — Define a transition: when in `from_state` and `event` occurs, move to `to_state`. Raises `ValueError` if a transition for the same (from_state, event) pair already exists.
- `advance(self, event: str) -> str` — Process an event and return the new state. Raises `InvalidTransitionError` if no transition is defined for the current state and event.
- `current_state` — Property that returns the current state.
- `reset(self) -> None` — Reset the machine to the initial state.
- `get_valid_events(self) -> list[str]` — Return a sorted list of events valid from the current state.

You must also define `InvalidTransitionError` as a custom exception inheriting from `Exception`.

## Invariants

- An invalid transition (no rule for current state + event) always raises `InvalidTransitionError`.
- After an invalid transition attempt, the state is unchanged.
- `current_state` always reflects the last successful transition.

## Examples

```python
sm = StateMachine("idle")
sm.add_transition("idle", "start", "running")
sm.add_transition("running", "stop", "idle")
sm.add_transition("running", "pause", "paused")
sm.add_transition("paused", "resume", "running")

sm.advance("start")       # returns "running"
sm.current_state          # "running"
sm.advance("pause")       # returns "paused"
sm.advance("start")       # raises InvalidTransitionError
sm.current_state          # still "paused"
```
