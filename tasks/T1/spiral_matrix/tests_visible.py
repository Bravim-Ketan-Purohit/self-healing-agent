from solution import spiral_order


def test_3x3():
    matrix = [[1,2,3],[4,5,6],[7,8,9]]
    assert spiral_order(matrix) == [1,2,3,6,9,8,7,4,5]


def test_3x4():
    matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
    assert spiral_order(matrix) == [1,2,3,4,8,12,11,10,9,5,6,7]


def test_1x1():
    assert spiral_order([[1]]) == [1]


def test_empty():
    assert spiral_order([]) == []
