def split_bill(total_cents: int, n: int) -> list[int]:
    """Split total_cents among n people. Sum is always exact."""
    base = total_cents // n
    remainder = total_cents % n
    return [base + 1 if i < remainder else base for i in range(n)]
