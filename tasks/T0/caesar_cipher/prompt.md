# Caesar Cipher

Write a function `caesar_cipher(text: str, shift: int) -> str` that shifts each letter in the string by `shift` positions in the alphabet.

- Wrap around from z to a (and Z to A).
- Preserve the case of each letter.
- Non-alphabetic characters remain unchanged.
- Shift can be negative (shift left) or zero.

## Examples

```python
caesar_cipher("abc", 1) == "bcd"
caesar_cipher("xyz", 3) == "abc"
caesar_cipher("Hello, World!", 5) == "Mjqqt, Btwqi!"
caesar_cipher("abc", -1) == "zab"
caesar_cipher("abc", 0) == "abc"
```
