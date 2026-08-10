"""Queue and BatchProcessor that must agree on the interface contract."""


class Queue:
    """A simple FIFO queue."""

    def __init__(self):
        raise NotImplementedError

    def put(self, item):
        """Add an item to the back of the queue."""
        raise NotImplementedError

    def get(self):
        """Remove and return the front item. Raises IndexError if empty."""
        raise NotImplementedError

    def size(self):
        """Return the number of items in the queue."""
        raise NotImplementedError

    def is_empty(self):
        """Return True if the queue is empty."""
        raise NotImplementedError


class BatchProcessor:
    """Processes items from a Queue in fixed-size batches."""

    def __init__(self, queue, batch_size):
        raise NotImplementedError

    def process_batch(self):
        """Remove up to batch_size items from queue and return as list.
        Returns empty list if queue is empty."""
        raise NotImplementedError

    def process_all(self):
        """Process all items in batches. Returns list of non-empty batches."""
        raise NotImplementedError
