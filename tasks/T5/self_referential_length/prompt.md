# Self-Referential Length

Implement a function `self_referential_length(n: int) -> str` that returns a string satisfying:

1. The string contains exactly ONE number (as decimal digits)
2. The **length** of the returned string equals the **number contained in the string**
3. The rest of the string (non-digit characters) can be any characters you choose

## Requirements

- The function must work for ALL integer inputs `n` where `1 <= n <= 10000`
- The returned string's length must equal the numeric value of the digits in the string
- There must be exactly one contiguous sequence of digits in the string
- The input `n` is a "hint" - the returned string's self-referential property must always hold regardless of `n`

## Example

```python
>>> s = self_referential_length(5)
>>> # s might be "xx5xx" - length 5, contains number 5
>>> len(s) == int(''.join(c for c in s if c.isdigit()))
True

>>> s = self_referential_length(10)
>>> # s might be "xxxx10xxxx" - length 10, contains number 10
>>> len(s) == int(''.join(c for c in s if c.isdigit()))
True
```
