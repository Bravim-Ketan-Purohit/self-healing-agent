from solution import BoundedCounter
import threading
import pytest


def test_value_never_exceeds_max():
    """Invariant: value is always <= max_value."""
    c = BoundedCounter(0, 5, 3)
    c.increment(2)  # -> 5
    with pytest.raises(OverflowError):
        c.increment(1)  # would be 6
    assert c.value == 5


def test_value_never_below_min():
    """Invariant: value is always >= min_value."""
    c = BoundedCounter(-2, 10, 0)
    c.decrement(2)  # -> -2
    with pytest.raises(OverflowError):
        c.decrement(1)  # would be -3
    assert c.value == -2


def test_failed_operation_leaves_value_unchanged():
    """Invariant: failed increment/decrement does not modify value."""
    c = BoundedCounter(0, 10, 5)
    with pytest.raises(OverflowError):
        c.increment(6)  # would be 11
    assert c.value == 5
    with pytest.raises(OverflowError):
        c.decrement(6)  # would be -1
    assert c.value == 5


def test_invalid_amount_raises():
    """Invariant: zero or negative amounts raise ValueError."""
    c = BoundedCounter(0, 10, 5)
    with pytest.raises(ValueError):
        c.increment(0)
    with pytest.raises(ValueError):
        c.increment(-1)
    with pytest.raises(ValueError):
        c.decrement(0)
    with pytest.raises(ValueError):
        c.decrement(-3)


def test_invalid_construction():
    """Invariant: invalid construction parameters raise ValueError."""
    with pytest.raises(ValueError):
        BoundedCounter(10, 5, 7)  # min > max
    with pytest.raises(ValueError):
        BoundedCounter(0, 10, 11)  # initial > max
    with pytest.raises(ValueError):
        BoundedCounter(0, 10, -1)  # initial < min


def test_thread_safety_invariant():
    """Invariant: value stays in [min, max] even under concurrent access."""
    c = BoundedCounter(0, 1000, 500)
    errors = []

    def inc_worker():
        for _ in range(100):
            try:
                c.increment(1)
            except OverflowError:
                pass

    def dec_worker():
        for _ in range(100):
            try:
                c.decrement(1)
            except OverflowError:
                pass

    threads = []
    for _ in range(5):
        threads.append(threading.Thread(target=inc_worker))
        threads.append(threading.Thread(target=dec_worker))
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert 0 <= c.value <= 1000


def test_reset_sets_to_min():
    """Invariant: reset always sets value to min_value."""
    c = BoundedCounter(-5, 5, 3)
    c.increment(2)
    c.reset()
    assert c.value == -5


def test_large_increments_and_decrements():
    """Invariant: large steps that stay in bounds succeed."""
    c = BoundedCounter(0, 1000, 0)
    c.increment(1000)
    assert c.value == 1000
    c.decrement(1000)
    assert c.value == 0
