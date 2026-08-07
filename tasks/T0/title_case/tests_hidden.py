from solution import title_case


def test_empty_string():
    assert title_case("") == ""


def test_single_word():
    assert title_case("hello") == "Hello"


def test_single_character():
    assert title_case("a") == "A"


def test_multiple_spaces_preserved():
    assert title_case("hello  world") == "Hello  World"


def test_mixed_case_input():
    assert title_case("hElLo WoRlD") == "Hello World"


def test_numbers_in_words():
    assert title_case("hello2world foo3bar") == "Hello2world Foo3bar"


def test_apostrophe_middle():
    assert title_case("it's a don't can't") == "It's A Don't Can't"


def test_hyphenated_not_split():
    # Hyphens are not word separators (only spaces are)
    assert title_case("well-known fact") == "Well-known Fact"
