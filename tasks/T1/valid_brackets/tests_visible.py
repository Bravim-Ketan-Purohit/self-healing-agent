from solution import valid_brackets


def test_simple_valid():
    assert valid_brackets("()") == True


def test_multiple_types():
    assert valid_brackets("()[]{}") == True


def test_nested():
    assert valid_brackets("{[()]}") == True


def test_mismatched():
    assert valid_brackets("(]") == False
