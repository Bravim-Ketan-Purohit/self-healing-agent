def flatten_list(lst: list) -> list:
    """Flatten a nested list of arbitrary depth into a single flat list."""
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten_list(item))
        else:
            result.append(item)
    return result
