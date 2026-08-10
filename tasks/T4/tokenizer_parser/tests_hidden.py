import pytest
from solution import Tokenizer, Parser


def test_division():
    tokens = Tokenizer("10 / 4").tokenize()
    assert Parser(tokens).evaluate() == 2.5


def test_nested_parens():
    tokens = Tokenizer("((2 + 3) * (4 - 1))").tokenize()
    assert Parser(tokens).evaluate() == 15


def test_left_to_right_subtraction():
    tokens = Tokenizer("10 - 3 - 2").tokenize()
    assert Parser(tokens).evaluate() == 5


def test_left_to_right_division():
    tokens = Tokenizer("12 / 3 / 2").tokenize()
    assert Parser(tokens).evaluate() == 2.0


def test_multi_digit_numbers():
    tokens = Tokenizer("100 + 200").tokenize()
    assert Parser(tokens).evaluate() == 300


def test_complex_expression():
    tokens = Tokenizer("2 * (3 + 4) - 8 / 2").tokenize()
    assert Parser(tokens).evaluate() == 10.0


def test_float_numbers():
    tokens = Tokenizer("3.5 + 1.5").tokenize()
    assert Parser(tokens).evaluate() == 5.0


def test_all_token_types_present():
    tokens = Tokenizer("(1 + 2) * 3 - 4 / 2").tokenize()
    types = {t["type"] for t in tokens}
    assert "NUMBER" in types
    assert "PLUS" in types
    assert "MUL" in types
    assert "MINUS" in types
    assert "DIV" in types
    assert "LPAREN" in types
    assert "RPAREN" in types
