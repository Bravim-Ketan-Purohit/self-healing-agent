from solution import BoundedCounter
import pytest


def test_increment_and_value():
    c = BoundedCounter(0, 10, 0)
    assert c.increment(5) == 5
    assert c.value == 5


def test_decrement():
    c = BoundedCounter(0, 10, 5)
    assert c.decrement(3) == 2
    assert c.value == 2


def test_overflow_raises():
    c = BoundedCounter(0, 10, 8)
    with pytest.raises(OverflowError):
        c.increment(5)


def test_underflow_raises():
    c = BoundedCounter(0, 10, 2)
    with pytest.raises(OverflowError):
        c.decrement(5)
