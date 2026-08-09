from solution import paginate


def test_first_page():
    assert paginate([1, 2, 3, 4, 5], 0, 2) == [1, 2]


def test_middle_page():
    assert paginate([1, 2, 3, 4, 5], 1, 2) == [3, 4]


def test_last_page_partial():
    assert paginate([1, 2, 3, 4, 5], 2, 2) == [5]


def test_empty_list():
    assert paginate([], 0, 5) == []
