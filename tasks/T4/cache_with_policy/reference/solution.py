"""Cache with pluggable eviction policy (LRU and LFU)."""

from collections import OrderedDict


class LRUPolicy:
    """Least Recently Used eviction policy."""

    def __init__(self):
        self._order = OrderedDict()

    def on_access(self, key):
        """Mark key as most recently used."""
        if key in self._order:
            self._order.move_to_end(key)
        else:
            self._order[key] = True

    def on_remove(self, key):
        """Remove key from tracking."""
        if key in self._order:
            del self._order[key]

    def evict(self):
        """Return the least recently used key."""
        if not self._order:
            raise RuntimeError("No keys to evict")
        # First item in OrderedDict is the least recently used
        return next(iter(self._order))


class LFUPolicy:
    """Least Frequently Used eviction policy. Ties broken by LRU."""

    def __init__(self):
        self._freq = {}
        self._order = []  # tracks access order for tie-breaking
        self._time = 0

    def on_access(self, key):
        """Increment access count for key."""
        self._time += 1
        if key in self._freq:
            self._freq[key][0] += 1
            self._freq[key][1] = self._time
        else:
            self._freq[key] = [1, self._time]

    def on_remove(self, key):
        """Remove key from tracking."""
        if key in self._freq:
            del self._freq[key]

    def evict(self):
        """Return key with lowest frequency. Break ties by oldest access time."""
        if not self._freq:
            raise RuntimeError("No keys to evict")
        # Find the key with min frequency, then min last-access time
        min_key = min(self._freq, key=lambda k: (self._freq[k][0], self._freq[k][1]))
        return min_key


class Cache:
    """A key-value cache with a max capacity and pluggable eviction."""

    def __init__(self, capacity, policy):
        if capacity < 1:
            raise ValueError("Capacity must be at least 1")
        self._capacity = capacity
        self._policy = policy
        self._store = {}

    def get(self, key):
        """Return value for key, or None. Notifies policy on hit."""
        if key not in self._store:
            return None
        self._policy.on_access(key)
        return self._store[key]

    def put(self, key, value):
        """Insert or update. Evicts if at capacity and key is new."""
        if key in self._store:
            self._store[key] = value
            self._policy.on_access(key)
            return

        if len(self._store) >= self._capacity:
            evict_key = self._policy.evict()
            del self._store[evict_key]
            self._policy.on_remove(evict_key)

        self._store[key] = value
        self._policy.on_access(key)

    def size(self):
        """Return the number of entries in the cache."""
        return len(self._store)
