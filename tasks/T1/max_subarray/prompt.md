# Maximum Subarray

Write a function `max_subarray(nums: list[int]) -> int` that finds the contiguous subarray (containing at least one number) which has the largest sum, and returns that sum.

Use Kadane's algorithm for an O(n) solution.

## Constraints

- `nums` is non-empty (contains at least one element).
- Elements may be negative.

## Examples

```python
max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6  # [4, -1, 2, 1]
max_subarray([1]) == 1
max_subarray([5, 4, -1, 7, 8]) == 23
max_subarray([-1, -2, -3]) == -1
```
