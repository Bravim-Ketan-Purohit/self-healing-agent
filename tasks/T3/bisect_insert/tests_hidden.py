from solution import insert_sorted


def test_no_mutation():
    """Original list must not be mutated."""
    original = [1, 3, 5, 7]
    result = insert_sorted(original, 4)
    assert original == [1, 3, 5, 7]
    assert result == [1, 3, 4, 5, 7]


def test_insert_duplicate_at_end_of_equals():
    """Inserting a duplicate should go after all existing equal elements."""
    assert insert_sorted([1, 3, 3, 5], 3) == [1, 3, 3, 3, 5]


def test_insert_at_boundary_first_element():
    """Inserting value equal to first element."""
    assert insert_sorted([2, 4, 6], 2) == [2, 2, 4, 6]


def test_insert_at_boundary_last_element():
    """Inserting value equal to last element."""
    assert insert_sorted([2, 4, 6], 6) == [2, 4, 6, 6]


def test_all_same_elements():
    """List of identical elements, insert same value."""
    assert insert_sorted([5, 5, 5], 5) == [5, 5, 5, 5]


def test_single_element_insert_before():
    """Insert before single-element list."""
    assert insert_sorted([5], 3) == [3, 5]


def test_single_element_insert_after():
    """Insert after single-element list."""
    assert insert_sorted([5], 7) == [5, 7]


def test_large_list_boundary():
    """Insert at the very end of a large sorted list."""
    lst = list(range(0, 1000, 2))  # [0, 2, 4, ..., 998]
    result = insert_sorted(lst, 999)
    assert result[-1] == 999
    assert len(result) == len(lst) + 1
    assert lst == list(range(0, 1000, 2))  # no mutation
