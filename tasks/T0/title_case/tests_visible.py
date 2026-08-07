from solution import title_case


def test_basic():
    assert title_case("hello world") == "Hello World"


def test_all_lowercase():
    assert title_case("the quick brown fox") == "The Quick Brown Fox"


def test_apostrophe():
    assert title_case("don't stop") == "Don't Stop"


def test_already_upper():
    assert title_case("HELLO WORLD") == "Hello World"
