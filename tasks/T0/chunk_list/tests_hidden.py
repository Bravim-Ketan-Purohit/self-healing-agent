import pytest
from solution import chunk_list


def test_empty_list():
    assert chunk_list([], 3) == []


def test_single_element():
    assert chunk_list([42], 1) == [[42]]


def test_strings():
    assert chunk_list(["a", "b", "c", "d"], 3) == [["a", "b", "c"], ["d"]]


def test_invalid_chunk_size_zero():
    with pytest.raises(ValueError):
        chunk_list([1, 2, 3], 0)


def test_invalid_chunk_size_negative():
    with pytest.raises(ValueError):
        chunk_list([1, 2], -1)


def test_large_list():
    result = chunk_list(list(range(100)), 10)
    assert len(result) == 10
    assert result[0] == list(range(10))


def test_chunk_size_equals_length():
    assert chunk_list([1, 2, 3], 3) == [[1, 2, 3]]


def test_mixed_types():
    assert chunk_list([1, "a", 2, "b"], 2) == [[1, "a"], [2, "b"]]
