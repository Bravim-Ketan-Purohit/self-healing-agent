# Topological Sort

Write a function `topological_sort(graph: dict[str, list[str]]) -> list[str]` that returns a valid topological ordering of nodes in a directed acyclic graph (DAG).

The graph is given as an adjacency list where keys are node names and values are lists of nodes that the key has edges to (i.e., `graph[u]` contains `v` means there is an edge from `u` to `v`).

If the graph contains a cycle, raise a `ValueError`.

For determinism, when multiple nodes are available to process, choose them in alphabetical order.

## Constraints

- Node names are strings.
- The graph may be empty.
- All nodes appear as keys in the dict (even if they have no outgoing edges).
- If the graph has a cycle, raise `ValueError`.

## Examples

```python
topological_sort({"a": ["b", "c"], "b": ["d"], "c": ["d"], "d": []})
# => ["a", "b", "c", "d"]

topological_sort({"x": [], "y": [], "z": []})
# => ["x", "y", "z"]

topological_sort({"a": ["b"], "b": ["a"]})
# raises ValueError
```
