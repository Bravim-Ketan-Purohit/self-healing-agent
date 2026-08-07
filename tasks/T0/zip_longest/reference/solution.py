def zip_longest(*lists, fill=None) -> list:
    """Zip multiple lists, filling shorter ones with a fill value."""
    if not lists:
        return []
    max_len = max(len(lst) for lst in lists)
    result = []
    for i in range(max_len):
        row = tuple(lst[i] if i < len(lst) else fill for lst in lists)
        result.append(row)
    return result
