# Spiral Matrix

Write a function `spiral_order(matrix: list[list[int]]) -> list[int]` that returns all elements of an M x N matrix in spiral order (clockwise, starting from the top-left).

## Constraints

- The matrix may have different numbers of rows and columns (non-square).
- The matrix may be empty (0 rows) or contain empty rows.

## Examples

```python
spiral_order([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]) == [1, 2, 3, 6, 9, 8, 7, 4, 5]

spiral_order([
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12]
]) == [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]

spiral_order([[1]]) == [1]
spiral_order([]) == []
```
