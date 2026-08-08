# Merge Intervals

Write a function `merge_intervals(intervals: list[list[int]]) -> list[list[int]]` that merges all overlapping intervals and returns a list of non-overlapping intervals that cover all the ranges in the input.

Two intervals `[a, b]` and `[c, d]` overlap if `c <= b` (assuming `a <= c` after sorting).

The output should be sorted by start time.

## Constraints

- Each interval is `[start, end]` where `start <= end`.
- The input list may not be sorted.
- The input list may be empty.

## Examples

```python
merge_intervals([[1,3],[2,6],[8,10],[15,18]]) == [[1,6],[8,10],[15,18]]
merge_intervals([[1,4],[4,5]]) == [[1,5]]
merge_intervals([]) == []
merge_intervals([[1,4],[0,4]]) == [[0,4]]
```
