# Bank Account

Implement a `BankAccount` class that models a simple bank account with the following operations:

- `__init__(self, owner: str, balance: float = 0.0)` — Create an account with an owner name and optional starting balance (default 0). Raises `ValueError` if initial balance is negative.
- `deposit(self, amount: float) -> None` — Add funds. Raises `ValueError` if amount is <= 0.
- `withdraw(self, amount: float) -> None` — Remove funds. Raises `ValueError` if amount is <= 0. Raises `ValueError` if amount exceeds current balance (no overdraft allowed).
- `transfer_to(self, other: 'BankAccount', amount: float) -> None` — Transfer funds from this account to another. Raises `ValueError` if amount is <= 0 or exceeds this account's balance. Raises `ValueError` if `other` is the same account as `self`.
- `balance` — Property that returns the current balance.

## Invariants

- Balance must never go negative.
- A transfer must be atomic: if it fails, neither account is modified.
- Total money across any closed system of accounts is conserved after transfers.

## Examples

```python
a = BankAccount("Alice", 100.0)
b = BankAccount("Bob", 50.0)
a.transfer_to(b, 30.0)
a.balance  # 70.0
b.balance  # 80.0

a.withdraw(200.0)  # raises ValueError
```
