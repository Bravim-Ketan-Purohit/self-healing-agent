from solution import rotate_matrix


def test_2x2():
    assert rotate_matrix([[1, 2], [3, 4]]) == [[3, 1], [4, 2]]


def test_3x3():
    assert rotate_matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == [[7, 4, 1], [8, 5, 2], [9, 6, 3]]


def test_1x1():
    assert rotate_matrix([[1]]) == [[1]]


def test_empty():
    assert rotate_matrix([]) == []
