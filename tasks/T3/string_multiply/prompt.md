# String Multiply

Write a function `repeat_join(s: str, n: int, sep: str) -> str` that repeats the string `s` exactly `n` times, joining them with the separator `sep`.

Note: `n` repetitions means there should be `n - 1` separators between them.

## Examples

```python
repeat_join("ha", 3, "-")     # "ha-ha-ha"
repeat_join("ab", 1, ",")     # "ab"
repeat_join("x", 5, "")       # "xxxxx"
repeat_join("hi", 0, "-")     # ""
repeat_join("a", 2, "---")    # "a---a"
```

## Constraints

- `n` is a non-negative integer.
- If `n == 0`, return an empty string.
- If `n == 1`, return `s` (no separator).
- `s` and `sep` can be any string (including empty).
