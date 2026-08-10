from solution import Tokenizer, Parser


def test_simple_addition():
    tokens = Tokenizer("2 + 3").tokenize()
    assert Parser(tokens).evaluate() == 5


def test_precedence():
    tokens = Tokenizer("2 + 3 * 4").tokenize()
    assert Parser(tokens).evaluate() == 14


def test_parentheses():
    tokens = Tokenizer("(2 + 3) * 4").tokenize()
    assert Parser(tokens).evaluate() == 20


def test_token_format():
    tokens = Tokenizer("1 + 2").tokenize()
    assert tokens[0]["type"] == "NUMBER"
    assert tokens[0]["value"] == "1"
    assert tokens[1]["type"] == "PLUS"
    assert tokens[1]["value"] == "+"
