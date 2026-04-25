"""Tests for the Command pattern implementation."""

import unittest
from balance.balance import Balance
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory
from command.transaction_command import ApplyTransactionCommand
from command.command_history import CommandHistory


class TestApplyTransactionCommand(unittest.TestCase):
    """Test the ApplyTransactionCommand implementation."""

    def setUp(self):
        """Set up test fixtures."""
        self.balance = Balance.get_instance()
        self.balance.reset()

    def test_command_execute(self):
        """Test executing a command applies the transaction."""
        transaction = Transaction(100, TransactionCategory.INCOME)
        command = ApplyTransactionCommand(self.balance, transaction)

        self.assertEqual(self.balance.get_balance(), 0)
        command.execute()
        self.assertEqual(self.balance.get_balance(), 100)

    def test_command_undo(self):
        """Test undoing a command restores previous balance."""
        transaction = Transaction(100, TransactionCategory.INCOME)
        command = ApplyTransactionCommand(self.balance, transaction)

        command.execute()
        self.assertEqual(self.balance.get_balance(), 100)

        command.undo()
        self.assertEqual(self.balance.get_balance(), 0)

    def test_command_execute_and_undo_multiple(self):
        """Test executing and undoing multiple commands."""
        command1 = ApplyTransactionCommand(
            self.balance,
            Transaction(100, TransactionCategory.INCOME)
        )
        command2 = ApplyTransactionCommand(
            self.balance,
            Transaction(50, TransactionCategory.EXPENSE)
        )

        command1.execute()
        self.assertEqual(self.balance.get_balance(), 100)

        command2.execute()
        self.assertEqual(self.balance.get_balance(), 50)

        command2.undo()
        self.assertEqual(self.balance.get_balance(), 100)

        command1.undo()
        self.assertEqual(self.balance.get_balance(), 0)

    def test_command_description(self):
        """Test command description."""
        transaction = Transaction(100, TransactionCategory.INCOME)
        command = ApplyTransactionCommand(self.balance, transaction)
        description = command.get_description()
        self.assertIn("100", description)
        self.assertIn("INCOME", description)


class TestCommandHistory(unittest.TestCase):
    """Test the CommandHistory implementation."""

    def setUp(self):
        """Set up test fixtures."""
        self.balance = Balance.get_instance()
        self.balance.reset()
        self.history = CommandHistory()

    def test_execute_single_command(self):
        """Test executing a single command through history."""
        command = ApplyTransactionCommand(
            self.balance,
            Transaction(100, TransactionCategory.INCOME)
        )
        self.history.execute(command)
        self.assertEqual(self.balance.get_balance(), 100)

    def test_execute_multiple_commands(self):
        """Test executing multiple commands in sequence."""
        command1 = ApplyTransactionCommand(
            self.balance,
            Transaction(100, TransactionCategory.INCOME)
        )
        command2 = ApplyTransactionCommand(
            self.balance,
            Transaction(30, TransactionCategory.EXPENSE)
        )

        self.history.execute(command1)
        self.history.execute(command2)

        self.assertEqual(self.balance.get_balance(), 70)

    def test_undo_single_command(self):
        """Test undoing a single command."""
        command = ApplyTransactionCommand(
            self.balance,
            Transaction(100, TransactionCategory.INCOME)
        )
        self.history.execute(command)

        self.assertTrue(self.history.can_undo())
        self.history.undo()
        self.assertEqual(self.balance.get_balance(), 0)

    def test_undo_multiple_commands(self):
        """Test undoing multiple commands."""
        command1 = ApplyTransactionCommand(
            self.balance,
            Transaction(100, TransactionCategory.INCOME)
        )
        command2 = ApplyTransactionCommand(
            self.balance,
            Transaction(30, TransactionCategory.EXPENSE)
        )

        self.history.execute(command1)
        self.history.execute(command2)

        self.history.undo()
        self.assertEqual(self.balance.get_balance(), 100)

        self.history.undo()
        self.assertEqual(self.balance.get_balance(), 0)

    def test_redo_command(self):
        """Test redoing an undone command."""
        command = ApplyTransactionCommand(
            self.balance,
            Transaction(100, TransactionCategory.INCOME)
        )

        self.history.execute(command)
        self.assertEqual(self.balance.get_balance(), 100)

        self.history.undo()
        self.assertEqual(self.balance.get_balance(), 0)

        self.assertTrue(self.history.can_redo())
        self.history.redo()
        self.assertEqual(self.balance.get_balance(), 100)

    def test_redo_multiple_commands(self):
        """Test redoing multiple commands."""
        command1 = ApplyTransactionCommand(
            self.balance,
            Transaction(100, TransactionCategory.INCOME)
        )
        command2 = ApplyTransactionCommand(
            self.balance,
            Transaction(30, TransactionCategory.EXPENSE)
        )

        self.history.execute(command1)
        self.history.execute(command2)

        self.history.undo()
        self.history.undo()
        self.assertEqual(self.balance.get_balance(), 0)

        self.history.redo()
        self.assertEqual(self.balance.get_balance(), 100)

        self.history.redo()
        self.assertEqual(self.balance.get_balance(), 70)

    def test_redo_cleared_on_new_command(self):
        """Test that redo stack is cleared when a new command is
        executed after undo."""
        command1 = ApplyTransactionCommand(
            self.balance,
            Transaction(100, TransactionCategory.INCOME)
        )
        command2 = ApplyTransactionCommand(
            self.balance,
            Transaction(50, TransactionCategory.EXPENSE)
        )

        self.history.execute(command1)
        self.history.execute(command2)

        self.history.undo()
        self.assertTrue(self.history.can_redo())

        # Execute a new command
        command3 = ApplyTransactionCommand(
            self.balance,
            Transaction(25, TransactionCategory.INCOME)
        )
        self.history.execute(command3)

        # Redo stack should be cleared
        self.assertFalse(self.history.can_redo())

    def test_can_undo_redo_flags(self):
        """Test can_undo and can_redo flags."""
        command = ApplyTransactionCommand(
            self.balance,
            Transaction(100, TransactionCategory.INCOME)
        )

        self.assertFalse(self.history.can_undo())
        self.assertFalse(self.history.can_redo())

        self.history.execute(command)
        self.assertTrue(self.history.can_undo())
        self.assertFalse(self.history.can_redo())

        self.history.undo()
        self.assertFalse(self.history.can_undo())
        self.assertTrue(self.history.can_redo())

    def test_history_summary(self):
        """Test history summary generation."""
        command1 = ApplyTransactionCommand(
            self.balance,
            Transaction(100, TransactionCategory.INCOME)
        )
        command2 = ApplyTransactionCommand(
            self.balance,
            Transaction(30, TransactionCategory.EXPENSE)
        )

        self.history.execute(command1)
        self.history.execute(command2)

        summary = self.history.get_history_summary()
        self.assertIn("Command History:", summary)
        self.assertIn("Apply", summary)

    def test_clear_history(self):
        """Test clearing history."""
        command = ApplyTransactionCommand(
            self.balance,
            Transaction(100, TransactionCategory.INCOME)
        )
        self.history.execute(command)

        self.assertTrue(self.history.can_undo())
        self.history.clear()
        self.assertFalse(self.history.can_undo())


if __name__ == "__main__":
    unittest.main()
