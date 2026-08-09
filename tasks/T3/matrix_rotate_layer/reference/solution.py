def rotate_outer_layer(matrix: list[list[int]], k: int) -> list[list[int]]:
    """Rotate the outer layer of matrix by k positions clockwise. Returns new matrix."""
    if not matrix or not matrix[0]:
        return [row[:] for row in matrix]

    rows = len(matrix)
    cols = len(matrix[0])

    # Deep copy
    result = [row[:] for row in matrix]

    # Extract outer layer elements in clockwise order
    layer = []
    # Top row left to right
    for c in range(cols):
        layer.append(matrix[0][c])
    # Right column top+1 to bottom
    for r in range(1, rows):
        layer.append(matrix[r][cols - 1])
    # Bottom row right-1 to left (if more than one row)
    if rows > 1:
        for c in range(cols - 2, -1, -1):
            layer.append(matrix[rows - 1][c])
    # Left column bottom-1 to top+1 (if more than one col)
    if cols > 1:
        for r in range(rows - 2, 0, -1):
            layer.append(matrix[r][0])

    perimeter = len(layer)
    if perimeter == 0:
        return result

    # Wrap k with modulo
    k = k % perimeter

    # Rotate: shift elements by k positions (clockwise means each element
    # moves k positions forward, so new position i gets old element at (i - k) % perimeter)
    rotated = [layer[(i - k) % perimeter] for i in range(perimeter)]

    # Place rotated elements back
    idx = 0
    for c in range(cols):
        result[0][c] = rotated[idx]
        idx += 1
    for r in range(1, rows):
        result[r][cols - 1] = rotated[idx]
        idx += 1
    if rows > 1:
        for c in range(cols - 2, -1, -1):
            result[rows - 1][c] = rotated[idx]
            idx += 1
    if cols > 1:
        for r in range(rows - 2, 0, -1):
            result[r][0] = rotated[idx]
            idx += 1

    return result
