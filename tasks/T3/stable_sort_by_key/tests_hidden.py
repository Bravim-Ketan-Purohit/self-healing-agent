from solution import stable_sort_by_key


def test_stability_preserved():
    """Items with equal keys must retain their original relative order."""
    items = [{"name": "alice", "age": 30},
             {"name": "bob", "age": 25},
             {"name": "carol", "age": 30},
             {"name": "dave", "age": 25}]
    result = stable_sort_by_key(items, "age")
    # bob before dave (both age 25), alice before carol (both age 30)
    assert result == [{"name": "bob", "age": 25},
                      {"name": "dave", "age": 25},
                      {"name": "alice", "age": 30},
                      {"name": "carol", "age": 30}]


def test_stability_many_duplicates():
    """All items have same key value — order must be completely preserved."""
    items = [{"id": i, "score": 5} for i in range(10)]
    result = stable_sort_by_key(items, "score")
    assert result == items


def test_no_mutation():
    """Original list must not be mutated."""
    items = [{"v": 3}, {"v": 1}, {"v": 2}]
    original = [d.copy() for d in items]
    stable_sort_by_key(items, "v")
    assert items == original


def test_reverse_order_stability():
    """Reverse-sorted input with ties."""
    items = [{"name": "e", "priority": 3},
             {"name": "d", "priority": 3},
             {"name": "c", "priority": 2},
             {"name": "b", "priority": 1},
             {"name": "a", "priority": 1}]
    result = stable_sort_by_key(items, "priority")
    assert result == [{"name": "b", "priority": 1},
                      {"name": "a", "priority": 1},
                      {"name": "c", "priority": 2},
                      {"name": "e", "priority": 3},
                      {"name": "d", "priority": 3}]


def test_string_key_stability():
    """Sorting by string key, stability on ties."""
    items = [{"word": "banana", "len": 6},
             {"word": "cherry", "len": 6},
             {"word": "apple", "len": 5},
             {"word": "grape", "len": 5}]
    result = stable_sort_by_key(items, "len")
    assert result == [{"word": "apple", "len": 5},
                      {"word": "grape", "len": 5},
                      {"word": "banana", "len": 6},
                      {"word": "cherry", "len": 6}]


def test_large_list_stability():
    """Larger list where stability matters."""
    import random
    random.seed(42)
    items = [{"idx": i, "group": random.choice([1, 2, 3])} for i in range(100)]
    result = stable_sort_by_key(items, "group")
    # Within each group, idx values must be in ascending order (original order)
    for group in [1, 2, 3]:
        group_items = [d for d in result if d["group"] == group]
        idxs = [d["idx"] for d in group_items]
        assert idxs == sorted(idxs)
