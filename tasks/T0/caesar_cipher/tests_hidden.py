from solution import caesar_cipher


def test_negative_shift():
    assert caesar_cipher("bcd", -1) == "abc"


def test_zero_shift():
    assert caesar_cipher("hello", 0) == "hello"


def test_full_rotation():
    assert caesar_cipher("abc", 26) == "abc"


def test_large_shift():
    assert caesar_cipher("abc", 52) == "abc"


def test_mixed_content():
    assert caesar_cipher("Hello, World! 123", 13) == "Uryyb, Jbeyq! 123"


def test_empty_string():
    assert caesar_cipher("", 5) == ""


def test_all_uppercase():
    assert caesar_cipher("XYZ", 2) == "ZAB"


def test_negative_large_shift():
    assert caesar_cipher("abc", -27) == "zab"
