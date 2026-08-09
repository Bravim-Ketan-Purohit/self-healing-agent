# Observable List

Implement an `ObservableList` class that wraps a list and notifies registered callbacks whenever the list is mutated:

- `__init__(self, initial: list = None)` — Create the list with optional initial items. No notifications for initial items.
- `subscribe(self, callback: callable) -> None` — Register a callback that will be called on mutations.
- `unsubscribe(self, callback: callable) -> None` — Remove a callback. Raises `ValueError` if callback is not registered.
- `insert(self, index: int, item) -> None` — Insert item at index and notify callbacks with `("insert", index, item)`.
- `remove(self, index: int) -> None` — Remove item at index and notify callbacks with `("remove", index, removed_item)`. Raises `IndexError` if index is out of range.
- `set(self, index: int, item) -> None` — Replace item at index and notify callbacks with `("set", index, item)`. Raises `IndexError` if index is out of range.
- `get(self, index: int)` — Return item at index. Raises `IndexError` if out of range.
- `__len__(self) -> int` — Return the number of items.
- `to_list(self) -> list` — Return a copy of the internal list.

## Invariants

- Callbacks always receive the correct index after mutations (e.g., inserting at index 0 shifts all subsequent items).
- The notification tuple always reflects the actual operation performed.
- After unsubscribe, the callback is never called again.

## Examples

```python
log = []
obs = ObservableList([1, 2, 3])
obs.subscribe(lambda event: log.append(event))
obs.insert(0, "x")      # log: [("insert", 0, "x")]
obs.to_list()            # ["x", 1, 2, 3]
obs.remove(2)            # log: [("insert", 0, "x"), ("remove", 2, 2)]
obs.to_list()            # ["x", 1, 3]
obs.set(1, "y")          # log: [..., ("set", 1, "y")]
obs.to_list()            # ["x", "y", 3]
```
