class IntervalScheduler:
    """Manages non-overlapping events with conflict detection."""

    def __init__(self):
        pass

    def add_event(self, start: int, end: int, name: str) -> None:
        pass

    def remove_event(self, name: str) -> None:
        pass

    def get_events_at(self, time: int) -> list:
        pass

    def has_conflict(self, start: int, end: int) -> bool:
        pass

    def all_events(self) -> list:
        pass

    def __len__(self) -> int:
        pass
