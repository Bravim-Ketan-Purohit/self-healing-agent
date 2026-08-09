from solution import ObservableList
import pytest


def test_callbacks_receive_correct_indices_after_insert():
    """Invariant: callbacks receive the correct insertion index."""
    log = []
    obs = ObservableList(["a", "b", "c"])
    obs.subscribe(lambda e: log.append(e))
    obs.insert(1, "x")
    obs.insert(0, "y")
    assert log == [("insert", 1, "x"), ("insert", 0, "y")]
    assert obs.to_list() == ["y", "a", "x", "b", "c"]


def test_callbacks_receive_correct_removed_item():
    """Invariant: remove notification includes the actual removed item."""
    log = []
    obs = ObservableList([10, 20, 30, 40])
    obs.subscribe(lambda e: log.append(e))
    obs.remove(2)
    assert log[-1] == ("remove", 2, 30)
    obs.remove(0)
    assert log[-1] == ("remove", 0, 10)


def test_unsubscribe_stops_notifications():
    """Invariant: unsubscribed callback never receives further events."""
    log1 = []
    log2 = []
    cb1 = lambda e: log1.append(e)
    cb2 = lambda e: log2.append(e)
    obs = ObservableList()
    obs.subscribe(cb1)
    obs.subscribe(cb2)
    obs.insert(0, "a")
    obs.unsubscribe(cb1)
    obs.insert(1, "b")
    assert len(log1) == 1  # only "a" event
    assert len(log2) == 2  # both events


def test_unsubscribe_nonexistent_raises():
    """Invariant: unsubscribe of non-registered callback raises ValueError."""
    obs = ObservableList()
    with pytest.raises(ValueError):
        obs.unsubscribe(lambda e: None)


def test_set_out_of_range_raises():
    """Invariant: set at invalid index raises IndexError."""
    obs = ObservableList([1, 2, 3])
    with pytest.raises(IndexError):
        obs.set(5, "x")
    with pytest.raises(IndexError):
        obs.set(-1, "x")


def test_multiple_subscribers_all_notified():
    """Invariant: all subscribers receive every event."""
    logs = [[] for _ in range(5)]
    obs = ObservableList()
    for log in logs:
        obs.subscribe(lambda e, l=log: l.append(e))
    obs.insert(0, "item")
    for log in logs:
        assert log == [("insert", 0, "item")]


def test_insert_at_end_uses_correct_index():
    """Invariant: insert beyond length appends and reports correct clamped index."""
    log = []
    obs = ObservableList(["a", "b"])
    obs.subscribe(lambda e: log.append(e))
    obs.insert(100, "z")  # should clamp to index 2
    assert obs.to_list() == ["a", "b", "z"]
    assert log == [("insert", 2, "z")]


def test_sequential_operations_consistent_state():
    """Invariant: after a sequence of ops, internal state and notifications are consistent."""
    log = []
    obs = ObservableList()
    obs.subscribe(lambda e: log.append(e))
    obs.insert(0, "a")
    obs.insert(1, "b")
    obs.insert(2, "c")
    obs.set(1, "B")
    obs.remove(0)
    assert obs.to_list() == ["B", "c"]
    assert len(log) == 5
    assert log[3] == ("set", 1, "B")
    assert log[4] == ("remove", 0, "a")
