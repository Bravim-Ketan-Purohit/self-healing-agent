import time
from solution import MedianCollection


def test_add_is_constant_time():
    """Verify add is truly O(1) by comparing time for small vs large collections."""
    mc_small = MedianCollection()
    mc_large = MedianCollection()

    # Pre-fill large collection
    for i in range(100000):
        mc_large.add(i)

    # Time adding to small collection
    start = time.perf_counter_ns()
    for i in range(10000):
        mc_small.add(i)
    small_time = time.perf_counter_ns() - start

    # Time adding to large collection (should be same if O(1))
    start = time.perf_counter_ns()
    for i in range(100000, 110000):
        mc_large.add(i)
    large_time = time.perf_counter_ns() - start

    # O(1) means large collection adds should be within 3x of small
    assert large_time < small_time * 3, \
        f"add() not O(1): large={large_time}ns, small={small_time}ns"


def test_median_is_constant_time():
    """Verify median is truly O(1) regardless of collection size."""
    mc_small = MedianCollection()
    mc_large = MedianCollection()

    for i in range(100):
        mc_small.add(i)
    for i in range(100000):
        mc_large.add(i)

    # Time median on small
    start = time.perf_counter_ns()
    for _ in range(10000):
        mc_small.median()
    small_time = time.perf_counter_ns() - start

    # Time median on large
    start = time.perf_counter_ns()
    for _ in range(10000):
        mc_large.median()
    large_time = time.perf_counter_ns() - start

    assert large_time < small_time * 3, \
        f"median() not O(1): large={large_time}ns, small={small_time}ns"


def test_remove_maintains_correct_median_stress():
    """Stress test that interleaved add/remove gives correct median
    with random access pattern - impossible in O(1) without sorted structure."""
    import random
    random.seed(42)
    mc = MedianCollection()
    elements = []

    for _ in range(10000):
        if elements and random.random() < 0.3:
            val = random.choice(elements)
            mc.remove(val)
            elements.remove(val)
        else:
            val = random.randint(-1000000, 1000000)
            mc.add(val)
            elements.append(val)

    # Verify median is correct
    elements.sort()
    n = len(elements)
    if n % 2 == 1:
        expected = elements[n // 2]
    else:
        expected = (elements[n // 2 - 1] + elements[n // 2]) / 2
    assert mc.median() == expected


def test_adversarial_add_remove_pattern():
    """Adversarial pattern that defeats simple dual-heap approaches
    while also requiring O(1) time (contradictory)."""
    mc = MedianCollection()
    # Add in pattern that forces rebalancing
    for i in range(50000):
        mc.add(i)
    # Remove from middle - forces O(log n) in any correct approach
    start = time.perf_counter_ns()
    for i in range(25000):
        mc.remove(i)
        assert mc.median() == (25000 + i + 49999) / 2 or \
               mc.median() == (i + 25000 + 49999) // 2
    elapsed = time.perf_counter_ns() - start

    # Must complete 25000 remove+median pairs in under 50ms (O(1) each)
    assert elapsed < 50_000_000, \
        f"Operations too slow for O(1): {elapsed}ns for 25000 ops"
