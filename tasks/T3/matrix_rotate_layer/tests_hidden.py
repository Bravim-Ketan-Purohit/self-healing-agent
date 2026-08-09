from solution import rotate_outer_layer


def test_full_rotation_returns_same():
    """k == perimeter means full rotation, matrix unchanged."""
    matrix = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]]
    assert rotate_outer_layer(matrix, 8) == matrix


def test_k_greater_than_perimeter():
    """k > perimeter should wrap with modulo."""
    matrix = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]]
    # perimeter = 8, k=9 is same as k=1
    assert rotate_outer_layer(matrix, 9) == rotate_outer_layer(matrix, 1)


def test_k_much_larger_than_perimeter():
    """Very large k wraps correctly."""
    matrix = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]]
    # perimeter = 8, k=800 is same as k=0
    assert rotate_outer_layer(matrix, 800) == matrix


def test_no_mutation():
    """Original matrix must not be mutated."""
    matrix = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]]
    original = [row[:] for row in matrix]
    rotate_outer_layer(matrix, 2)
    assert matrix == original


def test_rectangular_matrix():
    """Works for non-square matrix."""
    matrix = [[1, 2, 3, 4],
              [5, 6, 7, 8],
              [9, 10, 11, 12]]
    # perimeter = 2*(4+3)-4 = 10
    expected = [[5, 1, 2, 3],
                [9, 6, 7, 4],
                [10, 11, 12, 8]]
    assert rotate_outer_layer(matrix, 1) == expected


def test_single_row():
    """1xN matrix rotation."""
    matrix = [[1, 2, 3, 4]]
    # perimeter = 4, rotating by 1
    expected = [[4, 1, 2, 3]]
    assert rotate_outer_layer(matrix, 1) == expected


def test_single_column():
    """Nx1 matrix rotation."""
    matrix = [[1], [2], [3], [4]]
    # perimeter = 4, rotating by 1
    expected = [[4], [1], [2], [3]]
    assert rotate_outer_layer(matrix, 1) == expected


def test_2x2_full_rotation():
    """2x2 matrix, perimeter=4."""
    matrix = [[1, 2],
              [3, 4]]
    assert rotate_outer_layer(matrix, 4) == [[1, 2], [3, 4]]
    assert rotate_outer_layer(matrix, 5) == rotate_outer_layer(matrix, 1)
