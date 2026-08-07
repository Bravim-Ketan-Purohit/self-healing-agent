from solution import reverse_words


def test_empty_string():
    assert reverse_words("") == ""


def test_only_spaces():
    assert reverse_words("     ") == ""


def test_tabs_and_spaces():
    assert reverse_words("\thello\t world\t") == "world hello"


def test_single_character_words():
    assert reverse_words("a b c d") == "d c b a"


def test_long_sentence():
    words = [f"word{i}" for i in range(100)]
    sentence = " ".join(words)
    expected = " ".join(reversed(words))
    assert reverse_words(sentence) == expected


def test_punctuation_preserved():
    assert reverse_words("hello, world!") == "world! hello,"


def test_unicode_words():
    assert reverse_words("café résumé naïve") == "naïve résumé café"


def test_newlines_as_whitespace():
    assert reverse_words("hello\nworld\nfoo") == "foo world hello"
