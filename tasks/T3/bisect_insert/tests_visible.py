from solution import insert_sorted


def test_insert_middle():
    assert insert_sorted([1, 3, 5, 7], 4) == [1, 3, 4, 5, 7]


def test_insert_beginning():
    assert insert_sorted([1, 3, 5, 7], 0) == [0, 1, 3, 5, 7]


def test_insert_end():
    assert insert_sorted([1, 3, 5, 7], 8) == [1, 3, 5, 7, 8]


def test_insert_empty():
    assert insert_sorted([], 5) == [5]
