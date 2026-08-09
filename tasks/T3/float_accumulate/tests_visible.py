from solution import precise_sum


def test_basic_sum():
    assert abs(precise_sum([1.0, 2.0, 3.0]) - 6.0) < 1e-10


def test_simple_floats():
    assert abs(precise_sum([0.1, 0.2, 0.3]) - 0.6) < 1e-10


def test_empty_list():
    assert precise_sum([]) == 0.0


def test_single_element():
    assert abs(precise_sum([3.14]) - 3.14) < 1e-10
