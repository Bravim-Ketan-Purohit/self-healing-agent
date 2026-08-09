# Precise Float Sum

Write a function `precise_sum(numbers: list[float]) -> float` that returns the sum of a list of floating-point numbers with high accuracy.

The result must match the exact mathematical sum to within an absolute tolerance of `1e-10`.

Naive summation using `sum()` can accumulate floating-point drift, especially with many small values or alternating large/small magnitudes.

## Examples

```python
precise_sum([0.1, 0.2, 0.3]) == 0.6  # within 1e-10
precise_sum([1e16, 1.0, -1e16]) == 1.0  # within 1e-10
precise_sum([0.1] * 10) == 1.0  # within 1e-10
precise_sum([]) == 0.0
```

## Constraints

- The input list may contain up to 100,000 elements.
- Values can range from -1e16 to 1e16.
- Return 0.0 for an empty list.
