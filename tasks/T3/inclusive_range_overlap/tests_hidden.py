from solution import ranges_overlap


def test_touching_at_boundary():
    """Inclusive ranges touching at exactly one point DO overlap."""
    assert ranges_overlap(1, 5, 5, 10) is True


def test_touching_reverse_order():
    """Same boundary touch, different range order."""
    assert ranges_overlap(5, 10, 1, 5) is True


def test_off_by_one_no_overlap():
    """Adjacent but not touching: [1,4] and [5,10] do NOT overlap."""
    assert ranges_overlap(1, 4, 5, 10) is False


def test_single_point_overlap():
    """Single-point ranges that share the same point."""
    assert ranges_overlap(5, 5, 5, 5) is True


def test_single_point_no_overlap():
    """Single-point ranges that differ by 1."""
    assert ranges_overlap(5, 5, 6, 6) is False


def test_negative_ranges_overlap():
    """Negative ranges touching at boundary."""
    assert ranges_overlap(-10, -5, -5, 0) is True


def test_negative_ranges_no_overlap():
    """Negative ranges off by one."""
    assert ranges_overlap(-10, -6, -5, 0) is False


def test_large_range_boundary():
    """Large range values, boundary touching."""
    assert ranges_overlap(0, 1000000, 1000000, 2000000) is True
