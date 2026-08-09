class InvalidTransitionError(Exception):
    """Raised when an invalid transition is attempted."""
    pass


class StateMachine:
    """Finite state machine with defined states and transitions."""

    def __init__(self, initial_state: str):
        self._initial_state = initial_state
        self._current_state = initial_state
        self._transitions = {}  # (from_state, event) -> to_state

    @property
    def current_state(self) -> str:
        return self._current_state

    def add_transition(self, from_state: str, event: str, to_state: str) -> None:
        key = (from_state, event)
        if key in self._transitions:
            raise ValueError(
                f"Transition already defined for ({from_state}, {event})"
            )
        self._transitions[key] = to_state

    def advance(self, event: str) -> str:
        key = (self._current_state, event)
        if key not in self._transitions:
            raise InvalidTransitionError(
                f"No transition from '{self._current_state}' on event '{event}'"
            )
        self._current_state = self._transitions[key]
        return self._current_state

    def reset(self) -> None:
        self._current_state = self._initial_state

    def get_valid_events(self) -> list:
        events = []
        for (state, event) in self._transitions:
            if state == self._current_state:
                events.append(event)
        return sorted(events)
