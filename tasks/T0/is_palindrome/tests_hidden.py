from solution import is_palindrome


def test_empty_string():
    assert is_palindrome("") is True


def test_mixed_case():
    assert is_palindrome("Noon") is True


def test_numbers_in_string():
    assert is_palindrome("12321") is True


def test_numbers_not_palindrome():
    assert is_palindrome("12345") is False


def test_special_chars_only():
    assert is_palindrome("!!!") is True


def test_long_palindrome():
    assert is_palindrome("Was it a car or a cat I saw") is True


def test_spaces_only():
    assert is_palindrome("   ") is True


def test_two_characters_not_palindrome():
    assert is_palindrome("ab") is False
