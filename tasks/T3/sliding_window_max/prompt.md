# Sliding Window Maximum

Write a function `sliding_max(nums: list[int], k: int) -> list[int]` that returns the maximum value in each sliding window of size `k`.

The window slides from left to right, one element at a time. The output list should have exactly `len(nums) - k + 1` elements.

## Examples

```python
sliding_max([1, 3, -1, -3, 5, 3, 6, 7], 3)
# [3, 3, 5, 5, 6, 7]

sliding_max([1, 2, 3, 4, 5], 1)
# [1, 2, 3, 4, 5]

sliding_max([5, 4, 3, 2, 1], 5)
# [5]
```

## Constraints

- `1 <= k <= len(nums)`
- `nums` contains at least one element.
- The output has exactly `len(nums) - k + 1` elements.
