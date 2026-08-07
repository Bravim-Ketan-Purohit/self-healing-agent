# Run Length Encode

Write a function `run_length_encode(s: str) -> str` that compresses a string using run-length encoding.

Consecutive duplicate characters are replaced by the count followed by the character.

- Even single characters get a count of 1.
- Non-alphabetic characters are treated the same way.

## Examples

```python
run_length_encode("aaabbc") == "3a2b1c"
run_length_encode("a") == "1a"
run_length_encode("aabb") == "2a2b"
run_length_encode("") == ""
```
