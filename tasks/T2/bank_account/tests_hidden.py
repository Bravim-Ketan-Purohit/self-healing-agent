from solution import BankAccount
import pytest


def test_conservation_of_money_across_transfers():
    """Invariant: total money in a closed system is conserved."""
    a = BankAccount("A", 100.0)
    b = BankAccount("B", 200.0)
    c = BankAccount("C", 50.0)
    total_before = a.balance + b.balance + c.balance

    a.transfer_to(b, 40.0)
    b.transfer_to(c, 100.0)
    c.transfer_to(a, 25.0)

    total_after = a.balance + b.balance + c.balance
    assert total_before == total_after


def test_failed_transfer_leaves_both_unchanged():
    """Invariant: failed transfer is atomic - neither account modified."""
    a = BankAccount("A", 50.0)
    b = BankAccount("B", 100.0)
    with pytest.raises(ValueError):
        a.transfer_to(b, 75.0)  # exceeds a's balance
    assert a.balance == 50.0
    assert b.balance == 100.0


def test_self_transfer_raises():
    """Invariant: self-transfer is prohibited."""
    a = BankAccount("A", 100.0)
    with pytest.raises(ValueError):
        a.transfer_to(a, 10.0)
    assert a.balance == 100.0  # unchanged


def test_zero_and_negative_amounts_rejected():
    """Invariant: zero and negative amounts raise for all operations."""
    acc = BankAccount("X", 100.0)
    with pytest.raises(ValueError):
        acc.deposit(0)
    with pytest.raises(ValueError):
        acc.deposit(-10)
    with pytest.raises(ValueError):
        acc.withdraw(0)
    with pytest.raises(ValueError):
        acc.withdraw(-5)
    other = BankAccount("Y", 0.0)
    with pytest.raises(ValueError):
        acc.transfer_to(other, 0)
    with pytest.raises(ValueError):
        acc.transfer_to(other, -20)


def test_balance_never_negative_after_operations():
    """Invariant: balance is always >= 0 regardless of operation sequence."""
    acc = BankAccount("Test", 100.0)
    acc.withdraw(100.0)
    assert acc.balance == 0.0
    with pytest.raises(ValueError):
        acc.withdraw(0.01)
    assert acc.balance >= 0


def test_negative_initial_balance_raises():
    """Invariant: cannot create account with negative balance."""
    with pytest.raises(ValueError):
        BankAccount("Bad", -10.0)


def test_multiple_transfers_maintain_invariant():
    """Invariant: balance stays correct across many transfers."""
    accounts = [BankAccount(f"Acc{i}", 100.0) for i in range(5)]
    # Round-robin transfers
    for i in range(5):
        accounts[i].transfer_to(accounts[(i + 1) % 5], 20.0)
    # Each account sent 20 and received 20 -> still 100 each
    for acc in accounts:
        assert acc.balance == 100.0


def test_withdraw_exact_balance():
    """Invariant: withdrawing the exact balance leaves zero, not negative."""
    acc = BankAccount("Exact", 42.5)
    acc.withdraw(42.5)
    assert acc.balance == 0.0
    with pytest.raises(ValueError):
        acc.withdraw(0.01)
