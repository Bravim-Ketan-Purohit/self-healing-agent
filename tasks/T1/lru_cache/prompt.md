# LRU Cache

Implement a Least Recently Used (LRU) cache class `LRUCache` with the following interface:

- `LRUCache(capacity: int)` — Initialize the cache with a positive capacity.
- `get(key: int) -> int` — Return the value associated with `key` if it exists, otherwise return `-1`.
- `put(key: int, value: int) -> None` — Insert or update the value for `key`. If the cache exceeds its capacity, evict the least recently used key before inserting.

A key is "used" whenever `get` or `put` is called on it.

## Constraints

- `capacity >= 1`
- All keys and values are integers.
- Both `get` and `put` should run in O(1) average time.

## Examples

```python
cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
cache.get(1)       # returns 1
cache.put(3, 3)    # evicts key 2
cache.get(2)       # returns -1 (not found)
cache.put(4, 4)    # evicts key 1
cache.get(1)       # returns -1
cache.get(3)       # returns 3
cache.get(4)       # returns 4
```
