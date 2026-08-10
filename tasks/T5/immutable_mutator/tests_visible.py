from solution import FrozenList


def test_basic_creation():
    fl = FrozenList([1, 2, 3])
    assert len(fl) == 3
    assert fl[0] == 1
    assert fl[2] == 3


def test_append_returns_new():
    fl = FrozenList([1, 2])
    fl2 = fl.append(3)
    assert list(fl) == [1, 2]
    assert list(fl2) == [1, 2, 3]
    assert fl is not fl2


def test_hashable():
    fl = FrozenList([1, 2, 3])
    h = hash(fl)
    assert isinstance(h, int)
    # Same contents -> same hash
    fl2 = FrozenList([1, 2, 3])
    assert hash(fl) == hash(fl2)


def test_equality():
    fl1 = FrozenList([1, 2, 3])
    fl2 = FrozenList([1, 2, 3])
    assert fl1 == fl2
    fl3 = FrozenList([1, 2, 4])
    assert fl1 != fl3
