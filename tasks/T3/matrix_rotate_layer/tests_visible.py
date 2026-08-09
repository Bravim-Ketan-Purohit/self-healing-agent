from solution import rotate_outer_layer


def test_rotate_by_1():
    matrix = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]]
    expected = [[4, 1, 2],
                [7, 5, 3],
                [8, 9, 6]]
    assert rotate_outer_layer(matrix, 1) == expected


def test_rotate_by_2():
    matrix = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]]
    expected = [[7, 4, 1],
                [8, 5, 2],
                [9, 6, 3]]
    assert rotate_outer_layer(matrix, 2) == expected


def test_no_rotation():
    matrix = [[1, 2],
              [3, 4]]
    assert rotate_outer_layer(matrix, 0) == [[1, 2], [3, 4]]
