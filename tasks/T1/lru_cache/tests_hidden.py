from solution import LRUCache


def test_capacity_one():
    cache = LRUCache(1)
    cache.put(1, 1)
    cache.put(2, 2)  # evicts 1
    assert cache.get(1) == -1
    assert cache.get(2) == 2


def test_get_refreshes_usage():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.get(1)     # refreshes key 1
    cache.put(3, 3)  # should evict key 2, not key 1
    assert cache.get(2) == -1
    assert cache.get(1) == 1


def test_put_existing_refreshes_usage():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.put(1, 10)  # update refreshes key 1
    cache.put(3, 3)   # should evict key 2
    assert cache.get(2) == -1
    assert cache.get(1) == 10


def test_eviction_order_after_multiple_gets():
    cache = LRUCache(3)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.put(3, 3)
    cache.get(1)
    cache.get(2)
    cache.put(4, 4)  # evicts key 3 (least recently used)
    assert cache.get(3) == -1
    assert cache.get(1) == 1
    assert cache.get(2) == 2
    assert cache.get(4) == 4


def test_get_nonexistent_does_not_affect_order():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.get(99)    # miss, should not change anything
    cache.put(3, 3)  # evicts key 1 (oldest)
    assert cache.get(1) == -1
    assert cache.get(2) == 2


def test_overwrite_does_not_increase_size():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.put(1, 100)
    cache.put(2, 200)
    # No eviction should have happened
    assert cache.get(1) == 100
    assert cache.get(2) == 200


def test_sequential_evictions():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.put(3, 3)  # evicts 1
    cache.put(4, 4)  # evicts 2
    assert cache.get(1) == -1
    assert cache.get(2) == -1
    assert cache.get(3) == 3
    assert cache.get(4) == 4
