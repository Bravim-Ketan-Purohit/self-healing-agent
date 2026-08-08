from solution import binary_search


def test_found_middle():
    assert binary_search([1, 3, 5, 7, 9], 5) == 2


def test_not_found():
    assert binary_search([1, 3, 5, 7, 9], 4) == -1


def test_first_element():
    assert binary_search([1, 3, 5, 7, 9], 1) == 0


def test_last_element():
    assert binary_search([1, 3, 5, 7, 9], 9) == 4
