"""Cache with pluggable eviction policy (LRU and LFU).

Do not use functools.lru_cache or similar built-ins.
"""


class LRUPolicy:
    """Least Recently Used eviction policy."""

    def __init__(self):
        raise NotImplementedError

    def on_access(self, key):
        """Mark key as most recently used."""
        raise NotImplementedError

    def on_remove(self, key):
        """Remove key from tracking."""
        raise NotImplementedError

    def evict(self):
        """Return the least recently used key."""
        raise NotImplementedError


class LFUPolicy:
    """Least Frequently Used eviction policy.

    On tie (same frequency), evicts the least recently used among tied keys.
    """

    def __init__(self):
        raise NotImplementedError

    def on_access(self, key):
        """Increment access count for key."""
        raise NotImplementedError

    def on_remove(self, key):
        """Remove key from tracking."""
        raise NotImplementedError

    def evict(self):
        """Return key with lowest frequency (ties broken by LRU)."""
        raise NotImplementedError


class Cache:
    """A key-value cache with max capacity and pluggable eviction."""

    def __init__(self, capacity, policy):
        raise NotImplementedError

    def get(self, key):
        """Return value for key, or None. Notifies policy on hit."""
        raise NotImplementedError

    def put(self, key, value):
        """Insert or update. Evicts if at capacity and key is new."""
        raise NotImplementedError

    def size(self):
        """Return number of entries."""
        raise NotImplementedError
