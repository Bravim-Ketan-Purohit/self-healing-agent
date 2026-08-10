# Tokenizer & Parser for Math Expressions

## Problem

Implement two classes that work together to evaluate arithmetic expressions:

1. **`Tokenizer`** - Splits a math expression string into tokens:
   - `__init__(self, expression)` - Takes a string like `"3 + 4 * 2"`
   - `tokenize()` - Returns a list of Token objects (or dicts with `type` and `value` keys).

2. **`Parser`** - Evaluates a list of tokens:
   - `__init__(self, tokens)` - Takes the list produced by Tokenizer.
   - `evaluate()` - Returns the numerical result, respecting operator precedence.

## Token Format (the shared contract)

Each token must be a dict (or object) with:
- `type`: one of `"NUMBER"`, `"PLUS"`, `"MINUS"`, `"MUL"`, `"DIV"`, `"LPAREN"`, `"RPAREN"`
- `value`: the string representation (e.g., `"3"`, `"+"`, `"("`)

## Supported Operations

- Addition `+`, Subtraction `-`, Multiplication `*`, Division `/`
- Parentheses `(` and `)` for grouping
- Standard precedence: `*` and `/` before `+` and `-`
- Left-to-right evaluation for same-precedence operators
- Integer and float numbers (including multi-digit)

## Example

```python
tokens = Tokenizer("(2 + 3) * 4").tokenize()
result = Parser(tokens).evaluate()
assert result == 20
```

## Constraints

- Do NOT use `eval()`, `exec()`, or `ast` module.
- Division is float division (Python `/`).
- Both classes must be in the same `solution.py` file.
