# Inclusive Range Overlap

Write a function `ranges_overlap(a: int, b: int, c: int, d: int) -> bool` that determines if two **inclusive** integer ranges [a, b] and [c, d] overlap.

Two ranges overlap if they share at least one integer in common. Since both endpoints are inclusive, ranges like [1, 5] and [5, 10] **do** overlap (they share 5).

## Examples

```python
ranges_overlap(1, 5, 3, 8)    # True — they share 3, 4, 5
ranges_overlap(1, 5, 5, 10)   # True — they share 5
ranges_overlap(1, 5, 6, 10)   # False — no overlap
ranges_overlap(1, 10, 3, 7)   # True — [3,7] is inside [1,10]
ranges_overlap(5, 5, 5, 5)    # True — single point, same point
```

## Constraints

- `a <= b` and `c <= d` are always guaranteed.
- All values are integers (can be negative).
