from solution import ObservableList
import pytest


def test_insert_and_notify():
    log = []
    obs = ObservableList([1, 2, 3])
    obs.subscribe(lambda e: log.append(e))
    obs.insert(0, "x")
    assert obs.to_list() == ["x", 1, 2, 3]
    assert log == [("insert", 0, "x")]


def test_remove_and_notify():
    log = []
    obs = ObservableList(["a", "b", "c"])
    obs.subscribe(lambda e: log.append(e))
    obs.remove(1)
    assert obs.to_list() == ["a", "c"]
    assert log == [("remove", 1, "b")]


def test_set_and_notify():
    log = []
    obs = ObservableList([10, 20, 30])
    obs.subscribe(lambda e: log.append(e))
    obs.set(2, 99)
    assert obs.get(2) == 99
    assert log == [("set", 2, 99)]


def test_remove_out_of_range_raises():
    obs = ObservableList([1, 2])
    with pytest.raises(IndexError):
        obs.remove(5)
