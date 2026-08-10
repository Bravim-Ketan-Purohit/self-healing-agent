# Cache with Eviction Policy

## Problem

Implement two classes that work together—a generic cache and a pluggable eviction policy:

1. **`EvictionPolicy`** - Decides which key to evict. Two implementations required:
   - `LRUPolicy` - Least Recently Used: evicts the key that hasn't been accessed (get or put) longest.
   - `LFUPolicy` - Least Frequently Used: evicts the key accessed (get or put) the fewest times. On tie, evicts the least recently used among the tied keys.
   
   Each policy must implement:
   - `on_access(key)` - Notify the policy that a key was accessed (get or put).
   - `on_remove(key)` - Notify the policy that a key was removed.
   - `evict()` - Return the key to evict (without actually removing it from the policy).

2. **`Cache`** - A key-value cache with a max capacity:
   - `__init__(self, capacity, policy)` - Creates a cache with the given capacity and eviction policy.
   - `get(key)` - Return the value for key, or None if not present. Notifies policy on hit.
   - `put(key, value)` - Insert or update a key-value pair. If at capacity and inserting new key, asks policy for the key to evict.
   - `size()` - Return current number of entries.

## Interface Contract (Notification Protocol)

- Cache calls `policy.on_access(key)` every time a key is accessed (both `get` hits and `put` calls).
- Cache calls `policy.on_remove(key)` when a key is evicted.
- Cache calls `policy.evict()` when it needs to free space—policy returns the key to evict.
- Policy NEVER modifies the cache directly; it only tracks access info.

## Constraints

- Both classes must be in the same `solution.py` file.
- Do not use `functools.lru_cache` or similar built-ins.
