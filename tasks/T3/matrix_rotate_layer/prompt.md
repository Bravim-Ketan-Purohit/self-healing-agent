# Matrix Rotate Layer

Write a function `rotate_outer_layer(matrix: list[list[int]], k: int) -> list[list[int]]` that rotates the outer layer (border elements) of an NxM matrix by `k` positions clockwise.

The function must return a **new** matrix (do not mutate the original). Interior elements remain unchanged.

## Examples

```python
rotate_outer_layer([[1, 2, 3],
                    [4, 5, 6],
                    [7, 8, 9]], 1)
# Returns:
# [[4, 1, 2],
#  [7, 5, 3],
#  [8, 9, 6]]

rotate_outer_layer([[1, 2, 3],
                    [4, 5, 6],
                    [7, 8, 9]], 8)
# Full rotation (perimeter=8), returns original arrangement:
# [[1, 2, 3],
#  [4, 5, 6],
#  [7, 8, 9]]
```

## Constraints

- Matrix is at least 1x1.
- `k` is a non-negative integer (can be >= perimeter length).
- When `k >= perimeter`, wrap using modulo.
- Do not mutate the original matrix.
