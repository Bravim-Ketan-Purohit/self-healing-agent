# Phone Validator & Formatter

## Problem

Implement two classes that must agree on what constitutes a valid phone number and how it should be normalized:

1. **`PhoneValidator`** - Checks whether a phone number string is valid:
   - `is_valid(phone_str)` - Returns `True` if the string represents a valid phone number.
   - `get_digits(phone_str)` - Returns only the digit characters from the input, or raises `ValueError` if invalid.

2. **`PhoneFormatter`** - Normalizes valid phone numbers to a standard format:
   - `format(phone_str)` - Returns the phone number in the format `(XXX) XXX-XXXX` for 10-digit numbers, or `+X (XXX) XXX-XXXX` for 11-digit numbers starting with 1. Raises `ValueError` if the phone number is invalid.

## Accepted Input Formats

- `1234567890` (10 digits, no separators)
- `123-456-7890` (dashes)
- `(123) 456-7890` (parentheses with space and dash)
- `123.456.7890` (dots)
- `11234567890` or `1-123-456-7890` (with country code 1)
- Leading/trailing whitespace should be stripped.

## Invalid Inputs

- Fewer than 10 digits or more than 11 digits
- 11 digits where the first digit is NOT 1
- Contains letters or unexpected symbols (anything other than digits, spaces, dashes, dots, parens)
- Empty string

## Interface Contract

- Both must agree: if `PhoneValidator.is_valid(x)` returns True, then `PhoneFormatter.format(x)` must succeed.
- If `PhoneValidator.is_valid(x)` returns False, then `PhoneFormatter.format(x)` must raise `ValueError`.
- `PhoneValidator.get_digits(x)` returns the same digits that `PhoneFormatter` uses for formatting.
- Both classes must be in the same `solution.py` file.
