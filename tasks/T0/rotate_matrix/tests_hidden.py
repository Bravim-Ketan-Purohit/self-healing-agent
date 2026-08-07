from solution import rotate_matrix


def test_4x4():
    matrix = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
    expected = [[13, 9, 5, 1], [14, 10, 6, 2], [15, 11, 7, 3], [16, 12, 8, 4]]
    assert rotate_matrix(matrix) == expected


def test_does_not_modify_original():
    matrix = [[1, 2], [3, 4]]
    original_copy = [row[:] for row in matrix]
    rotate_matrix(matrix)
    assert matrix == original_copy


def test_four_rotations_identity():
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    result = matrix
    for _ in range(4):
        result = rotate_matrix(result)
    assert result == matrix


def test_negative_numbers():
    assert rotate_matrix([[-1, -2], [-3, -4]]) == [[-3, -1], [-4, -2]]


def test_5x5():
    matrix = [[i * 5 + j for j in range(5)] for i in range(5)]
    result = rotate_matrix(matrix)
    assert result[0] == [20, 15, 10, 5, 0]
    assert result[4] == [24, 19, 14, 9, 4]


def test_zeros():
    assert rotate_matrix([[0, 0], [0, 0]]) == [[0, 0], [0, 0]]
