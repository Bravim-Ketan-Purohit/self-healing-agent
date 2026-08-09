from solution import repeat_join


def test_separator_count():
    """n repeats should produce exactly n-1 separators."""
    result = repeat_join("a", 4, ",")
    assert result == "a,a,a,a"
    assert result.count(",") == 3


def test_multi_char_separator():
    """Multi-character separator, count separators correctly."""
    result = repeat_join("x", 3, "---")
    assert result == "x---x---x"


def test_separator_not_at_end():
    """No trailing separator."""
    result = repeat_join("word", 2, "|")
    assert result == "word|word"
    assert not result.endswith("|")


def test_separator_not_at_start():
    """No leading separator."""
    result = repeat_join("word", 2, "|")
    assert not result.startswith("|")


def test_n_one_no_separator():
    """n=1 means just the string, no separator at all."""
    result = repeat_join("test", 1, "LONG_SEP")
    assert result == "test"


def test_empty_string_repeated():
    """Empty string repeated gives just separators."""
    result = repeat_join("", 3, "-")
    assert result == "--"


def test_large_n_separator_count():
    """Large n: verify exactly n-1 separators."""
    result = repeat_join("a", 100, ",")
    assert result.count(",") == 99
    assert result.count("a") == 100


def test_length_formula():
    """Total length = n*len(s) + (n-1)*len(sep) for n>0."""
    s, n, sep = "ab", 5, "--"
    result = repeat_join(s, n, sep)
    expected_len = n * len(s) + (n - 1) * len(sep)
    assert len(result) == expected_len
