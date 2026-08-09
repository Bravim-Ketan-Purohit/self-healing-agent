class RateLimiter:
    """Token bucket rate limiter."""

    def __init__(self, capacity: int, refill_rate: float):
        if capacity < 1:
            raise ValueError("Capacity must be at least 1")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
        self._capacity = capacity
        self._refill_rate = refill_rate
        self._tokens = float(capacity)  # starts full
        self._last_timestamp = None

    def allow(self, timestamp: float) -> bool:
        if self._last_timestamp is not None:
            elapsed = timestamp - self._last_timestamp
            if elapsed > 0:
                self._tokens += elapsed * self._refill_rate
                if self._tokens > self._capacity:
                    self._tokens = self._capacity
        self._last_timestamp = timestamp

        if self._tokens >= 1.0:
            self._tokens -= 1.0
            return True
        return False
