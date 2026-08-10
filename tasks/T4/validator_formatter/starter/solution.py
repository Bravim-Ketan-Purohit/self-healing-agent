"""Phone Validator and Formatter that must agree on valid formats.

Both classes must agree: if PhoneValidator.is_valid(x) is True,
PhoneFormatter.format(x) must succeed and vice versa.
"""


class PhoneValidator:
    """Validates phone number strings."""

    def is_valid(self, phone_str):
        """Return True if phone_str is a valid phone number."""
        raise NotImplementedError

    def get_digits(self, phone_str):
        """Return only the digit characters. Raises ValueError if invalid."""
        raise NotImplementedError


class PhoneFormatter:
    """Formats valid phone numbers to standard format.

    10 digits -> (XXX) XXX-XXXX
    11 digits starting with 1 -> +1 (XXX) XXX-XXXX
    """

    def format(self, phone_str):
        """Return formatted phone number or raise ValueError if invalid."""
        raise NotImplementedError
