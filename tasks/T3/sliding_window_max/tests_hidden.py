from solution import sliding_max


def test_output_length():
    """Output must have exactly len(nums) - k + 1 elements."""
    nums = [1, 2, 3, 4, 5, 6, 7]
    assert len(sliding_max(nums, 3)) == 5
    assert len(sliding_max(nums, 1)) == 7
    assert len(sliding_max(nums, 7)) == 1


def test_all_same_values():
    """When all values are the same, every window max is that value."""
    assert sliding_max([5, 5, 5, 5, 5], 3) == [5, 5, 5]


def test_descending_sequence():
    """Descending: max is always the leftmost element of each window."""
    assert sliding_max([5, 4, 3, 2, 1], 3) == [5, 4, 3]


def test_single_element():
    """Single element list with k=1."""
    assert sliding_max([42], 1) == [42]


def test_k_equals_two():
    """Window of size 2 on various inputs."""
    assert sliding_max([1, 3, 2, 5, 4], 2) == [3, 3, 5, 5]


def test_negative_values():
    """Works correctly with all negative values."""
    assert sliding_max([-5, -3, -1, -4, -2], 3) == [-1, -1, -1]


def test_large_window():
    """Window equals array length with mixed values."""
    nums = [3, 1, 4, 1, 5, 9, 2, 6]
    assert sliding_max(nums, len(nums)) == [9]


def test_alternating_peaks():
    """Alternating high/low pattern with k=2."""
    assert sliding_max([1, 10, 1, 10, 1, 10], 2) == [10, 10, 10, 10, 10]
