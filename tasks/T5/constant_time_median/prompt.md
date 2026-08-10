# Constant Time Median

Implement a class `MedianCollection` that maintains a dynamic collection of numbers supporting the following operations, all in **O(1)** worst-case time:

## API

```python
class MedianCollection:
    def __init__(self):
        ...

    def add(self, value: int) -> None:
        """Add a value to the collection. O(1) time."""

    def remove(self, value: int) -> None:
        """Remove one occurrence of value. Raises ValueError if not present. O(1) time."""

    def median(self) -> float:
        """Return the median of the collection. O(1) time.
        For even number of elements, return average of two middle values.
        Raises ValueError if collection is empty."""

    def size(self) -> int:
        """Return the number of elements. O(1) time."""
```

## Requirements

1. All four operations must be O(1) worst-case time complexity
2. The collection supports duplicate values
3. Values can be any integer (positive, negative, or zero)
4. The median calculation must be exact (not approximate)

## Example

```python
>>> mc = MedianCollection()
>>> mc.add(3)
>>> mc.add(1)
>>> mc.add(2)
>>> mc.median()
2
>>> mc.add(4)
>>> mc.median()
2.5
>>> mc.remove(1)
>>> mc.median()
3
```
