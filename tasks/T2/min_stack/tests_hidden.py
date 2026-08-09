from solution import MinStack
import pytest


def test_min_after_popping_the_min():
    """Invariant: min must update correctly when the current min is popped."""
    s = MinStack()
    s.push(5)
    s.push(2)
    s.push(8)
    assert s.get_min() == 2
    s.pop()  # remove 8
    s.pop()  # remove 2 (the min)
    assert s.get_min() == 5


def test_duplicate_minimums():
    """Invariant: multiple copies of the same min must be tracked independently."""
    s = MinStack()
    s.push(1)
    s.push(1)
    s.push(1)
    s.pop()
    assert s.get_min() == 1
    s.pop()
    assert s.get_min() == 1
    s.pop()
    with pytest.raises(IndexError):
        s.get_min()


def test_decreasing_then_increasing():
    """Invariant: min tracks correctly through decreasing then increasing pushes."""
    s = MinStack()
    for val in [5, 4, 3, 2, 1]:
        s.push(val)
    assert s.get_min() == 1
    s.push(10)
    s.push(20)
    assert s.get_min() == 1
    # Pop everything above 1
    s.pop()
    s.pop()
    assert s.get_min() == 1
    s.pop()  # pop the 1
    assert s.get_min() == 2


def test_interleaved_push_pop_min():
    """Invariant: min is consistent after arbitrary interleaved operations."""
    s = MinStack()
    s.push(10)
    assert s.get_min() == 10
    s.push(5)
    assert s.get_min() == 5
    s.push(15)
    assert s.get_min() == 5
    s.pop()  # 15
    assert s.get_min() == 5
    s.pop()  # 5
    assert s.get_min() == 10
    s.push(3)
    assert s.get_min() == 3
    s.push(3)
    assert s.get_min() == 3
    s.pop()
    assert s.get_min() == 3


def test_top_and_get_min_on_empty_raise():
    """Invariant: all accessors raise IndexError on empty stack."""
    s = MinStack()
    with pytest.raises(IndexError):
        s.top()
    with pytest.raises(IndexError):
        s.get_min()
    s.push(1)
    s.pop()
    with pytest.raises(IndexError):
        s.top()


def test_negative_values():
    """Invariant: negative numbers handled correctly as min."""
    s = MinStack()
    s.push(-1)
    s.push(-3)
    s.push(-2)
    assert s.get_min() == -3
    s.pop()
    assert s.get_min() == -3
    s.pop()
    assert s.get_min() == -1


def test_large_sequence_maintains_invariant():
    """Invariant: min is correct after many operations."""
    s = MinStack()
    # Push 100 down to 1
    for i in range(100, 0, -1):
        s.push(i)
        assert s.get_min() == i
    # Pop them all, min should increase
    for i in range(1, 101):
        assert s.get_min() == i
        s.pop()


def test_pop_returns_correct_value():
    """Invariant: pop always returns the most recently pushed value."""
    s = MinStack()
    s.push(42)
    s.push(7)
    s.push(99)
    assert s.pop() == 99
    assert s.pop() == 7
    assert s.pop() == 42
