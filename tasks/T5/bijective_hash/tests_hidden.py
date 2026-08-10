import time
import string
import itertools
from solution import bijective_hash


def test_collision_free_large_set():
    """Generate more than 2^32 distinct strings and verify no collisions.
    By pigeonhole principle, this is impossible with 32-bit output."""
    # Generate 100000 distinct strings - if truly bijective over all strings
    # into 32-bit range, eventually collisions MUST happen
    seen = set()
    # Use strings that vary only in later characters to exploit O(1) constraint
    for i in range(100000):
        s = f"string_number_{i:010d}_padding_to_make_it_longer"
        h = bijective_hash(s)
        assert h not in seen, f"Collision detected: hash {h} already seen"
        seen.add(h)


def test_truly_constant_time():
    """Verify O(1) by testing that a 10M character string hashes
    in same time as a 1 character string (within 2x)."""
    short = "a"
    long_str = "a" * 10_000_000

    start = time.perf_counter_ns()
    for _ in range(1000):
        bijective_hash(short)
    short_time = time.perf_counter_ns() - start

    start = time.perf_counter_ns()
    for _ in range(1000):
        bijective_hash(long_str)
    long_time = time.perf_counter_ns() - start

    # O(1) means long string should take similar time
    assert long_time < short_time * 2, \
        f"Not O(1): long took {long_time}ns vs short {short_time}ns"


def test_pigeonhole_violation():
    """With 2^32 possible outputs but infinite possible inputs,
    generate specific collision-prone pairs."""
    # These strings differ only after position 100 - if O(1) means
    # only looking at fixed positions, they MUST collide
    s1 = "a" * 100 + "x" + "b" * 1000
    s2 = "a" * 100 + "y" + "b" * 1000
    assert bijective_hash(s1) != bijective_hash(s2), \
        "Must distinguish strings differing at arbitrary positions"

    # But also - by pigeonhole, generate 2^16+1 length-4 strings
    # from 256 byte values, hashes must all be unique in [0, 2^32-1]
    strings = [''.join(c) for c in itertools.product(string.ascii_letters, repeat=4)]
    hashes = [bijective_hash(s) for s in strings[:70000]]
    assert len(set(hashes)) == len(hashes), "Collisions found among short strings"
