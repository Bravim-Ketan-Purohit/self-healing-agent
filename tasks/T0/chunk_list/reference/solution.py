def chunk_list(lst: list, n: int) -> list:
    """Split a list into consecutive chunks of size n. Last chunk may be smaller."""
    if n < 1:
        raise ValueError("Chunk size must be at least 1")
    return [lst[i:i + n] for i in range(0, len(lst), n)]
