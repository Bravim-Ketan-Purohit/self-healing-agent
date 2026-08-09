# Date Range

Write a function `date_range(start: str, end: str) -> list[str]` that generates all dates from `start` to `end`, **inclusive on both ends**.

Dates are given and returned in `"YYYY-MM-DD"` format.

## Examples

```python
date_range("2024-01-01", "2024-01-03")
# ["2024-01-01", "2024-01-02", "2024-01-03"]

date_range("2024-03-01", "2024-03-01")
# ["2024-03-01"]

date_range("2024-02-28", "2024-03-01")
# ["2024-02-28", "2024-02-29", "2024-03-01"]  (2024 is a leap year)
```

## Constraints

- `start` is always <= `end`.
- Both dates are valid calendar dates.
- The range can span month and year boundaries.
