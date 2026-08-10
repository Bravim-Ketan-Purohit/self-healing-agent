import re
from solution import self_referential_length


def test_basic():
    s = self_referential_length(5)
    digits = ''.join(c for c in s if c.isdigit())
    assert len(s) == int(digits)


def test_two_digits():
    s = self_referential_length(12)
    digits = ''.join(c for c in s if c.isdigit())
    assert len(s) == int(digits)


def test_one_contiguous_number():
    s = self_referential_length(7)
    # Must have exactly one contiguous group of digits
    groups = re.findall(r'\d+', s)
    assert len(groups) == 1


def test_various_inputs():
    for n in [1, 3, 10, 20, 100]:
        s = self_referential_length(n)
        digits = ''.join(c for c in s if c.isdigit())
        assert len(s) == int(digits), f"Failed for n={n}: len={len(s)}, num={digits}"
