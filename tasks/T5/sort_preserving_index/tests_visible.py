from solution import sort_preserving_index


def test_basic_sort():
    sorted_list, index_map = sort_preserving_index([3, 1, 2])
    assert sorted_list == [1, 2, 3]
    assert index_map == [1, 2, 0]


def test_already_sorted():
    sorted_list, index_map = sort_preserving_index([1, 2, 3])
    assert sorted_list == [1, 2, 3]
    assert index_map == [0, 1, 2]


def test_duplicates_stable():
    sorted_list, index_map = sort_preserving_index([5, 5, 5])
    assert sorted_list == [5, 5, 5]
    assert index_map == [0, 1, 2]


def test_reverse_sorted():
    sorted_list, index_map = sort_preserving_index([4, 3, 2, 1])
    assert sorted_list == [1, 2, 3, 4]
    assert index_map == [3, 2, 1, 0]
