from solution import split_bill


def test_sum_always_exact():
    """The sum must always equal the total, no rounding loss."""
    assert sum(split_bill(1000, 7)) == 1000


def test_sum_exact_prime_divisor():
    """Prime number of people, odd total."""
    result = split_bill(100, 7)
    assert sum(result) == 100
    assert max(result) - min(result) <= 1


def test_large_remainder():
    """Remainder of 6: first 6 people get +1."""
    result = split_bill(13, 7)
    assert sum(result) == 13
    assert result == [2, 2, 2, 2, 2, 2, 1]


def test_one_cent_total():
    """Only 1 cent split among many: one gets 1, rest get 0."""
    result = split_bill(1, 5)
    assert sum(result) == 1
    assert result == [1, 0, 0, 0, 0]


def test_zero_total():
    """Zero cents means everyone gets 0."""
    assert split_bill(0, 3) == [0, 0, 0]


def test_total_less_than_people():
    """Fewer cents than people: some get 1, rest get 0."""
    result = split_bill(3, 5)
    assert sum(result) == 3
    assert result == [1, 1, 1, 0, 0]


def test_no_float_drift():
    """Classic float trap: 10.00 / 3 = 3.333... Using int division avoids drift."""
    # 1000 cents / 3 = 333 remainder 1
    result = split_bill(1000, 3)
    assert sum(result) == 1000
    assert result == [334, 333, 333]


def test_large_values():
    """Large values should not suffer float precision issues."""
    result = split_bill(999999999, 7)
    assert sum(result) == 999999999
    assert max(result) - min(result) <= 1
