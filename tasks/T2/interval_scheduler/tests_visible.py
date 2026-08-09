from solution import IntervalScheduler
import pytest


def test_add_and_get_events():
    s = IntervalScheduler()
    s.add_event(9, 10, "standup")
    s.add_event(10, 12, "coding")
    assert s.get_events_at(9) == ["standup"]
    assert s.get_events_at(10) == ["coding"]


def test_overlap_raises():
    s = IntervalScheduler()
    s.add_event(5, 10, "meeting")
    with pytest.raises(ValueError):
        s.add_event(8, 12, "conflict")


def test_has_conflict():
    s = IntervalScheduler()
    s.add_event(10, 12, "coding")
    assert s.has_conflict(11, 13) is True
    assert s.has_conflict(12, 14) is False


def test_remove_event():
    s = IntervalScheduler()
    s.add_event(9, 10, "standup")
    s.remove_event("standup")
    assert len(s) == 0
    assert s.has_conflict(9, 10) is False
