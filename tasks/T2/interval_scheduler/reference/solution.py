import bisect


class IntervalScheduler:
    """Manages non-overlapping events with conflict detection."""

    def __init__(self):
        self._events = []  # sorted list of (start, end, name)
        self._names = {}  # name -> (start, end)

    def add_event(self, start: int, end: int, name: str) -> None:
        if start >= end:
            raise ValueError("start must be less than end")
        if self.has_conflict(start, end):
            raise ValueError(f"Event '{name}' overlaps with an existing event")
        entry = (start, end, name)
        idx = bisect.bisect_left(self._events, (start,))
        self._events.insert(idx, entry)
        self._names[name] = (start, end)

    def remove_event(self, name: str) -> None:
        if name not in self._names:
            raise KeyError(f"Event '{name}' not found")
        start, end = self._names.pop(name)
        self._events.remove((start, end, name))

    def get_events_at(self, time: int) -> list:
        result = []
        for start, end, name in self._events:
            if start <= time < end:
                result.append(name)
            elif start > time:
                break
        return result

    def has_conflict(self, start: int, end: int) -> bool:
        for ev_start, ev_end, _ in self._events:
            if ev_start < end and start < ev_end:
                return True
        return False

    def all_events(self) -> list:
        return list(self._events)

    def __len__(self) -> int:
        return len(self._events)
