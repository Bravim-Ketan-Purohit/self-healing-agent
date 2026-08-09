from solution import stable_sort_by_key


def test_sort_by_age():
    items = [{"name": "alice", "age": 30},
             {"name": "bob", "age": 25},
             {"name": "carol", "age": 35}]
    result = stable_sort_by_key(items, "age")
    assert result == [{"name": "bob", "age": 25},
                      {"name": "alice", "age": 30},
                      {"name": "carol", "age": 35}]


def test_sort_by_id():
    items = [{"id": 3}, {"id": 1}, {"id": 2}]
    assert stable_sort_by_key(items, "id") == [{"id": 1}, {"id": 2}, {"id": 3}]


def test_already_sorted():
    items = [{"v": 1}, {"v": 2}, {"v": 3}]
    assert stable_sort_by_key(items, "v") == [{"v": 1}, {"v": 2}, {"v": 3}]


def test_single_element():
    items = [{"x": 42}]
    assert stable_sort_by_key(items, "x") == [{"x": 42}]
