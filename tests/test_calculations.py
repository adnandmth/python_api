import pytest
from app.calculations import add, subtract, multiply, divide, BankAccount, InsufficientFunds

"""
About fixtures — pytest documentation
Fixtures define the steps and data that constitute the arrange phase of a test (see Anatomy of a test). In pytest, they are functions you define that serve this purpose. They can also be used to define a test's act phase; this is a powerful technique for designing more complex tests.
"""
@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

# special decorator to parameterize multiple computations
# https://docs.pytest.org/en/7.1.x/example/parametrize.html
@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (7, 1, 8),
    (12, 4, 16)
])
def test_add(num1, num2, expected):
    sum = add(num1, num2)
    assert sum == expected

def test_subtract():
    result = subtract(9, 4)
    assert result == 5

def test_multiply():
    result = multiply(2, 4)
    assert result == 8

def test_divide():
    result = divide(2, 2)
    assert result == 1

def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50

def test_bank_set_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_bank_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30

def test_bank_deposit(bank_account):
    bank_account.deposit(20)
    assert bank_account.balance == 70

def test_bank_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55

@pytest.mark.parametrize("deposited, withdrew, expected", [
    (200, 100, 100),
    (500, 500, 0),
    (500, 100, 400)
])
def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected

def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)
