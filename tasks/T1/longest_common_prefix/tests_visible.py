from solution import longest_common_prefix


def test_common_prefix():
    assert longest_common_prefix(["flower", "flow", "flight"]) == "fl"


def test_no_common_prefix():
    assert longest_common_prefix(["dog", "racecar", "car"]) == ""


def test_full_match():
    assert longest_common_prefix(["test", "test", "test"]) == "test"


def test_single_string():
    assert longest_common_prefix(["alone"]) == "alone"
