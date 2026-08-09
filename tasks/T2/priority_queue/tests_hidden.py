from solution import PriorityQueue
import pytest


def test_pop_always_returns_minimum():
    """Invariant: pop always returns the item with the lowest priority."""
    pq = PriorityQueue()
    pq.push("e", 5)
    pq.push("a", 1)
    pq.push("d", 4)
    pq.push("b", 2)
    pq.push("c", 3)
    results = [pq.pop() for _ in range(5)]
    assert results == ["a", "b", "c", "d", "e"]


def test_no_duplicates_on_push_existing():
    """Invariant: pushing an existing item updates priority, no duplicates."""
    pq = PriorityQueue()
    pq.push("item", 5)
    pq.push("item", 1)  # should update, not duplicate
    assert len(pq) == 1
    assert pq.pop() == "item"
    assert len(pq) == 0


def test_update_priority_maintains_order():
    """Invariant: after update_priority, heap ordering is correct."""
    pq = PriorityQueue()
    pq.push("a", 1)
    pq.push("b", 2)
    pq.push("c", 3)
    pq.update_priority("c", 0)
    assert pq.pop() == "c"
    assert pq.pop() == "a"
    assert pq.pop() == "b"


def test_update_priority_nonexistent_raises():
    """Invariant: updating a non-existent item raises KeyError."""
    pq = PriorityQueue()
    pq.push("a", 1)
    with pytest.raises(KeyError):
        pq.update_priority("z", 5)


def test_peek_empty_raises():
    """Invariant: peek on empty queue raises IndexError."""
    pq = PriorityQueue()
    with pytest.raises(IndexError):
        pq.peek()


def test_contains_reflects_state():
    """Invariant: __contains__ accurately reflects queue membership."""
    pq = PriorityQueue()
    pq.push("x", 1)
    assert "x" in pq
    assert "y" not in pq
    pq.pop()
    assert "x" not in pq


def test_large_sequence_maintains_min_invariant():
    """Invariant: pop returns minimum even after many mixed operations."""
    pq = PriorityQueue()
    for i in range(50, 0, -1):
        pq.push(f"item_{i}", i)
    pq.update_priority("item_50", -1)
    assert pq.pop() == "item_50"
    # Rest should come out in order 1..49
    prev_priority = -1
    for i in range(49):
        item = pq.pop()
        num = int(item.split("_")[1])
        assert num > prev_priority or prev_priority == -1
        prev_priority = num


def test_update_priority_increase():
    """Invariant: increasing priority pushes item down correctly."""
    pq = PriorityQueue()
    pq.push("a", 1)
    pq.push("b", 2)
    pq.push("c", 3)
    pq.update_priority("a", 10)
    assert pq.pop() == "b"
    assert pq.pop() == "c"
    assert pq.pop() == "a"
