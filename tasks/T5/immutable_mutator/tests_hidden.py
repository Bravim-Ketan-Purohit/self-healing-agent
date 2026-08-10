from solution import FrozenList


def test_same_object_after_append():
    """CONTRADICTORY: The append operation must modify the SAME object
    (same id()) while the object must remain immutable."""
    fl = FrozenList([1, 2, 3])
    original_id = id(fl)
    fl2 = fl.append(4)

    # Hidden: append must return the SAME object (same identity)
    assert id(fl2) == original_id, \
        "append must return the same object (same id)"
    # But also: the new element must exist
    assert 4 in list(fl2), "appended element must be present"
    # And original contents unchanged (from visible test contract)
    assert fl[0] == 1 and fl[1] == 2 and fl[2] == 3


def test_immutability_yet_mutable():
    """Object must reject __setitem__ but append must 'work' on same object."""
    fl = FrozenList([10, 20, 30])
    original_id = id(fl)

    # Must reject direct mutation
    try:
        fl[0] = 99
        assert False, "Must raise TypeError on __setitem__"
    except TypeError:
        pass

    # But append must add to same object
    fl2 = fl.append(40)
    assert id(fl2) == original_id
    assert len(fl2) == 4
    assert fl2[3] == 40

    # AND original length must still be 3 (immutability)
    assert len(fl) == 3, "Original must remain length 3 (immutable)"


def test_hash_stability_with_mutation():
    """If same object, hash must not change. But contents change via append.
    hash(fl) before append must equal hash(fl) after append returns same object,
    but hash should also reflect contents."""
    fl = FrozenList([1, 2])
    h1 = hash(fl)

    fl2 = fl.append(3)
    h2 = hash(fl2)

    # Same object means same hash
    assert id(fl) == id(fl2), "Must be same object"
    assert h1 == h2, "Same object must have same hash"

    # But also: FrozenList([1,2,3]) should have a different hash than FrozenList([1,2])
    fl_check = FrozenList([1, 2, 3])
    assert hash(fl_check) != h1, \
        "List with different contents must have different hash"

    # Contradiction: fl2 is fl (same object, same hash as [1,2])
    # but fl2 contains [1,2,3] (should hash same as fl_check)
    assert hash(fl2) == hash(fl_check), \
        "fl2 contains [1,2,3] so must hash same as FrozenList([1,2,3])"


def test_append_chain_same_identity():
    """Chained appends must ALL return same identity while each
    showing progressively more elements."""
    fl = FrozenList([])
    original_id = id(fl)

    fl1 = fl.append(1)
    assert id(fl1) == original_id
    assert list(fl1) == [1]
    assert list(fl) == []  # original unchanged

    fl2 = fl1.append(2)
    assert id(fl2) == original_id
    assert list(fl2) == [1, 2]
    assert list(fl1) == [1]  # fl1 unchanged
    assert list(fl) == []  # fl unchanged
