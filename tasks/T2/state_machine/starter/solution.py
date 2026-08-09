class InvalidTransitionError(Exception):
    """Raised when an invalid transition is attempted."""
    pass


class StateMachine:
    """Finite state machine with defined states and transitions."""

    def __init__(self, initial_state: str):
        pass

    @property
    def current_state(self) -> str:
        pass

    def add_transition(self, from_state: str, event: str, to_state: str) -> None:
        pass

    def advance(self, event: str) -> str:
        pass

    def reset(self) -> None:
        pass

    def get_valid_events(self) -> list:
        pass
