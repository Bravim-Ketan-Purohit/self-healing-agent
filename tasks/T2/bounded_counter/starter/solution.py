class BoundedCounter:
    """Thread-safe counter with min/max bounds."""

    def __init__(self, min_value: int = 0, max_value: int = 10, initial: int = 0):
        pass

    @property
    def value(self) -> int:
        pass

    @property
    def min_value(self) -> int:
        pass

    @property
    def max_value(self) -> int:
        pass

    def increment(self, amount: int = 1) -> int:
        pass

    def decrement(self, amount: int = 1) -> int:
        pass

    def reset(self) -> None:
        pass
