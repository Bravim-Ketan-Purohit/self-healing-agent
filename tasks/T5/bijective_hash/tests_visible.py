from solution import bijective_hash


def test_deterministic():
    assert bijective_hash("hello") == bijective_hash("hello")
    assert bijective_hash("") == bijective_hash("")


def test_different_strings_different_hashes():
    assert bijective_hash("hello") != bijective_hash("world")
    assert bijective_hash("abc") != bijective_hash("abd")


def test_output_range():
    h = bijective_hash("test")
    assert 0 <= h <= 2**32 - 1


def test_empty_string():
    h = bijective_hash("")
    assert isinstance(h, int)
    assert 0 <= h <= 2**32 - 1
