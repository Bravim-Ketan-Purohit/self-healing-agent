def reverse_words(s: str) -> str:
    """Reverse the order of words in a string."""
    words = s.split()
    return " ".join(reversed(words))
