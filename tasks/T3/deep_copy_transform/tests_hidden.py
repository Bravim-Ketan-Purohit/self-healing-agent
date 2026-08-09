import copy
from solution import transform


def test_original_not_mutated_flat():
    """Original top-level dict must not change."""
    data = {"a": 1, "b": 2}
    original = copy.deepcopy(data)
    transform(data, "a", lambda x: x * 100)
    assert data == original


def test_original_not_mutated_nested():
    """Original nested dict must not change."""
    data = {"a": 1, "nested": {"a": 2, "b": {"a": 3}}}
    original = copy.deepcopy(data)
    transform(data, "a", lambda x: x + 100)
    assert data == original


def test_deep_nesting():
    """Three levels deep transform."""
    data = {"lvl1": {"lvl2": {"target": 5, "other": 9}, "target": 3}, "target": 1}
    result = transform(data, "target", lambda x: x * 2)
    assert result["target"] == 2
    assert result["lvl1"]["target"] == 6
    assert result["lvl1"]["lvl2"]["target"] == 10
    assert result["lvl1"]["lvl2"]["other"] == 9


def test_no_shared_references():
    """Returned dict must not share any mutable objects with original."""
    inner = {"val": [1, 2, 3]}
    data = {"a": inner, "b": {"a": inner}}
    result = transform(data, "x", lambda x: x)  # no key matches
    # Mutating result's list should not affect original
    if isinstance(result.get("a"), dict) and "val" in result["a"]:
        result["a"]["val"].append(99)
    assert inner["val"] == [1, 2, 3]


def test_list_values_not_recursed():
    """Lists inside dicts should be treated as leaf values, not recursed."""
    data = {"items": [{"a": 1}, {"a": 2}], "a": 10}
    result = transform(data, "a", lambda x: x + 5)
    assert result["a"] == 15
    # The list items should remain untouched (lists are not recursed)
    assert result["items"] == [{"a": 1}, {"a": 2}]


def test_empty_dict():
    """Empty dict returns empty dict."""
    assert transform({}, "a", lambda x: x) == {}


def test_transform_string_values():
    """Transform works on string values too."""
    data = {"name": "alice", "info": {"name": "bob"}}
    result = transform(data, "name", str.upper)
    assert result == {"name": "ALICE", "info": {"name": "BOB"}}


def test_original_nested_list_not_mutated():
    """Mutable values within nested dicts must not be shared."""
    data = {"a": [1, 2], "b": {"a": [3, 4], "c": "hello"}}
    original = copy.deepcopy(data)
    result = transform(data, "a", lambda x: x + [99] if isinstance(x, list) else x)
    assert data == original
    assert result["a"] == [1, 2, 99]
    assert result["b"]["a"] == [3, 4, 99]
