from solution import sum_digits


def test_empty_string():
    assert sum_digits("") == 0


def test_only_digits():
    assert sum_digits("1234567890") == 45


def test_spaces_and_digits():
    assert sum_digits("1 2 3 4 5") == 15


def test_special_characters():
    assert sum_digits("!@#1$%^2&*()3") == 6


def test_large_string():
    s = "a1" * 5000
    assert sum_digits(s) == 5000


def test_leading_zeros():
    assert sum_digits("007") == 7


def test_unicode_with_digits():
    assert sum_digits("café5résumé3") == 8


def test_single_digit():
    assert sum_digits("x5x") == 5
