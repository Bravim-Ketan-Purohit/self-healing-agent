# Two Sum

Write a function `two_sum(nums: list[int], target: int) -> list[int]` that finds two indices whose values sum to `target`.

Return the pair of indices as a sorted list `[i, j]` where `i < j`.

If no such pair exists, raise a `ValueError`.

## Constraints

- Each input has at most one valid solution.
- You may not use the same element twice (indices must be different).
- `nums` may contain negative numbers and duplicates.

## Examples

```python
two_sum([2, 7, 11, 15], 9) == [0, 1]
two_sum([3, 2, 4], 6) == [1, 2]
two_sum([3, 3], 6) == [0, 1]
two_sum([1, 2, 3], 10)  # raises ValueError
```
