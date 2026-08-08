from solution import roman_to_int


def test_one():
    assert roman_to_int("I") == 1


def test_ix():
    assert roman_to_int("IX") == 9


def test_xl():
    assert roman_to_int("XL") == 40


def test_xc():
    assert roman_to_int("XC") == 90


def test_cd():
    assert roman_to_int("CD") == 400


def test_cm():
    assert roman_to_int("CM") == 900


def test_max_value():
    assert roman_to_int("MMMCMXCIX") == 3999


def test_all_subtractive():
    assert roman_to_int("CDXLIV") == 444
