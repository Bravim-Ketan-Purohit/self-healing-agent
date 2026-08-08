from solution import group_anagrams


def test_basic_grouping():
    result = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    sorted_result = sorted([sorted(g) for g in result])
    assert sorted_result == [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]]


def test_single_string():
    assert group_anagrams(["a"]) == [["a"]]


def test_empty_string():
    assert group_anagrams([""]) == [[""]]


def test_no_anagrams():
    result = group_anagrams(["abc", "def", "ghi"])
    sorted_result = sorted([sorted(g) for g in result])
    assert sorted_result == [["abc"], ["def"], ["ghi"]]
