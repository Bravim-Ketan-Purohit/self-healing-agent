# Bounded Counter

Implement a `BoundedCounter` class that models a thread-safe counter with enforced min/max bounds:

- `__init__(self, min_value: int = 0, max_value: int = 10, initial: int = 0)` — Create a counter with bounds and initial value. Raises `ValueError` if min_value > max_value or initial is out of [min_value, max_value].
- `increment(self, amount: int = 1) -> int` — Increase the value by amount and return the new value. Raises `ValueError` if amount <= 0. Raises `OverflowError` if the result would exceed max_value.
- `decrement(self, amount: int = 1) -> int` — Decrease the value by amount and return the new value. Raises `ValueError` if amount <= 0. Raises `OverflowError` if the result would go below min_value.
- `reset(self) -> None` — Reset the value to min_value.
- `value` — Property returning the current value.
- `min_value` — Property returning the minimum bound.
- `max_value` — Property returning the maximum bound.

The counter must be thread-safe: concurrent increments and decrements must never leave the value outside [min_value, max_value].

## Invariants

- The value is always within [min_value, max_value].
- A failed operation (would breach bounds) leaves the value unchanged.
- Thread-safe: concurrent access preserves the bounds invariant.

## Examples

```python
c = BoundedCounter(0, 10, 5)
c.increment(3)   # returns 8
c.increment(3)   # raises OverflowError (8+3=11 > 10)
c.value          # 8
c.decrement(9)   # raises OverflowError (8-9=-1 < 0)
c.value          # 8
c.reset()
c.value          # 0
```
