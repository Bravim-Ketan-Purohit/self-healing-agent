# Currency Split

Write a function `split_bill(total_cents: int, n: int) -> list[int]` that splits a bill (given in cents as an integer) among `n` people as fairly as possible.

Each person's share is in whole cents. The sum of all shares must equal `total_cents` exactly. Distribute any remainder by giving 1 extra cent to the first people in the list.

## Examples

```python
split_bill(100, 3)   # [34, 33, 33] — remainder 1 goes to first person
split_bill(10, 3)    # [4, 3, 3]    — remainder 1 goes to first person
split_bill(100, 4)   # [25, 25, 25, 25] — divides evenly
split_bill(7, 3)     # [3, 2, 2]    — remainder 1 goes to first person
split_bill(10, 1)    # [10]
```

## Constraints

- `total_cents` is a non-negative integer.
- `n` is a positive integer (>= 1).
- Each element of the returned list is a non-negative integer.
- `sum(result) == total_cents` must always hold.
- The maximum difference between any two shares is at most 1.
