# Universal Parser

Implement a function `parse(grammar: str, input_str: str) -> bool` that determines whether `input_str` is a valid sentence in the context-free grammar specified by `grammar`.

## Grammar Format

The grammar is specified in BNF-like format:
```
S -> a B | b A
A -> a | a S | b A A
B -> b | b S | a B B
```

- Non-terminals are uppercase letters
- Terminals are lowercase letters or digits
- `S` is always the start symbol
- `|` separates alternatives
- Rules are separated by newlines

## Requirements

1. **Correct**: Must return `True` if and only if the input is derivable from the start symbol
2. **Linear time**: Must run in O(n) time where n = len(input_str)
3. **Universal**: Must handle ANY valid context-free grammar (not just LL(1) or LR(1))
4. **Handles ambiguity**: Must work correctly on ambiguous grammars

## Example

```python
>>> grammar = "S -> a S b | a b"
>>> parse(grammar, "aabb")
True
>>> parse(grammar, "ab")
True
>>> parse(grammar, "aab")
False
```

## Notes

This is useful for building lightweight syntax validators without pulling in heavy parser generator libraries.
