from solution import chunk_list


def test_basic_chunking():
    assert chunk_list([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]


def test_exact_division():
    assert chunk_list([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]


def test_chunk_size_one():
    assert chunk_list([1, 2, 3], 1) == [[1], [2], [3]]


def test_chunk_larger_than_list():
    assert chunk_list([1, 2], 5) == [[1, 2]]
