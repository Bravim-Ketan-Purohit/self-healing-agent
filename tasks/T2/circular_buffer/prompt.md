# Circular Buffer

Implement a `CircularBuffer` class representing a fixed-size circular (ring) buffer:

- `__init__(self, capacity: int)` — Create a buffer with the given maximum capacity. Raises `ValueError` if capacity < 1.
- `write(self, item)` — Write an item to the buffer. Raises `BufferError` if the buffer is full.
- `read(self)` — Read and remove the oldest item. Raises `BufferError` if the buffer is empty.
- `overwrite(self, item)` — Write an item; if the buffer is full, overwrite the oldest item.
- `clear(self)` — Reset the buffer to empty.
- `__len__(self)` — Return the number of items currently in the buffer.

## Invariants

- `len(buffer)` is always between 0 and capacity (inclusive).
- `read` returns items in FIFO order (oldest first).
- `overwrite` when full discards exactly the oldest item and writes the new item in its place.
- After `clear()`, the buffer behaves as if newly created.

## Examples

```python
buf = CircularBuffer(3)
buf.write("a")
buf.write("b")
buf.write("c")
buf.read()  # "a"
buf.write("d")
buf.read()  # "b"
buf.read()  # "c"
buf.read()  # "d"

buf2 = CircularBuffer(2)
buf2.write(1)
buf2.write(2)
buf2.overwrite(3)  # overwrites 1
buf2.read()  # 2
buf2.read()  # 3
```
