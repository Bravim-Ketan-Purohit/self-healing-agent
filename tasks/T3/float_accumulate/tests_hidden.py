from solution import precise_sum


def test_repeated_tenths():
    """[0.1] * 10 should sum to exactly 1.0 within tolerance."""
    result = precise_sum([0.1] * 10)
    assert abs(result - 1.0) < 1e-10


def test_catastrophic_cancellation():
    """Large + small - large: manual accumulators lose the small value."""
    numbers = []
    for _ in range(10000):
        numbers.append(1e16)
        numbers.append(-1e16)
        numbers.append(0.0001)
    result = precise_sum(numbers)
    assert abs(result - 1.0) < 1e-10


def test_alternating_large_small():
    """Alternating large positive and negative with small residuals."""
    numbers = []
    for _ in range(5000):
        numbers.append(1e15)
        numbers.append(0.0001)
        numbers.append(-1e15)
    result = precise_sum(numbers)
    assert abs(result - 0.5) < 1e-10


def test_many_small_values():
    """Summing many small values that should not drift."""
    result = precise_sum([1e-10] * 1000000)
    assert abs(result - 1e-4) < 1e-10


def test_kahan_adversarial():
    """Values designed to expose naive left-to-right accumulation drift."""
    # Interleave huge values with tiny corrections
    numbers = [1e16, 1.0, 1.0, 1.0, -1e16]
    result = precise_sum(numbers)
    assert abs(result - 3.0) < 1e-10


def test_negative_values():
    """Mix of negative floats summed precisely."""
    result = precise_sum([-0.1] * 10)
    assert abs(result - (-1.0)) < 1e-10


def test_mixed_signs_cancel_large():
    """Many values that should cancel to a specific result."""
    # 50k pairs of +1e14 and -1e14 with a 0.01 added each time
    numbers = []
    for _ in range(50000):
        numbers.extend([1e14, -1e14, 0.01])
    result = precise_sum(numbers)
    assert abs(result - 500.0) < 1e-10


def test_conditioned_sum():
    """Sum where ordering matters for naive accumulators."""
    # Start with a big number, add tiny increments that get swallowed
    numbers = [1e16] + [1.0] * 100 + [-1e16]
    result = precise_sum(numbers)
    assert abs(result - 100.0) < 1e-10
