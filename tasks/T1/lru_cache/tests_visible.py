from solution import LRUCache


def test_basic_put_and_get():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1


def test_eviction():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.put(3, 3)  # evicts key 1
    assert cache.get(1) == -1


def test_get_missing_key():
    cache = LRUCache(2)
    assert cache.get(99) == -1


def test_update_existing():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(1, 10)
    assert cache.get(1) == 10
