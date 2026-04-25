import unittest
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory
from balance.balance import Balance
from balance.balance_observer import LowBalanceAlertObserver


class TestLowBalanceAlertObserver(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()

    def test_alert_triggers_on_low_balance(self):
        observer = LowBalanceAlertObserver(threshold=50)
        self.balance.register_observer(observer)

        income_tx = Transaction(100, TransactionCategory.INCOME)
        self.balance.apply_transaction(income_tx)
        self.assertFalse(observer.alert_triggered)

        expense_tx = Transaction(60, TransactionCategory.EXPENSE)
        self.balance.apply_transaction(expense_tx)
        self.assertTrue(observer.alert_triggered)

        income_tx2 = Transaction(100, TransactionCategory.INCOME)
        self.balance.apply_transaction(income_tx2)
        self.assertFalse(observer.alert_triggered)

        expense_tx2 = Transaction(60, TransactionCategory.EXPENSE)
        self.balance.apply_transaction(expense_tx2)
        self.assertFalse(observer.alert_triggered)

        expense_tx3 = Transaction(60, TransactionCategory.EXPENSE)
        self.balance.apply_transaction(expense_tx3)
        self.assertTrue(observer.alert_triggered)


if __name__ == "__main__":
    unittest.main()
