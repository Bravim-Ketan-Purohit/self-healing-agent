# Sort Preserving Index

Implement a function `sort_preserving_index(lst)` that sorts a list of integers and returns a tuple `(sorted_list, index_map)` where:

- `sorted_list` is the input sorted in ascending order
- `index_map` is a list where `index_map[i]` gives the **original index** of the element now at position `i` in the sorted list

## Requirements

1. The sort must be **stable** - equal elements must maintain their relative order from the input
2. For duplicate values, `index_map` must map each sorted position to a **unique** original index
3. The mapping must be **bijective** - every original index appears exactly once in `index_map`
4. `sorted_list[i]` must always equal `lst[index_map[i]]` for all valid `i`

## Example

```python
>>> sort_preserving_index([3, 1, 2])
([1, 2, 3], [1, 2, 0])

>>> sort_preserving_index([5, 5, 5])
([5, 5, 5], [0, 1, 2])  # stable sort preserves order
```
