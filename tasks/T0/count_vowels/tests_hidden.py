from solution import count_vowels


def test_empty_string():
    assert count_vowels("") == 0


def test_all_consonants():
    assert count_vowels("bcdfghjklmnpqrstvwxyz") == 0


def test_mixed_case_vowels():
    assert count_vowels("AeIoU") == 5


def test_with_numbers_and_symbols():
    assert count_vowels("h3ll0 w0rld!") == 0


def test_spaces_and_punctuation():
    assert count_vowels("hello, world!") == 3


def test_long_string():
    assert count_vowels("a" * 10000) == 10000


def test_unicode_no_count():
    # Accented vowels should NOT count as plain vowels
    assert count_vowels("café") == 1  # only 'a' counts, not 'é'


def test_repeated_vowels():
    assert count_vowels("aaeeiioouu") == 10
