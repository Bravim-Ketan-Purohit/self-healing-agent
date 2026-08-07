from solution import caesar_cipher


def test_basic_shift():
    assert caesar_cipher("abc", 1) == "bcd"


def test_wrap_around():
    assert caesar_cipher("xyz", 3) == "abc"


def test_preserve_case():
    assert caesar_cipher("Hello", 5) == "Mjqqt"


def test_non_alpha_unchanged():
    assert caesar_cipher("a-b-c", 2) == "c-d-e"
