import pytest
from solution import PhoneValidator, PhoneFormatter


def test_dots_format():
    v = PhoneValidator()
    f = PhoneFormatter()
    assert v.is_valid("123.456.7890") is True
    assert f.format("123.456.7890") == "(123) 456-7890"


def test_parentheses_format():
    v = PhoneValidator()
    f = PhoneFormatter()
    assert v.is_valid("(123) 456-7890") is True
    assert f.format("(123) 456-7890") == "(123) 456-7890"


def test_11_digit_with_separators():
    v = PhoneValidator()
    f = PhoneFormatter()
    assert v.is_valid("1-123-456-7890") is True
    assert f.format("1-123-456-7890") == "+1 (123) 456-7890"


def test_invalid_letters():
    v = PhoneValidator()
    f = PhoneFormatter()
    assert v.is_valid("123-abc-7890") is False
    with pytest.raises(ValueError):
        f.format("123-abc-7890")


def test_invalid_11_digit_not_starting_with_1():
    v = PhoneValidator()
    f = PhoneFormatter()
    assert v.is_valid("21234567890") is False
    with pytest.raises(ValueError):
        f.format("21234567890")


def test_strip_whitespace():
    v = PhoneValidator()
    f = PhoneFormatter()
    assert v.is_valid("  1234567890  ") is True
    assert f.format("  1234567890  ") == "(123) 456-7890"


def test_empty_string():
    v = PhoneValidator()
    f = PhoneFormatter()
    assert v.is_valid("") is False
    with pytest.raises(ValueError):
        f.format("")


def test_get_digits_consistency():
    v = PhoneValidator()
    phone = "(123) 456-7890"
    digits = v.get_digits(phone)
    assert digits == "1234567890"


def test_get_digits_invalid_raises():
    v = PhoneValidator()
    with pytest.raises(ValueError):
        v.get_digits("not-a-phone")
