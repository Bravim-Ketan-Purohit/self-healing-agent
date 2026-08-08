# Valid Brackets

Write a function `valid_brackets(s: str) -> bool` that determines if a string containing only the characters `()[]{}` has valid (balanced) brackets.

A string is valid if:
1. Every opening bracket has a corresponding closing bracket of the same type.
2. Brackets are closed in the correct order.
3. An empty string is considered valid.

## Examples

```python
valid_brackets("()") == True
valid_brackets("()[]{}") == True
valid_brackets("(]") == False
valid_brackets("([)]") == False
valid_brackets("{[]}") == True
valid_brackets("") == True
```
