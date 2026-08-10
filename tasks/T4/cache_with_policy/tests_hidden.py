import pytest
from solution import Cache, LRUPolicy, LFUPolicy


def test_lru_update_does_not_evict():
    policy = LRUPolicy()
    cache = Cache(2, policy)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("a", 10)  # update, should NOT evict
    assert cache.size() == 2
    assert cache.get("a") == 10
    assert cache.get("b") == 2


def test_lru_multiple_evictions():
    policy = LRUPolicy()
    cache = Cache(3, policy)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)
    cache.put("d", 4)  # evict a
    cache.put("e", 5)  # evict b
    assert cache.get("a") is None
    assert cache.get("b") is None
    assert cache.get("c") == 3


def test_lfu_tie_breaks_by_lru():
    policy = LFUPolicy()
    cache = Cache(2, policy)
    cache.put("a", 1)
    cache.put("b", 2)
    # Both have freq=1, "a" was accessed earlier, so evict "a"
    cache.put("c", 3)
    assert cache.get("a") is None
    assert cache.get("b") == 2


def test_lfu_frequency_matters():
    policy = LFUPolicy()
    cache = Cache(3, policy)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)
    # Access a and b multiple times
    cache.get("a")
    cache.get("a")
    cache.get("b")
    # freq: a=3, b=2, c=1
    cache.put("d", 4)  # should evict "c"
    assert cache.get("c") is None
    assert cache.get("a") == 1
    assert cache.get("b") == 2


def test_cache_capacity_one():
    policy = LRUPolicy()
    cache = Cache(1, policy)
    cache.put("a", 1)
    cache.put("b", 2)
    assert cache.get("a") is None
    assert cache.get("b") == 2
    assert cache.size() == 1


def test_get_miss_returns_none():
    cache = Cache(5, LRUPolicy())
    assert cache.get("nonexistent") is None


def test_lfu_removed_key_not_evicted_again():
    policy = LFUPolicy()
    cache = Cache(2, policy)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)  # evicts one
    # After eviction, remaining two should still be accessible
    assert cache.size() == 2
    remaining = [k for k in ["a", "b", "c"] if cache.get(k) is not None]
    assert len(remaining) == 2


def test_invalid_capacity():
    with pytest.raises((ValueError, Exception)):
        Cache(0, LRUPolicy())
