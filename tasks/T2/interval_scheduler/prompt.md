# Interval Scheduler

Implement an `IntervalScheduler` class that manages non-overlapping events:

- `__init__(self)` — Create an empty scheduler.
- `add_event(self, start: int, end: int, name: str) -> None` — Add an event with a time range [start, end). Raises `ValueError` if start >= end. Raises `ValueError` if the event overlaps with an existing event.
- `remove_event(self, name: str) -> None` — Remove an event by name. Raises `KeyError` if event not found.
- `get_events_at(self, time: int) -> list[str]` — Return a list of event names that contain the given time point (start <= time < end).
- `has_conflict(self, start: int, end: int) -> bool` — Return True if the given range would overlap with any existing event.
- `all_events(self) -> list[tuple[int, int, str]]` — Return all events as (start, end, name) tuples sorted by start time.
- `__len__(self) -> int` — Return the number of scheduled events.

## Invariants

- No two events may overlap (share any common time point).
- After `remove_event`, the removed event's time range is freed.
- `get_events_at` returns at most one event for any time point (since no overlaps).

## Examples

```python
s = IntervalScheduler()
s.add_event(9, 10, "standup")
s.add_event(10, 12, "coding")
s.add_event(9, 11, "conflict")  # raises ValueError (overlaps with standup and coding)
s.get_events_at(9)   # ["standup"]
s.get_events_at(10)  # ["coding"]
s.has_conflict(11, 13)  # True (overlaps with coding [10,12))
s.has_conflict(12, 14)  # False
```
