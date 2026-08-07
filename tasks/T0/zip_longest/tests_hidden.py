from solution import zip_longest


def test_empty_input():
    assert zip_longest() == []


def test_single_list():
    assert zip_longest([1, 2, 3]) == [(1,), (2,), (3,)]


def test_all_empty_lists():
    assert zip_longest([], [], []) == []


def test_one_empty_one_full():
    assert zip_longest([], [1, 2], fill=0) == [(0, 1), (0, 2)]


def test_string_fill():
    assert zip_longest([1, 2], [3], fill="x") == [(1, 3), (2, "x")]


def test_four_lists():
    result = zip_longest([1], [2], [3], [4], fill=0)
    assert result == [(1, 2, 3, 4)]


def test_large_difference():
    result = zip_longest([1], [2, 3, 4, 5, 6], fill=0)
    assert len(result) == 5
    assert result[-1] == (0, 6)


def test_none_elements_with_fill():
    assert zip_longest([None, None], [1], fill="?") == [(None, 1), (None, "?")]
