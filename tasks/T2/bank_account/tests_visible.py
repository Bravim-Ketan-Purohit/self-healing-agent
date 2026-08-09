from solution import BankAccount
import pytest


def test_deposit_and_balance():
    acc = BankAccount("Alice", 100.0)
    acc.deposit(50.0)
    assert acc.balance == 150.0


def test_withdraw():
    acc = BankAccount("Bob", 100.0)
    acc.withdraw(40.0)
    assert acc.balance == 60.0


def test_overdraft_raises():
    acc = BankAccount("Charlie", 50.0)
    with pytest.raises(ValueError):
        acc.withdraw(100.0)


def test_transfer_basic():
    a = BankAccount("Alice", 100.0)
    b = BankAccount("Bob", 50.0)
    a.transfer_to(b, 30.0)
    assert a.balance == 70.0
    assert b.balance == 80.0
