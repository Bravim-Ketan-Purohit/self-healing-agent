class BankAccount:
    """Bank account with deposit, withdraw, transfer, and overdraft protection."""

    def __init__(self, owner: str, balance: float = 0.0):
        if balance < 0:
            raise ValueError("Initial balance cannot be negative")
        self._owner = owner
        self._balance = balance

    @property
    def balance(self) -> float:
        return self._balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount

    def transfer_to(self, other: 'BankAccount', amount: float) -> None:
        if other is self:
            raise ValueError("Cannot transfer to the same account")
        if amount <= 0:
            raise ValueError("Transfer amount must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient funds for transfer")
        self._balance -= amount
        other._balance += amount
