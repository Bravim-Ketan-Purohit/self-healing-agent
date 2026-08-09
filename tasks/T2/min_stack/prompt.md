# Min Stack

Implement a `MinStack` class that supports the following operations, all in O(1) time:

- `push(val: int)` — Push an integer onto the stack.
- `pop() -> int` — Remove and return the top element. Raises `IndexError` if the stack is empty.
- `top() -> int` — Return the top element without removing it. Raises `IndexError` if the stack is empty.
- `get_min() -> int` — Return the minimum element currently in the stack. Raises `IndexError` if the stack is empty.

## Constraints

- All operations must run in O(1) time.
- The minimum must be correctly tracked after any sequence of push/pop operations.

## Examples

```python
s = MinStack()
s.push(5)
s.push(3)
s.push(7)
s.get_min()  # 3
s.pop()      # 7
s.get_min()  # 3
s.pop()      # 3
s.get_min()  # 5
```
