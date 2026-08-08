from collections import deque


def topological_sort(graph: dict[str, list[str]]) -> list[str]:
    """Topological sort of a DAG given as adjacency list. Raise ValueError on cycle."""
    # Compute in-degrees
    in_degree = {node: 0 for node in graph}
    for node in graph:
        for neighbor in graph[node]:
            if neighbor not in in_degree:
                in_degree[neighbor] = 0
            in_degree[neighbor] += 1

    # Start with nodes that have no incoming edges
    queue = deque(sorted(node for node, deg in in_degree.items() if deg == 0))
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)
        for neighbor in sorted(graph.get(node, [])):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(result) != len(in_degree):
        raise ValueError("Graph contains a cycle")

    return result
