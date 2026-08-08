import pytest
from solution import topological_sort


def test_linear_chain():
    graph = {"a": ["b"], "b": ["c"], "c": []}
    assert topological_sort(graph) == ["a", "b", "c"]


def test_diamond():
    graph = {"a": ["b", "c"], "b": ["d"], "c": ["d"], "d": []}
    assert topological_sort(graph) == ["a", "b", "c", "d"]


def test_cycle_raises():
    graph = {"a": ["b"], "b": ["a"]}
    with pytest.raises(ValueError):
        topological_sort(graph)


def test_independent_nodes():
    graph = {"x": [], "y": [], "z": []}
    assert topological_sort(graph) == ["x", "y", "z"]
