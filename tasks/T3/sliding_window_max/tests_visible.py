from solution import sliding_max


def test_basic():
    assert sliding_max([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]


def test_k_equals_one():
    assert sliding_max([4, 2, 7, 1], 1) == [4, 2, 7, 1]


def test_k_equals_length():
    assert sliding_max([3, 1, 4, 1, 5], 5) == [5]


def test_ascending():
    assert sliding_max([1, 2, 3, 4, 5], 3) == [3, 4, 5]
