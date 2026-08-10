"""Queue and BatchProcessor that must agree on the interface contract."""


class Queue:
    """A simple FIFO queue."""

    def __init__(self):
        self._items = []

    def put(self, item):
        """Add an item to the back of the queue."""
        self._items.append(item)

    def get(self):
        """Remove and return the front item. Raises IndexError if empty."""
        if not self._items:
            raise IndexError("Queue is empty")
        return self._items.pop(0)

    def size(self):
        """Return the number of items in the queue."""
        return len(self._items)

    def is_empty(self):
        """Return True if the queue is empty."""
        return len(self._items) == 0


class BatchProcessor:
    """Processes items from a Queue in fixed-size batches."""

    def __init__(self, queue, batch_size):
        if batch_size < 1:
            raise ValueError("batch_size must be at least 1")
        self.queue = queue
        self.batch_size = batch_size

    def process_batch(self):
        """Remove up to batch_size items from queue and return as list.
        Returns empty list if queue is empty."""
        batch = []
        for _ in range(self.batch_size):
            if self.queue.is_empty():
                break
            batch.append(self.queue.get())
        return batch

    def process_all(self):
        """Process all items in batches. Returns list of non-empty batches."""
        batches = []
        while not self.queue.is_empty():
            batch = self.process_batch()
            if batch:
                batches.append(batch)
        return batches
