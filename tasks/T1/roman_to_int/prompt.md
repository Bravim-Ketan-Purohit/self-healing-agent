# Roman to Integer

Write a function `roman_to_int(s: str) -> int` that converts a Roman numeral string to an integer.

Roman numerals use the following symbols:

| Symbol | Value |
|--------|-------|
| I      | 1    |
| V      | 5    |
| X      | 10   |
| L      | 50   |
| C      | 100  |
| D      | 500  |
| M      | 1000 |

When a smaller value appears before a larger value, it is subtracted (e.g., IV = 4, IX = 9).

## Constraints

- `s` is a valid Roman numeral in the range [1, 3999].
- Input contains only characters: I, V, X, L, C, D, M.

## Examples

```python
roman_to_int("III") == 3
roman_to_int("LVIII") == 58
roman_to_int("MCMXCIV") == 1994
roman_to_int("IV") == 4
roman_to_int("IX") == 9
```
