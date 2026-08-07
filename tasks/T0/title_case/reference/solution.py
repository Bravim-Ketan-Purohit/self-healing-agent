def title_case(s: str) -> str:
    """Convert a string to title case, handling apostrophes correctly."""
    words = s.split(" ")
    result = []
    for word in words:
        if word:
            result.append(word[0].upper() + word[1:].lower())
        else:
            result.append(word)
    return " ".join(result)
