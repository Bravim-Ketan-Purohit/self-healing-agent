class CircularBuffer:
    """Fixed-size circular buffer with write, read, and overwrite."""

    def __init__(self, capacity: int):
        if capacity < 1:
            raise ValueError("Capacity must be at least 1")
        self._capacity = capacity
        self._buffer = [None] * capacity
        self._head = 0  # index to read from (oldest)
        self._tail = 0  # index to write to (next slot)
        self._size = 0

    def write(self, item) -> None:
        if self._size == self._capacity:
            raise BufferError("Buffer is full")
        self._buffer[self._tail] = item
        self._tail = (self._tail + 1) % self._capacity
        self._size += 1

    def read(self):
        if self._size == 0:
            raise BufferError("Buffer is empty")
        item = self._buffer[self._head]
        self._buffer[self._head] = None
        self._head = (self._head + 1) % self._capacity
        self._size -= 1
        return item

    def overwrite(self, item) -> None:
        if self._size < self._capacity:
            self.write(item)
        else:
            # Overwrite the oldest item
            self._buffer[self._head] = item
            self._head = (self._head + 1) % self._capacity
            self._tail = self._head

    def clear(self) -> None:
        self._buffer = [None] * self._capacity
        self._head = 0
        self._tail = 0
        self._size = 0

    def __len__(self) -> int:
        return self._size
