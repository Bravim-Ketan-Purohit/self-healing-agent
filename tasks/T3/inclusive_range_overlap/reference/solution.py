def ranges_overlap(a: int, b: int, c: int, d: int) -> bool:
    """Return True if inclusive ranges [a,b] and [c,d] overlap."""
    return a <= d and c <= b
