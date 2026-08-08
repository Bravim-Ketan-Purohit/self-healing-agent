class ListNode:
    """Singly linked list node."""

    def __init__(self, val: int = 0, next: "ListNode | None" = None):
        self.val = val
        self.next = next


def has_cycle(head: ListNode | None) -> bool:
    """Detect if a linked list has a cycle using Floyd's algorithm."""
    pass
