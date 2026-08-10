"""Phone Validator and Formatter that must agree on valid formats."""

import re


class PhoneValidator:
    """Validates phone number strings."""

    _ALLOWED = re.compile(r'^[\d\s\-\.\(\)]+$')

    def _extract_digits(self, phone_str):
        """Extract digits from phone string, return None if invalid chars."""
        phone_str = phone_str.strip()
        if not phone_str:
            return None
        if not self._ALLOWED.match(phone_str):
            return None
        digits = re.sub(r'\D', '', phone_str)
        return digits

    def is_valid(self, phone_str):
        """Return True if phone_str is a valid phone number."""
        digits = self._extract_digits(phone_str)
        if digits is None:
            return False
        if len(digits) == 10:
            return True
        if len(digits) == 11 and digits[0] == '1':
            return True
        return False

    def get_digits(self, phone_str):
        """Return only the digits. Raises ValueError if invalid."""
        if not self.is_valid(phone_str):
            raise ValueError(f"Invalid phone number: {phone_str}")
        return self._extract_digits(phone_str)


class PhoneFormatter:
    """Formats valid phone numbers to standard format."""

    def __init__(self):
        self._validator = PhoneValidator()

    def format(self, phone_str):
        """Return formatted phone number or raise ValueError if invalid."""
        if not self._validator.is_valid(phone_str):
            raise ValueError(f"Invalid phone number: {phone_str}")
        digits = self._validator.get_digits(phone_str)
        if len(digits) == 11:
            # +1 (XXX) XXX-XXXX
            return f"+{digits[0]} ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
        else:
            # (XXX) XXX-XXXX
            return f"({digits[0:3]}) {digits[3:6]}-{digits[6:]}"
