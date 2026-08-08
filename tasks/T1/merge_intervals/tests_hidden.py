from solution import merge_intervals


def test_empty_list():
    assert merge_intervals([]) == []


def test_single_interval():
    assert merge_intervals([[5, 10]]) == [[5, 10]]


def test_all_overlapping():
    assert merge_intervals([[1,10],[2,5],[3,7],[6,9]]) == [[1,10]]


def test_contained_interval():
    # [2,3] is fully contained within [1,5]
    assert merge_intervals([[1,5],[2,3]]) == [[1,5]]


def test_same_start_different_end():
    assert merge_intervals([[1,4],[1,6],[1,2]]) == [[1,6]]


def test_negative_intervals():
    assert merge_intervals([[-5,-1],[0,3],[-3,2]]) == [[-5,3]]


def test_single_point_intervals():
    assert merge_intervals([[1,1],[2,2],[3,3]]) == [[1,1],[2,2],[3,3]]


def test_large_unsorted():
    intervals = [[10,12],[1,3],[5,8],[2,6],[15,18]]
    assert merge_intervals(intervals) == [[1,8],[10,12],[15,18]]
