# Chunk List

Write a function `chunk_list(lst: list, n: int) -> list` that splits a list into consecutive chunks of size `n`.

- The last chunk may contain fewer than `n` elements.
- If `n` is less than 1, raise a `ValueError`.
- If the list is empty, return an empty list.

## Examples

```python
chunk_list([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]
chunk_list([1, 2, 3], 3) == [[1, 2, 3]]
chunk_list([1, 2, 3, 4], 1) == [[1], [2], [3], [4]]
chunk_list([], 5) == []
```
