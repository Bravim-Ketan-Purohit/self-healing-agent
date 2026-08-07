def is_palindrome(s: str) -> bool:
    """Check if string is a palindrome (ignore spaces, punctuation, case)."""
    cleaned = [c.lower() for c in s if c.isalnum()]
    return cleaned == cleaned[::-1]
