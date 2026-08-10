import pytest
from solution import PhoneValidator, PhoneFormatter


def test_valid_10_digit():
    v = PhoneValidator()
    f = PhoneFormatter()
    assert v.is_valid("1234567890") is True
    assert f.format("1234567890") == "(123) 456-7890"


def test_valid_with_dashes():
    v = PhoneValidator()
    f = PhoneFormatter()
    assert v.is_valid("123-456-7890") is True
    assert f.format("123-456-7890") == "(123) 456-7890"


def test_invalid_too_short():
    v = PhoneValidator()
    f = PhoneFormatter()
    assert v.is_valid("12345") is False
    with pytest.raises(ValueError):
        f.format("12345")


def test_valid_11_digit_with_country_code():
    v = PhoneValidator()
    f = PhoneFormatter()
    assert v.is_valid("11234567890") is True
    assert f.format("11234567890") == "+1 (123) 456-7890"
