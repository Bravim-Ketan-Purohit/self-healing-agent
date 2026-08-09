from solution import split_bill


def test_even_split():
    assert split_bill(100, 4) == [25, 25, 25, 25]


def test_remainder_one():
    assert split_bill(10, 3) == [4, 3, 3]


def test_single_person():
    assert split_bill(10, 1) == [10]


def test_larger_remainder():
    assert split_bill(100, 3) == [34, 33, 33]
