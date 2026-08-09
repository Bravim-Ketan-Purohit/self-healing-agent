from solution import PriorityQueue
import pytest


def test_push_and_pop_basic():
    pq = PriorityQueue()
    pq.push("a", 3)
    pq.push("b", 1)
    pq.push("c", 2)
    assert pq.pop() == "b"
    assert pq.pop() == "c"
    assert pq.pop() == "a"


def test_peek_returns_minimum():
    pq = PriorityQueue()
    pq.push("x", 5)
    pq.push("y", 2)
    assert pq.peek() == "y"
    assert len(pq) == 2  # peek doesn't remove


def test_update_priority():
    pq = PriorityQueue()
    pq.push("a", 10)
    pq.push("b", 5)
    pq.update_priority("a", 1)
    assert pq.pop() == "a"


def test_pop_empty_raises():
    pq = PriorityQueue()
    with pytest.raises(IndexError):
        pq.pop()
