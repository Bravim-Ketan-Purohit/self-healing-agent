from solution import paginate


def test_page_beyond_range():
    """Page well beyond the end returns empty."""
    assert paginate([1, 2, 3], 5, 2) == []


def test_page_size_greater_than_total():
    """Page size larger than the list: page 0 gets everything, page 1 empty."""
    assert paginate([1, 2, 3], 0, 10) == [1, 2, 3]
    assert paginate([1, 2, 3], 1, 10) == []


def test_exactly_full_last_page():
    """When items divide evenly, last valid page is full, next is empty."""
    assert paginate([1, 2, 3, 4], 1, 2) == [3, 4]
    assert paginate([1, 2, 3, 4], 2, 2) == []


def test_page_size_one():
    """page_size=1 means each element is its own page."""
    items = [10, 20, 30, 40, 50]
    assert paginate(items, 0, 1) == [10]
    assert paginate(items, 4, 1) == [50]
    assert paginate(items, 5, 1) == []


def test_page_zero_is_first():
    """Verify 0-indexed: page 0 is the first, not page 1."""
    items = list(range(100))
    assert paginate(items, 0, 10) == list(range(10))


def test_single_item_list():
    """Single-item list edge case."""
    assert paginate([42], 0, 1) == [42]
    assert paginate([42], 1, 1) == []
    assert paginate([42], 0, 5) == [42]


def test_page_size_equals_length():
    """When page_size equals list length: page 0 is full, page 1 is empty."""
    items = [1, 2, 3, 4, 5]
    assert paginate(items, 0, 5) == [1, 2, 3, 4, 5]
    assert paginate(items, 1, 5) == []


def test_large_page_number():
    """Very large page number returns empty."""
    assert paginate([1, 2, 3], 999999, 2) == []
