from solution import RateLimiter


def test_initial_burst():
    rl = RateLimiter(capacity=3, refill_rate=1.0)
    assert rl.allow(0.0) is True
    assert rl.allow(0.0) is True
    assert rl.allow(0.0) is True
    assert rl.allow(0.0) is False


def test_refill_over_time():
    rl = RateLimiter(capacity=2, refill_rate=1.0)
    rl.allow(0.0)
    rl.allow(0.0)
    assert rl.allow(0.0) is False
    assert rl.allow(1.0) is True  # 1 second passed, 1 token refilled


def test_long_gap_caps_at_capacity():
    rl = RateLimiter(capacity=3, refill_rate=1.0)
    rl.allow(0.0)  # 2 left
    # After 100 seconds, should refill to capacity (3), not 102
    assert rl.allow(100.0) is True
    assert rl.allow(100.0) is True
    assert rl.allow(100.0) is True
    assert rl.allow(100.0) is False
