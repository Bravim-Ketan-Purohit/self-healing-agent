from solution import valid_brackets


def test_empty_string():
    assert valid_brackets("") == True


def test_only_opening():
    assert valid_brackets("(((") == False


def test_only_closing():
    assert valid_brackets(")))") == False


def test_interleaved_invalid():
    assert valid_brackets("([)]") == False


def test_deeply_nested():
    assert valid_brackets("((((((()))))))") == True


def test_single_opening():
    assert valid_brackets("(") == False


def test_single_closing():
    assert valid_brackets(")") == False


def test_correct_close_order_matters():
    assert valid_brackets("{[}]") == False


def test_long_valid():
    assert valid_brackets("()[]{}" * 1000) == True


def test_unbalanced_extra_closing():
    assert valid_brackets("()())") == False
