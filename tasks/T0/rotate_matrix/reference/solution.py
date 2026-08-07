def rotate_matrix(matrix: list) -> list:
    """Rotate an NxN matrix 90 degrees clockwise. Returns a new matrix."""
    if not matrix:
        return []
    n = len(matrix)
    return [[matrix[n - 1 - j][i] for j in range(n)] for i in range(n)]
