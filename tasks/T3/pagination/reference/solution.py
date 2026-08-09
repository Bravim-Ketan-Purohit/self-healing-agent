def paginate(items: list, page: int, page_size: int) -> list:
    """Return the items for a 0-indexed page."""
    start = page * page_size
    end = start + page_size
    return items[start:end]
