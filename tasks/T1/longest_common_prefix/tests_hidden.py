from solution import longest_common_prefix


def test_empty_list():
    assert longest_common_prefix([]) == ""


def test_list_with_empty_string():
    assert longest_common_prefix(["", "abc", "abd"]) == ""


def test_empty_string_in_middle():
    assert longest_common_prefix(["abc", "", "abd"]) == ""


def test_single_char_strings():
    assert longest_common_prefix(["a", "a", "a"]) == "a"


def test_no_common_single_chars():
    assert longest_common_prefix(["a", "b", "c"]) == ""


def test_prefix_is_shortest_string():
    assert longest_common_prefix(["ab", "abc", "abcd"]) == "ab"


def test_two_strings():
    assert longest_common_prefix(["interspecies", "interstellar"]) == "inters"


def test_all_identical():
    assert longest_common_prefix(["hello", "hello", "hello", "hello"]) == "hello"
