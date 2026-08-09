class BankAccount:
    """Bank account with deposit, withdraw, transfer, and overdraft protection."""

    def __init__(self, owner: str, balance: float = 0.0):
        pass

    @property
    def balance(self) -> float:
        pass

    def deposit(self, amount: float) -> None:
        pass

    def withdraw(self, amount: float) -> None:
        pass

    def transfer_to(self, other: 'BankAccount', amount: float) -> None:
        pass
