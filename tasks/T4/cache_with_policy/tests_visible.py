from solution import Cache, LRUPolicy, LFUPolicy


def test_lru_basic_eviction():
    policy = LRUPolicy()
    cache = Cache(2, policy)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)  # should evict "a"
    assert cache.get("a") is None
    assert cache.get("b") == 2
    assert cache.get("c") == 3


def test_lru_access_updates_order():
    policy = LRUPolicy()
    cache = Cache(2, policy)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.get("a")  # "a" is now most recent
    cache.put("c", 3)  # should evict "b"
    assert cache.get("b") is None
    assert cache.get("a") == 1


def test_lfu_basic_eviction():
    policy = LFUPolicy()
    cache = Cache(2, policy)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.get("a")  # freq: a=2, b=1
    cache.put("c", 3)  # should evict "b" (least frequent)
    assert cache.get("b") is None
    assert cache.get("a") == 1


def test_cache_size():
    cache = Cache(3, LRUPolicy())
    assert cache.size() == 0
    cache.put("x", 1)
    assert cache.size() == 1
