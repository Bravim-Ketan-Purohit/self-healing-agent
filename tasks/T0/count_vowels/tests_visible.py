from solution import count_vowels


def test_basic():
    assert count_vowels("hello") == 2


def test_all_vowels():
    assert count_vowels("aeiou") == 5


def test_uppercase():
    assert count_vowels("HELLO") == 2


def test_no_vowels():
    assert count_vowels("xyz") == 0
