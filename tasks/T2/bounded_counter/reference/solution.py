import threading


class BoundedCounter:
    """Thread-safe counter with min/max bounds."""

    def __init__(self, min_value: int = 0, max_value: int = 10, initial: int = 0):
        if min_value > max_value:
            raise ValueError("min_value must be <= max_value")
        if not (min_value <= initial <= max_value):
            raise ValueError("initial must be within [min_value, max_value]")
        self._value = initial
        self._min = min_value
        self._max = max_value
        self._lock = threading.Lock()

    @property
    def value(self) -> int:
        with self._lock:
            return self._value

    @property
    def min_value(self) -> int:
        return self._min

    @property
    def max_value(self) -> int:
        return self._max

    def increment(self, amount: int = 1) -> int:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        with self._lock:
            new_value = self._value + amount
            if new_value > self._max:
                raise OverflowError(
                    f"Increment would exceed max_value ({self._max})"
                )
            self._value = new_value
            return self._value

    def decrement(self, amount: int = 1) -> int:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        with self._lock:
            new_value = self._value - amount
            if new_value < self._min:
                raise OverflowError(
                    f"Decrement would go below min_value ({self._min})"
                )
            self._value = new_value
            return self._value

    def reset(self) -> None:
        with self._lock:
            self._value = self._min
