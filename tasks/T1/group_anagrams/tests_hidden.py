from solution import group_anagrams


def test_empty_list():
    assert group_anagrams([]) == []


def test_all_anagrams():
    result = group_anagrams(["abc", "bca", "cab", "acb"])
    assert len(result) == 1
    assert sorted(result[0]) == ["abc", "acb", "bca", "cab"]


def test_multiple_empty_strings():
    result = group_anagrams(["", "", ""])
    assert len(result) == 1
    assert result[0] == ["", "", ""]


def test_same_length_different_chars():
    result = group_anagrams(["ab", "cd", "ba", "dc"])
    sorted_result = sorted([sorted(g) for g in result])
    assert sorted_result == [["ab", "ba"], ["cd", "dc"]]


def test_single_char_strings():
    result = group_anagrams(["a", "b", "a", "c", "b"])
    sorted_result = sorted([sorted(g) for g in result])
    assert sorted_result == [["a", "a"], ["b", "b"], ["c"]]


def test_different_lengths():
    result = group_anagrams(["a", "ab", "abc"])
    sorted_result = sorted([sorted(g) for g in result])
    assert sorted_result == [["a"], ["ab"], ["abc"]]


def test_repeated_chars():
    result = group_anagrams(["aab", "aba", "baa", "abb"])
    sorted_result = sorted([sorted(g) for g in result])
    assert sorted_result == [["aab", "aba", "baa"], ["abb"]]


def test_large_group():
    words = ["listen", "silent", "enlist", "inlets", "tinsel"]
    result = group_anagrams(words)
    assert len(result) == 1
    assert sorted(result[0]) == sorted(words)
