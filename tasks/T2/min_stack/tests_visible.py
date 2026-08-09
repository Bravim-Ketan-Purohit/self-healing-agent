from solution import MinStack
import pytest


def test_push_and_top():
    s = MinStack()
    s.push(10)
    s.push(20)
    assert s.top() == 20


def test_pop_returns_value():
    s = MinStack()
    s.push(1)
    s.push(2)
    assert s.pop() == 2
    assert s.pop() == 1


def test_get_min_basic():
    s = MinStack()
    s.push(3)
    s.push(1)
    s.push(2)
    assert s.get_min() == 1


def test_empty_stack_raises():
    s = MinStack()
    with pytest.raises(IndexError):
        s.pop()
