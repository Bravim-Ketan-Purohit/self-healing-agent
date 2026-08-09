def repeat_join(s: str, n: int, sep: str) -> str:
    """Repeat s exactly n times, joined by sep."""
    if n <= 0:
        return ""
    return sep.join([s] * n)
