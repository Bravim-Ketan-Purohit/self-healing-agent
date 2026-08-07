def count_vowels(s: str) -> int:
    """Count the number of vowels in a string (case-insensitive)."""
    return sum(1 for c in s if c.lower() in "aeiou")
