from solution import Queue, BatchProcessor


def test_basic_batch():
    q = Queue()
    for i in range(5):
        q.put(i)
    bp = BatchProcessor(q, batch_size=2)
    assert bp.process_batch() == [0, 1]
    assert bp.process_batch() == [2, 3]
    assert bp.process_batch() == [4]


def test_empty_queue_batch():
    q = Queue()
    bp = BatchProcessor(q, batch_size=3)
    assert bp.process_batch() == []


def test_process_all():
    q = Queue()
    for i in range(7):
        q.put(i)
    bp = BatchProcessor(q, batch_size=3)
    batches = bp.process_all()
    assert batches == [[0, 1, 2], [3, 4, 5], [6]]


def test_queue_empty_after_get():
    q = Queue()
    q.put("a")
    assert q.get() == "a"
    assert q.is_empty() is True
