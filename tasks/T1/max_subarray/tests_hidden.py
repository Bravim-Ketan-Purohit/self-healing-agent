from solution import max_subarray


def test_single_negative():
    assert max_subarray([-5]) == -5


def test_single_zero():
    assert max_subarray([0]) == 0


def test_zeros_and_negatives():
    assert max_subarray([-3, 0, -2, 0, -1]) == 0


def test_large_negative_then_positive():
    assert max_subarray([-100, 50, -1, 50]) == 99


def test_alternating():
    assert max_subarray([2, -1, 2, -1, 2]) == 4


def test_prefix_is_best():
    assert max_subarray([10, -1, -1, -1, -100]) == 10


def test_suffix_is_best():
    assert max_subarray([-100, -1, -1, -1, 10]) == 10


def test_all_ones():
    assert max_subarray([1] * 1000) == 1000
