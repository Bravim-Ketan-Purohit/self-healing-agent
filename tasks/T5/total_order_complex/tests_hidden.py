from solution import compare_complex


def test_addition_preserving():
    """If a <= b, then a+c <= b+c for any c."""
    test_cases = [
        (1+0j, 2+0j, 1+1j),
        (0+1j, 0+2j, 3+3j),
        (-1+0j, 1+0j, 0+1j),
        (1+2j, 3+4j, -5-6j),
    ]
    for a, b, c in test_cases:
        if compare_complex(a, b) <= 0:
            assert compare_complex(a + c, b + c) <= 0, \
                f"Addition not preserved: {a} <= {b} but {a+c} > {b+c}"


def test_multiplication_preserving():
    """If a <= b and 0 <= c, then a*c <= b*c.
    This is mathematically impossible for complex numbers
    combined with total ordering."""
    # If i > 0, then i*i = -1 > 0 (contradiction since -1 < 0 for real ordering)
    # If i < 0, then (-i) > 0, so (-i)*(-i) = -1 > 0 (same contradiction)
    i = 0+1j
    zero = 0+0j
    neg_one = -1+0j
    one = 1+0j

    # First: determine ordering of i vs 0
    cmp_i_0 = compare_complex(i, zero)

    if cmp_i_0 > 0:
        # i > 0, so multiplying positive by positive: i*i should be > 0
        assert compare_complex(i * i, zero) >= 0, \
            "i > 0 implies i*i >= 0, but i*i = -1 < 0"
        # Also check that -1 >= 0 (since i*i = -1)
        assert compare_complex(neg_one, zero) >= 0, \
            "i > 0 and multiplication preserving implies -1 >= 0"
    elif cmp_i_0 < 0:
        # i < 0 means -i > 0
        neg_i = -i
        assert compare_complex(neg_i, zero) > 0
        # (-i)*(-i) should be >= 0 since -i > 0
        result = neg_i * neg_i  # = -1
        assert compare_complex(result, zero) >= 0, \
            "-i > 0 implies (-i)*(-i) >= 0, but (-i)*(-i) = -1 < 0"
    else:
        # i == 0 contradicts i being nonzero
        assert False, "i cannot equal 0 in any sensible ordering"


def test_ordered_field_contradiction():
    """Direct test of the ordered field impossibility.
    In any ordered field, x^2 >= 0 for all x.
    But i^2 = -1, so we need -1 >= 0.
    If -1 >= 0, then by addition: 0 >= 1. But 1 > 0 in any ordered field.
    Contradiction."""
    zero = 0+0j
    one = 1+0j
    neg_one = -1+0j

    # x^2 >= 0 for all x (required by multiplication preservation)
    i = 0+1j
    i_squared = i * i  # = -1

    # Requirement 5: if 0 <= i, then 0*i <= i*i, so 0 <= -1
    # OR if i <= 0, then 0 <= -i, so 0 <= (-i)^2 = -1
    # Either way: -1 >= 0
    assert compare_complex(neg_one, zero) >= 0, \
        "Multiplication preservation requires -1 >= 0"

    # But requirement 4 (addition preserving) + real line ordering requires:
    # 0 < 1 (standard), and if -1 >= 0 then -1 + 1 >= 0 + 1, i.e., 0 >= 1
    # So 0 >= 1
    assert compare_complex(zero, one) >= 0, \
        "If -1 >= 0, then by adding 1: 0 >= 1"

    # But also must have 1 > 0 for non-trivial ordering
    assert compare_complex(one, zero) > 0, \
        "1 must be positive in any non-trivial ordering"
