from solution import spiral_order


def test_single_row():
    assert spiral_order([[1, 2, 3, 4, 5]]) == [1, 2, 3, 4, 5]


def test_single_column():
    assert spiral_order([[1],[2],[3],[4]]) == [1, 2, 3, 4]


def test_2x2():
    assert spiral_order([[1,2],[3,4]]) == [1, 2, 4, 3]


def test_4x3():
    matrix = [[1,2,3],[4,5,6],[7,8,9],[10,11,12]]
    assert spiral_order(matrix) == [1,2,3,6,9,12,11,10,7,4,5,8]


def test_2x4():
    matrix = [[1,2,3,4],[5,6,7,8]]
    assert spiral_order(matrix) == [1,2,3,4,8,7,6,5]


def test_empty_rows():
    assert spiral_order([[]]) == []


def test_1x2():
    assert spiral_order([[1, 2]]) == [1, 2]


def test_2x1():
    assert spiral_order([[1],[2]]) == [1, 2]
