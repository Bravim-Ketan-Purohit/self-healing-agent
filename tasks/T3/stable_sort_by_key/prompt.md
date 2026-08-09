# Stable Sort by Key

Write a function `stable_sort_by_key(items: list[dict], key: str) -> list[dict]` that sorts a list of dictionaries by the value of the given key in ascending order, while **preserving the original order** for items with equal key values (stable sort).

The function must return a new list (do not mutate the original).

## Examples

```python
stable_sort_by_key(
    [{"name": "alice", "age": 30},
     {"name": "bob", "age": 25},
     {"name": "carol", "age": 30}],
    "age"
)
# Returns:
# [{"name": "bob", "age": 25},
#  {"name": "alice", "age": 30},
#  {"name": "carol", "age": 30}]
# Note: alice comes before carol because she was first in the original list.

stable_sort_by_key(
    [{"id": 3}, {"id": 1}, {"id": 2}],
    "id"
)
# Returns: [{"id": 1}, {"id": 2}, {"id": 3}]
```

## Constraints

- All items in the list have the given key.
- Values for the key are comparable (numbers or strings).
- The original list must not be mutated.
- Stability is required: equal-keyed items retain their relative order.
