from solution import repeat_join


def test_basic_repeat():
    assert repeat_join("ha", 3, "-") == "ha-ha-ha"


def test_single_repeat():
    assert repeat_join("ab", 1, ",") == "ab"


def test_empty_separator():
    assert repeat_join("x", 5, "") == "xxxxx"


def test_zero_repeats():
    assert repeat_join("hi", 0, "-") == ""
