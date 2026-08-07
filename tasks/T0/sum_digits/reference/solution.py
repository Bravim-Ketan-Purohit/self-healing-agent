def sum_digits(s: str) -> int:
    """Sum all digits found in a string."""
    return sum(int(c) for c in s if c.isdigit())
