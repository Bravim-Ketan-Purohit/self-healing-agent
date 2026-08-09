from solution import RateLimiter
import pytest


def test_tokens_never_exceed_capacity():
    """Invariant: tokens are capped at capacity regardless of time elapsed."""
    rl = RateLimiter(capacity=5, refill_rate=10.0)
    # Drain all tokens
    for _ in range(5):
        rl.allow(0.0)
    # Wait a very long time (1000 seconds at rate 10 = 10000 tokens, but capped at 5)
    for _ in range(5):
        assert rl.allow(1000.0) is True
    assert rl.allow(1000.0) is False  # exactly 5 were available


def test_fractional_token_accumulation():
    """Invariant: partial tokens accumulate correctly over multiple calls."""
    rl = RateLimiter(capacity=1, refill_rate=2.0)  # 2 tokens/sec
    rl.allow(0.0)  # consume the 1 token
    assert rl.allow(0.0) is False  # 0 tokens
    assert rl.allow(0.3) is False  # 0.6 tokens (not enough for 1)
    assert rl.allow(0.5) is True   # 0.6 + 0.4 = 1.0 tokens -> consume -> 0


def test_exact_boundary_token():
    """Invariant: exactly 1.0 token available means allow succeeds."""
    rl = RateLimiter(capacity=5, refill_rate=1.0)
    # Drain all
    for _ in range(5):
        rl.allow(0.0)
    # Wait exactly 1 second -> exactly 1 token
    assert rl.allow(1.0) is True
    assert rl.allow(1.0) is False  # no time passed, 0 tokens


def test_rapid_fire_after_partial_refill():
    """Invariant: partial tokens don't grant a full request."""
    rl = RateLimiter(capacity=2, refill_rate=1.0)
    rl.allow(0.0)
    rl.allow(0.0)
    # 0.5 sec -> 0.5 tokens, not enough
    assert rl.allow(0.5) is False
    # another 0.5 sec -> 0.5 + 0.5 = 1.0 tokens, enough
    assert rl.allow(1.0) is True


def test_high_refill_rate():
    """Invariant: high refill rate refills quickly but still caps."""
    rl = RateLimiter(capacity=3, refill_rate=100.0)
    rl.allow(0.0)
    rl.allow(0.0)
    rl.allow(0.0)
    # 0.01 sec at rate 100 = 1 token
    assert rl.allow(0.01) is True
    assert rl.allow(0.01) is False  # no more time elapsed


def test_invalid_construction_raises():
    """Invariant: invalid parameters are rejected."""
    with pytest.raises(ValueError):
        RateLimiter(capacity=0, refill_rate=1.0)
    with pytest.raises(ValueError):
        RateLimiter(capacity=-1, refill_rate=1.0)
    with pytest.raises(ValueError):
        RateLimiter(capacity=5, refill_rate=0)
    with pytest.raises(ValueError):
        RateLimiter(capacity=5, refill_rate=-1.0)


def test_sequence_of_allow_calls_consistency():
    """Invariant: state is consistent through a realistic call sequence."""
    rl = RateLimiter(capacity=10, refill_rate=2.0)
    # Burst 10 at t=0
    results = [rl.allow(0.0) for _ in range(12)]
    assert results[:10] == [True] * 10
    assert results[10:] == [False] * 2
    # Wait 3 seconds -> +6 tokens
    results = [rl.allow(3.0) for _ in range(8)]
    assert results[:6] == [True] * 6
    assert results[6:] == [False] * 2


def test_monotonic_timestamp_not_required_but_handled():
    """Invariant: if same timestamp is repeated, no extra tokens are generated."""
    rl = RateLimiter(capacity=2, refill_rate=1.0)
    assert rl.allow(5.0) is True
    assert rl.allow(5.0) is True
    assert rl.allow(5.0) is False
    # Same timestamp again - still no tokens
    assert rl.allow(5.0) is False
