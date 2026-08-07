from solution import flatten_list


def test_basic():
    assert flatten_list([1, [2, 3], [4, [5, 6]]]) == [1, 2, 3, 4, 5, 6]


def test_already_flat():
    assert flatten_list([1, 2, 3]) == [1, 2, 3]


def test_deeply_nested():
    assert flatten_list([[1, [2, [3, [4]]]]]) == [1, 2, 3, 4]


def test_empty():
    assert flatten_list([]) == []
