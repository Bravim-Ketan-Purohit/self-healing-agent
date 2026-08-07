from solution import flatten_list


def test_empty_nested():
    assert flatten_list([[], [[]], [[], []]]) == []


def test_mixed_types():
    assert flatten_list([1, ["hello", 2.5], [True, [None]]]) == [1, "hello", 2.5, True, None]


def test_single_element():
    assert flatten_list([[[[42]]]]) == [42]


def test_large_flat():
    big = list(range(1000))
    assert flatten_list(big) == big


def test_large_nested():
    nested = list(range(100)) + [list(range(100, 200))]
    assert flatten_list(nested) == list(range(200))


def test_strings_not_expanded():
    assert flatten_list(["abc", ["def"]]) == ["abc", "def"]


def test_preserves_order():
    assert flatten_list([[3, 2], [1], [[0, -1]]]) == [3, 2, 1, 0, -1]


def test_nested_empty_and_values():
    assert flatten_list([[], 1, [2, [], [3, []]]]) == [1, 2, 3]
