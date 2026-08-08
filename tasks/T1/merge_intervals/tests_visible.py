from solution import merge_intervals


def test_basic_merge():
    assert merge_intervals([[1,3],[2,6],[8,10],[15,18]]) == [[1,6],[8,10],[15,18]]


def test_touching_intervals():
    assert merge_intervals([[1,4],[4,5]]) == [[1,5]]


def test_no_overlap():
    assert merge_intervals([[1,2],[5,6],[9,10]]) == [[1,2],[5,6],[9,10]]


def test_unsorted_input():
    assert merge_intervals([[3,4],[1,2],[5,6]]) == [[1,2],[3,4],[5,6]]
