# Binary Search

Write a function `binary_search(nums: list[int], target: int) -> int` that performs binary search on a sorted list of integers.

Return the index of `target` in `nums`, or `-1` if the target is not found.

If `target` appears multiple times, return the index of its **first occurrence**.

## Constraints

- `nums` is sorted in non-decreasing order.
- `nums` may be empty.
- Elements may be negative.

## Examples

```python
binary_search([1, 3, 5, 7, 9], 5) == 2
binary_search([1, 3, 5, 7, 9], 4) == -1
binary_search([], 1) == -1
binary_search([2, 2, 2, 2], 2) == 0
```
