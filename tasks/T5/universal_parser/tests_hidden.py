import time
from solution import parse


def test_inherently_ambiguous_grammar():
    """Inherently ambiguous CFG: {a^i b^j c^k | i=j or j=k}.
    No unambiguous grammar exists for this language.
    Correct parsing requires tracking multiple derivations."""
    grammar = (
        "S -> A C | D B\n"
        "A -> a A b | a b\n"
        "B -> b B c | b c\n"
        "C -> c | c C\n"
        "D -> a | a D"
    )
    assert parse(grammar, "abc") == True  # i=j=k=1
    assert parse(grammar, "aabbc") == True  # i=j=2, k=1
    assert parse(grammar, "abbcc") == True  # i=1, j=k=2
    assert parse(grammar, "aabbcc") == True  # i=j=k=2
    assert parse(grammar, "aaabcc") == False  # i=3,j=1,k=2 (neither i=j nor j=k)


def test_linear_time_enforcement():
    """Verify O(n) by parsing a long string.
    For general CFG, CYK is O(n^3) and Earley is O(n^3) worst case.
    True O(n) is impossible for general CFGs."""
    grammar = "S -> a S b S | b S a S | a b | b a"
    # Generate long valid balanced string
    n = 50000
    input_str = "ab" * n

    start = time.perf_counter_ns()
    result = parse(grammar, input_str)
    time_n = time.perf_counter_ns() - start

    # Double the input
    input_str_2x = "ab" * (2 * n)
    start = time.perf_counter_ns()
    result2 = parse(grammar, input_str_2x)
    time_2n = time.perf_counter_ns() - start

    # O(n) means doubling input should roughly double time (within 3x)
    # O(n^3) would mean 8x increase
    assert time_2n < time_n * 4, \
        f"Not O(n): time({2*n})={time_2n}ns, time({n})={time_n}ns, ratio={time_2n/time_n:.1f}"


def test_epsilon_and_ambiguity():
    """Grammar with epsilon productions and high ambiguity.
    Requires exponential derivations for correct parsing in linear time."""
    grammar = (
        "S -> A A A A\n"
        "A -> a A | A a | a"
    )
    # This is highly ambiguous - 'aaaa' has many parse trees
    assert parse(grammar, "aaaa") == True
    assert parse(grammar, "a") == False  # need at least 4 A's worth


def test_general_cfg_not_lr():
    """Grammar that is not LR(k) for any k. Requires general parsing.
    O(n) parsing is provably impossible for this class."""
    grammar = (
        "S -> S S | a S b | b S a | a b | b a"
    )
    # Dyck language with two types - inherently requires stack
    # and ambiguous splitting makes O(n) impossible
    input_str = "ab" * 10000
    start = time.perf_counter_ns()
    assert parse(grammar, input_str) == True
    elapsed = time.perf_counter_ns() - start

    # Must complete 20000-char parse in under 20ms (O(n) budget)
    assert elapsed < 20_000_000, \
        f"Parse took {elapsed}ns for 20000 chars - not O(n)"
