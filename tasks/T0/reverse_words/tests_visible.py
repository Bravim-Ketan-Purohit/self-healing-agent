from solution import reverse_words


def test_basic():
    assert reverse_words("hello world") == "world hello"


def test_multiple_words():
    assert reverse_words("the sky is blue") == "blue is sky the"


def test_single_word():
    assert reverse_words("one") == "one"


def test_extra_spaces():
    assert reverse_words("  hello   world  ") == "world hello"
