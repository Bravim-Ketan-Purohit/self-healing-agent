# Flatten List

Write a function `flatten_list(lst: list) -> list` that flattens a nested list of arbitrary depth into a single flat list.

The function should handle lists nested to any depth and preserve the order of elements.

## Examples

```python
flatten_list([1, [2, 3], [4, [5, 6]]]) == [1, 2, 3, 4, 5, 6]
flatten_list([[1, 2], [3, [4, [5]]]]) == [1, 2, 3, 4, 5]
flatten_list([]) == []
flatten_list([1, 2, 3]) == [1, 2, 3]
```
