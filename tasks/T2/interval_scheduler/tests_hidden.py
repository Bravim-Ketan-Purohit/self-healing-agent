from solution import IntervalScheduler
import pytest


def test_no_overlapping_events_invariant():
    """Invariant: no two events can overlap in time."""
    s = IntervalScheduler()
    s.add_event(0, 5, "a")
    s.add_event(5, 10, "b")
    s.add_event(10, 15, "c")
    # All adjacent but non-overlapping: should work fine
    assert len(s) == 3
    # Even a single time point overlap should fail
    with pytest.raises(ValueError):
        s.add_event(4, 6, "overlap_ab")
    with pytest.raises(ValueError):
        s.add_event(9, 11, "overlap_bc")


def test_get_events_at_returns_at_most_one():
    """Invariant: since no overlaps, at most one event at any time point."""
    s = IntervalScheduler()
    s.add_event(0, 10, "long")
    s.add_event(10, 20, "after")
    for t in range(0, 10):
        events = s.get_events_at(t)
        assert len(events) <= 1
        assert events == ["long"]
    for t in range(10, 20):
        assert s.get_events_at(t) == ["after"]


def test_remove_frees_time_range():
    """Invariant: removing an event frees its time range for new events."""
    s = IntervalScheduler()
    s.add_event(5, 10, "original")
    s.remove_event("original")
    s.add_event(5, 10, "replacement")
    assert s.get_events_at(7) == ["replacement"]


def test_invalid_range_raises():
    """Invariant: start must be < end."""
    s = IntervalScheduler()
    with pytest.raises(ValueError):
        s.add_event(10, 10, "zero_length")
    with pytest.raises(ValueError):
        s.add_event(10, 5, "backwards")


def test_remove_nonexistent_raises():
    """Invariant: removing non-existent event raises KeyError."""
    s = IntervalScheduler()
    with pytest.raises(KeyError):
        s.remove_event("ghost")


def test_all_events_sorted_by_start():
    """Invariant: all_events returns events sorted by start time."""
    s = IntervalScheduler()
    s.add_event(20, 25, "c")
    s.add_event(5, 10, "a")
    s.add_event(12, 15, "b")
    events = s.all_events()
    assert events == [(5, 10, "a"), (12, 15, "b"), (20, 25, "c")]


def test_get_events_at_boundary_exclusive_end():
    """Invariant: events use half-open interval [start, end)."""
    s = IntervalScheduler()
    s.add_event(5, 10, "event")
    assert s.get_events_at(5) == ["event"]
    assert s.get_events_at(9) == ["event"]
    assert s.get_events_at(10) == []  # end is exclusive


def test_many_adjacent_events():
    """Invariant: many adjacent events never overlap."""
    s = IntervalScheduler()
    for i in range(100):
        s.add_event(i * 10, i * 10 + 10, f"event_{i}")
    assert len(s) == 100
    # Trying to insert in any gap should fail
    with pytest.raises(ValueError):
        s.add_event(5, 15, "overlap")
