from collections import deque


def sliding_max(nums: list[int], k: int) -> list[int]:
    """Return the maximum in each sliding window of size k."""
    if not nums or k == 0:
        return []

    result = []
    dq = deque()  # stores indices of elements in decreasing order

    for i, num in enumerate(nums):
        # Remove elements outside the window
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        # Remove elements smaller than current from the back
        while dq and nums[dq[-1]] <= num:
            dq.pop()
        dq.append(i)
        # Start recording results once we've filled the first window
        if i >= k - 1:
            result.append(nums[dq[0]])

    return result
