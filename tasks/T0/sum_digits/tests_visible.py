from solution import sum_digits


def test_basic():
    assert sum_digits("abc123") == 6


def test_no_digits():
    assert sum_digits("hello") == 0


def test_all_digits():
    assert sum_digits("99") == 18


def test_mixed():
    assert sum_digits("1a2b3c") == 6
