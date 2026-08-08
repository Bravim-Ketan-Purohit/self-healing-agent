import pytest
from solution import two_sum


def test_negative_numbers():
    assert two_sum([-1, -2, -3, -4, -5], -8) == [2, 4]


def test_mixed_positive_negative():
    assert two_sum([-3, 4, 3, 90], 0) == [0, 2]


def test_zero_target():
    assert two_sum([0, 4, 3, 0], 0) == [0, 3]


def test_large_numbers():
    assert two_sum([1000000, 500000, -1000000, 0], 0) == [0, 2]


def test_single_element_raises():
    with pytest.raises(ValueError):
        two_sum([1], 2)


def test_empty_list_raises():
    with pytest.raises(ValueError):
        two_sum([], 0)


def test_pair_at_end():
    assert two_sum([1, 2, 3, 4, 5, 6], 11) == [4, 5]


def test_result_is_sorted():
    result = two_sum([15, 11, 7, 2], 9)
    assert result == sorted(result)
    assert result == [2, 3]
