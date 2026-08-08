import pytest
from solution import topological_sort


def test_empty_graph():
    assert topological_sort({}) == []


def test_single_node():
    assert topological_sort({"a": []}) == ["a"]


def test_self_loop():
    with pytest.raises(ValueError):
        topological_sort({"a": ["a"]})


def test_three_node_cycle():
    graph = {"a": ["b"], "b": ["c"], "c": ["a"]}
    with pytest.raises(ValueError):
        topological_sort(graph)


def test_complex_dag():
    graph = {
        "a": ["b", "c"],
        "b": ["d"],
        "c": ["d", "e"],
        "d": ["f"],
        "e": ["f"],
        "f": [],
    }
    result = topological_sort(graph)
    # Verify ordering constraints
    assert result.index("a") < result.index("b")
    assert result.index("a") < result.index("c")
    assert result.index("b") < result.index("d")
    assert result.index("c") < result.index("d")
    assert result.index("c") < result.index("e")
    assert result.index("d") < result.index("f")
    assert result.index("e") < result.index("f")


def test_alphabetical_tiebreaking():
    graph = {"c": [], "a": [], "b": []}
    assert topological_sort(graph) == ["a", "b", "c"]


def test_partial_cycle():
    # Graph with a cycle among some nodes but not all
    graph = {"a": ["b"], "b": ["c"], "c": ["b"], "d": []}
    with pytest.raises(ValueError):
        topological_sort(graph)


def test_many_edges():
    graph = {
        "a": ["b", "c", "d", "e"],
        "b": ["e"],
        "c": ["e"],
        "d": ["e"],
        "e": [],
    }
    result = topological_sort(graph)
    assert result[0] == "a"
    assert result[-1] == "e"
