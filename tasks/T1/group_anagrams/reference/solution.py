from collections import defaultdict


def group_anagrams(strs: list[str]) -> list[list[str]]:
    """Group a list of strings by anagram equivalence."""
    groups = defaultdict(list)
    for s in strs:
        key = "".join(sorted(s))
        groups[key].append(s)
    return list(groups.values())
