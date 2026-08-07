from solution import zip_longest


def test_basic():
    assert zip_longest([1, 2, 3], [4, 5], fill=0) == [(1, 4), (2, 5), (3, 0)]


def test_equal_length():
    assert zip_longest([1, 2], [3, 4]) == [(1, 3), (2, 4)]


def test_default_fill():
    assert zip_longest([1, 2, 3], [4]) == [(1, 4), (2, None), (3, None)]


def test_three_lists():
    assert zip_longest([1], [2, 3], [4, 5, 6], fill=-1) == [(1, 2, 4), (-1, 3, 5), (-1, -1, 6)]
