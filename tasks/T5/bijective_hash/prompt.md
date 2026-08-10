# Bijective Hash

Implement a function `bijective_hash(s: str) -> int` that hashes a string to an integer with the following properties:

## Requirements

1. **Deterministic**: Same input always produces same output
2. **Fixed output range**: Output must be a non-negative integer in range `[0, 2^32 - 1]` (32-bit unsigned)
3. **Collision-free (bijective)**: No two distinct strings may produce the same hash value. `bijective_hash(a) == bijective_hash(b)` implies `a == b`
4. **Constant time**: The function must run in O(1) time regardless of input length
5. **Universal**: Must work for ANY valid Python string (including empty string, unicode, strings of any length)

## Example

```python
>>> bijective_hash("hello")
# some integer in [0, 2^32 - 1]
>>> bijective_hash("world")
# different integer than above
>>> bijective_hash("hello") == bijective_hash("hello")
True
>>> bijective_hash("hello") == bijective_hash("world")
False
```

## Notes

A bijective hash is extremely valuable for perfect hash tables and data deduplication.
The O(1) constraint means you cannot iterate over the entire string character by character.
