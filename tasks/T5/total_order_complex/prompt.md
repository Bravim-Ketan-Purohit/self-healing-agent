# Total Order on Complex Numbers

Implement a function `compare_complex(a: complex, b: complex) -> int` that defines a **total ordering** on complex numbers that is compatible with arithmetic operations.

## Requirements

1. **Total order**: For any two complex numbers a, b: exactly one of `compare_complex(a, b) < 0`, `compare_complex(a, b) == 0`, or `compare_complex(a, b) > 0` holds
2. **Transitivity**: If `compare_complex(a, b) <= 0` and `compare_complex(b, c) <= 0`, then `compare_complex(a, c) <= 0`
3. **Antisymmetry**: If `compare_complex(a, b) <= 0` and `compare_complex(b, a) <= 0`, then `a == b`
4. **Addition preserving**: If `compare_complex(a, b) <= 0`, then `compare_complex(a + c, b + c) <= 0` for all c
5. **Multiplication preserving**: If `compare_complex(a, b) <= 0` and `compare_complex(0+0j, c) <= 0`, then `compare_complex(a * c, b * c) <= 0`

## Return Value

- Negative int if a < b in the ordering
- Zero if a == b
- Positive int if a > b in the ordering

## Example

```python
>>> compare_complex(1+0j, 2+0j)  # Negative (1 < 2)
-1
>>> compare_complex(2+0j, 1+0j)  # Positive (2 > 1)
1
>>> compare_complex(1+1j, 1+1j)  # Equal
0
```
