# Zip Longest

Write a function `zip_longest(*lists, fill=None) -> list` that zips multiple lists together, filling shorter lists with a fill value.

- Returns a list of tuples.
- Each tuple has one element from each input list.
- Shorter lists are padded with the `fill` value to match the longest list.
- If no lists are provided, return an empty list.

## Examples

```python
zip_longest([1, 2, 3], [4, 5], fill=0) == [(1, 4), (2, 5), (3, 0)]
zip_longest([1], [2, 3], [4, 5, 6], fill=-1) == [(1, 2, 4), (-1, 3, 5), (-1, -1, 6)]
zip_longest([1, 2], [3, 4]) == [(1, 3), (2, 4)]
zip_longest() == []
```
