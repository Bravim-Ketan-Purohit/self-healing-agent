from solution import run_length_encode


def test_basic():
    assert run_length_encode("aaabbc") == "3a2b1c"


def test_single_char():
    assert run_length_encode("a") == "1a"


def test_no_repeats():
    assert run_length_encode("abc") == "1a1b1c"


def test_all_same():
    assert run_length_encode("aaaa") == "4a"
