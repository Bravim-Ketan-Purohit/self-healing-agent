def two_sum(nums: list[int], target: int) -> list[int]:
    """Find two indices that sum to target. Return sorted pair or raise ValueError."""
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return sorted([seen[complement], i])
        seen[num] = i
    raise ValueError("No two sum solution")
