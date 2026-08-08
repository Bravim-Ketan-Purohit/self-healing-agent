from solution import binary_search


def test_empty_list():
    assert binary_search([], 5) == -1


def test_single_element_found():
    assert binary_search([7], 7) == 0


def test_single_element_not_found():
    assert binary_search([7], 3) == -1


def test_duplicates_returns_first():
    assert binary_search([1, 2, 2, 2, 3, 4], 2) == 1


def test_all_same_elements():
    assert binary_search([5, 5, 5, 5, 5], 5) == 0


def test_negative_numbers():
    assert binary_search([-10, -5, -1, 0, 3, 8], -5) == 1


def test_target_smaller_than_all():
    assert binary_search([10, 20, 30, 40], 5) == -1


def test_target_larger_than_all():
    assert binary_search([10, 20, 30, 40], 50) == -1


def test_large_list():
    nums = list(range(0, 100000, 2))  # even numbers 0..99998
    assert binary_search(nums, 50000) == 25000
    assert binary_search(nums, 50001) == -1


def test_duplicates_at_beginning():
    assert binary_search([1, 1, 1, 2, 3, 4, 5], 1) == 0
