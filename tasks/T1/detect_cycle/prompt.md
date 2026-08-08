# Detect Cycle in Linked List

Implement a `ListNode` class and a function `has_cycle(head: ListNode | None) -> bool` that detects whether a singly linked list has a cycle.

## ListNode

```python
class ListNode:
    def __init__(self, val: int = 0, next: "ListNode | None" = None):
        self.val = val
        self.next = next
```

## Function

`has_cycle(head)` should return `True` if there is a cycle in the linked list, `False` otherwise.

A cycle exists when a node's `next` pointer points back to a previously visited node.

Use Floyd's cycle detection algorithm (tortoise and hare) for O(1) space complexity.

## Constraints

- The list may be empty (`head` is `None`).
- Node values are integers.

## Examples

```python
# No cycle: 1 -> 2 -> 3 -> None
head = ListNode(1, ListNode(2, ListNode(3)))
has_cycle(head) == False

# Cycle: 1 -> 2 -> 3 -> 1
a, b, c = ListNode(1), ListNode(2), ListNode(3)
a.next, b.next, c.next = b, c, a
has_cycle(a) == True

# Empty list
has_cycle(None) == False
```
