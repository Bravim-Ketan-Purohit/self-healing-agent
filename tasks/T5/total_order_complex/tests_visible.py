from solution import compare_complex


def test_real_ordering():
    assert compare_complex(1+0j, 2+0j) < 0
    assert compare_complex(3+0j, 1+0j) > 0
    assert compare_complex(5+0j, 5+0j) == 0


def test_reflexivity():
    assert compare_complex(1+2j, 1+2j) == 0
    assert compare_complex(0+0j, 0+0j) == 0


def test_antisymmetry():
    a, b = 1+2j, 3+4j
    r1 = compare_complex(a, b)
    r2 = compare_complex(b, a)
    assert (r1 > 0 and r2 < 0) or (r1 < 0 and r2 > 0) or (r1 == 0 and r2 == 0)


def test_transitivity():
    a, b, c = 1+0j, 2+0j, 3+0j
    assert compare_complex(a, b) < 0
    assert compare_complex(b, c) < 0
    assert compare_complex(a, c) < 0
