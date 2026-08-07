from solution import remove_duplicates


def test_no_duplicates():
    assert remove_duplicates([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]


def test_mixed_types():
    assert remove_duplicates([1, "1", 1, "1", True]) == [1, "1"]


def test_large_list():
    lst = list(range(500)) * 3
    assert remove_duplicates(lst) == list(range(500))


def test_preserves_first_occurrence_order():
    assert remove_duplicates([5, 3, 1, 3, 5, 7]) == [5, 3, 1, 7]


def test_single_element():
    assert remove_duplicates([42]) == [42]


def test_booleans_and_ints():
    # In Python, True == 1 and False == 0
    assert remove_duplicates([True, 1, False, 0]) == [True, False]


def test_none_values():
    assert remove_duplicates([None, 1, None, 2]) == [None, 1, 2]


def test_tuples_as_elements():
    assert remove_duplicates([(1, 2), (3, 4), (1, 2)]) == [(1, 2), (3, 4)]
