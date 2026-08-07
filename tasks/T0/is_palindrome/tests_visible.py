from solution import is_palindrome


def test_simple_palindrome():
    assert is_palindrome("racecar") is True


def test_not_palindrome():
    assert is_palindrome("hello") is False


def test_with_spaces_and_punctuation():
    assert is_palindrome("A man, a plan, a canal: Panama") is True


def test_single_character():
    assert is_palindrome("a") is True
