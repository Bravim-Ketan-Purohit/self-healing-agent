# Producer/Consumer: Queue & BatchProcessor

## Problem

Implement two classes that work together:

1. **`Queue`** - A FIFO queue with these methods:
   - `put(item)` - Add an item to the back of the queue.
   - `get()` - Remove and return the item at the front. Raises `IndexError` if empty.
   - `size()` - Return the current number of items.
   - `is_empty()` - Return True if the queue has no items.

2. **`BatchProcessor`** - Processes items from a Queue in batches:
   - `__init__(self, queue, batch_size)` - Takes a Queue instance and a batch size.
   - `process_batch()` - Removes up to `batch_size` items from the queue and returns them as a list. If fewer items are available, returns whatever is there. If queue is empty, returns an empty list `[]`.
   - `process_all()` - Processes all items in batches, returning a list of batches (each batch is a list). Stops when queue is empty.

## Interface Contract

- BatchProcessor must use Queue's `get()`, `size()`, and `is_empty()` methods (not access internal state directly).
- `process_batch()` on an empty queue returns `[]`, never raises.
- `process_all()` returns a list of non-empty batches. The last batch may be smaller than `batch_size`.
- Both classes must be in the same `solution.py` file.
