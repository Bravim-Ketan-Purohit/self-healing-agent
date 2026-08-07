from solution import remove_duplicates


def test_basic():
    assert remove_duplicates([1, 2, 3, 2, 1]) == [1, 2, 3]


def test_all_same():
    assert remove_duplicates([1, 1, 1]) == [1]


def test_empty():
    assert remove_duplicates([]) == []


def test_strings():
    assert remove_duplicates(["a", "b", "a", "c"]) == ["a", "b", "c"]
