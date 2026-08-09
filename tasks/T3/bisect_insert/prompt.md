# Bisect Insert

Write a function `insert_sorted(lst: list[int], val: int) -> list[int]` that inserts `val` into the sorted list `lst` while maintaining sorted order.

**Important:** The function must NOT mutate the original list. Return a new list.

If `val` is equal to an existing element, insert it after all existing equal elements (stable insertion).

## Examples

```python
insert_sorted([1, 3, 5, 7], 4)      # [1, 3, 4, 5, 7]
insert_sorted([1, 3, 5, 7], 0)      # [0, 1, 3, 5, 7]
insert_sorted([1, 3, 5, 7], 8)      # [1, 3, 5, 7, 8]
insert_sorted([1, 3, 3, 5], 3)      # [1, 3, 3, 3, 5]
insert_sorted([], 5)                 # [5]
```

## Constraints

- `lst` is sorted in non-decreasing order.
- `val` is any integer.
- The original list must not be modified.
