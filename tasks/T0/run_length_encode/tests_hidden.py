from solution import run_length_encode


def test_empty_string():
    assert run_length_encode("") == ""


def test_spaces():
    assert run_length_encode("   ") == "3 "


def test_mixed_content():
    assert run_length_encode("aabbb11") == "2a3b21"


def test_uppercase():
    assert run_length_encode("AAAbbb") == "3A3b"


def test_alternating():
    assert run_length_encode("ababab") == "1a1b1a1b1a1b"


def test_long_run():
    assert run_length_encode("x" * 100) == "100x"


def test_special_characters():
    assert run_length_encode("!!!@@") == "3!2@"


def test_single_each():
    assert run_length_encode("abcdef") == "1a1b1c1d1e1f"
