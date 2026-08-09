import bisect


def insert_sorted(lst: list[int], val: int) -> list[int]:
    """Insert val into sorted lst maintaining order. Does not mutate original."""
    new_lst = lst.copy()
    bisect.insort_right(new_lst, val)
    return new_lst
