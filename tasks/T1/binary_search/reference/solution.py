def binary_search(nums: list[int], target: int) -> int:
    """Binary search returning index of first occurrence, or -1 if not found."""
    left, right = 0, len(nums) - 1
    result = -1

    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            result = mid
            right = mid - 1  # continue searching left for first occurrence
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return result
