from datetime import date, timedelta


def date_range(start: str, end: str) -> list[str]:
    """Generate all dates from start to end, inclusive on both ends."""
    start_date = date.fromisoformat(start)
    end_date = date.fromisoformat(end)
    result = []
    current = start_date
    while current <= end_date:
        result.append(current.isoformat())
        current += timedelta(days=1)
    return result
