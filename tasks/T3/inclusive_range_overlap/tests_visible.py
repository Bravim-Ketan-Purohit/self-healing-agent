from solution import ranges_overlap


def test_clear_overlap():
    assert ranges_overlap(1, 5, 3, 8) is True


def test_no_overlap():
    assert ranges_overlap(1, 5, 6, 10) is False


def test_contained_range():
    assert ranges_overlap(1, 10, 3, 7) is True


def test_same_range():
    assert ranges_overlap(2, 5, 2, 5) is True
