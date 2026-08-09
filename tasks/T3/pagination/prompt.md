# Pagination

Write a function `paginate(items: list, page: int, page_size: int) -> list` that returns the items for a given 0-indexed page.

Pages are 0-indexed: page 0 is the first page containing items[0:page_size], page 1 contains items[page_size:2*page_size], etc.

If the requested page is beyond the available data, return an empty list.

## Examples

```python
paginate([1, 2, 3, 4, 5], 0, 2)  # [1, 2]
paginate([1, 2, 3, 4, 5], 1, 2)  # [3, 4]
paginate([1, 2, 3, 4, 5], 2, 2)  # [5]
paginate([1, 2, 3, 4, 5], 3, 2)  # []
paginate([], 0, 5)               # []
```

## Constraints

- `page` is a non-negative integer (0-indexed).
- `page_size` is a positive integer (>= 1).
- Return an empty list for out-of-range pages or empty input.
