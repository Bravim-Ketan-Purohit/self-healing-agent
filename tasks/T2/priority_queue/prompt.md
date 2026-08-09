# Priority Queue

Implement a `PriorityQueue` class that models a min-heap priority queue with the following operations:

- `__init__(self)` — Create an empty priority queue.
- `push(self, item: str, priority: int) -> None` — Add an item with the given priority. If the item already exists, update its priority instead.
- `pop(self) -> str` — Remove and return the item with the lowest priority value. Raises `IndexError` if the queue is empty.
- `peek(self) -> str` — Return the item with the lowest priority value without removing it. Raises `IndexError` if the queue is empty.
- `update_priority(self, item: str, new_priority: int) -> None` — Change the priority of an existing item. Raises `KeyError` if the item does not exist.
- `__len__(self) -> int` — Return the number of items in the queue.
- `__contains__(self, item: str) -> bool` — Return True if the item is in the queue.

## Invariants

- `pop()` always returns the item with the minimum priority value.
- After `update_priority`, the heap ordering is maintained.
- No duplicate items exist in the queue at any time.

## Examples

```python
pq = PriorityQueue()
pq.push("task_a", 3)
pq.push("task_b", 1)
pq.push("task_c", 2)
pq.peek()   # "task_b"
pq.pop()    # "task_b"
pq.pop()    # "task_c"

pq.push("task_d", 10)
pq.update_priority("task_d", 0)
pq.peek()   # "task_d"
```
