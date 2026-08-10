import pytest
from solution import Queue, BatchProcessor


def test_queue_fifo_order():
    q = Queue()
    q.put("first")
    q.put("second")
    q.put("third")
    assert q.get() == "first"
    assert q.get() == "second"
    assert q.get() == "third"


def test_queue_raises_on_empty_get():
    q = Queue()
    with pytest.raises(IndexError):
        q.get()


def test_queue_size_tracking():
    q = Queue()
    assert q.size() == 0
    q.put(1)
    q.put(2)
    assert q.size() == 2
    q.get()
    assert q.size() == 1


def test_batch_processor_invalid_batch_size():
    q = Queue()
    with pytest.raises((ValueError, Exception)):
        BatchProcessor(q, batch_size=0)


def test_process_all_empty_queue():
    q = Queue()
    bp = BatchProcessor(q, batch_size=5)
    assert bp.process_all() == []


def test_batch_size_one():
    q = Queue()
    for i in range(3):
        q.put(i)
    bp = BatchProcessor(q, batch_size=1)
    assert bp.process_all() == [[0], [1], [2]]


def test_batch_size_larger_than_queue():
    q = Queue()
    q.put("x")
    q.put("y")
    bp = BatchProcessor(q, batch_size=10)
    assert bp.process_batch() == ["x", "y"]
    assert q.is_empty() is True


def test_interleaved_put_and_process():
    q = Queue()
    q.put(1)
    q.put(2)
    bp = BatchProcessor(q, batch_size=2)
    assert bp.process_batch() == [1, 2]
    q.put(3)
    q.put(4)
    q.put(5)
    assert bp.process_batch() == [3, 4]
    assert bp.process_batch() == [5]
    assert bp.process_batch() == []
