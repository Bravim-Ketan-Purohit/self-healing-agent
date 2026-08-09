# Rate Limiter (Token Bucket)

Implement a `RateLimiter` class using the token bucket algorithm:

- `__init__(self, capacity: int, refill_rate: float)` — Create a rate limiter with a maximum token `capacity` and a `refill_rate` (tokens added per second). The bucket starts full. Raises `ValueError` if capacity < 1 or refill_rate <= 0.
- `allow(self, timestamp: float) -> bool` — Called at the given timestamp (in seconds). Refills tokens based on elapsed time since the last call (capped at capacity), then attempts to consume one token. Returns `True` if a token was available (request allowed), `False` otherwise.

## Invariants

- Token count never exceeds `capacity`.
- Token count never goes below 0.
- Tokens refill proportionally to elapsed time at `refill_rate` tokens/second.
- After a long idle period, the bucket refills to at most `capacity` (not beyond).

## Examples

```python
rl = RateLimiter(capacity=3, refill_rate=1.0)  # 3 tokens max, 1 token/sec

rl.allow(0.0)  # True (3 -> 2 tokens)
rl.allow(0.0)  # True (2 -> 1 tokens)
rl.allow(0.0)  # True (1 -> 0 tokens)
rl.allow(0.0)  # False (0 tokens, no time to refill)

rl.allow(2.5)  # True (2.5 sec passed, +2.5 -> 2.5 tokens, consume 1 -> 1.5)
rl.allow(2.5)  # True (0 sec passed, 1.5 -> consume 1 -> 0.5)
rl.allow(2.5)  # False (0.5 tokens, not enough)
```
