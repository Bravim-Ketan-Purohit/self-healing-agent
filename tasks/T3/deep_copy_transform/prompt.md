# Deep Copy Transform

Write a function `transform(data: dict, key: str, func: callable) -> dict` that returns a **new** dictionary with `func` applied to every value associated with `key` at any level of nesting.

The original `data` dictionary must NOT be mutated.

The function should recursively search through all nested dictionaries. If a nested dict contains the target `key`, apply `func` to its value in the returned copy. Non-dict values and keys that don't match should remain unchanged.

## Examples

```python
data = {"a": 1, "b": {"a": 2, "c": 3}}
result = transform(data, "a", lambda x: x * 10)
# result == {"a": 10, "b": {"a": 20, "c": 3}}
# data is still {"a": 1, "b": {"a": 2, "c": 3}}

data = {"x": {"y": {"x": 5}}}
result = transform(data, "x", lambda v: v + 1 if isinstance(v, int) else v)
# The top-level "x" value is a dict, so func is applied to it (returns the dict since not int)
# The nested "x" with value 5 gets func applied: 6
```

## Constraints

- `data` is a dictionary that may be nested to arbitrary depth.
- Only dict values should be recursed into.
- Lists inside dicts should NOT be recursed into (treat them as leaf values).
- The original `data` must remain completely unchanged after the call.
