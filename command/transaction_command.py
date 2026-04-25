"""Command pattern implementation for transaction operations."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from balance.balance import Balance
    from transaction.transaction import Transaction


class Command(ABC):
    """
    Abstract base class for all commands.

    DESIGN PATTERN: Command
    PURPOSE: Encapsulate transactions as objects that can be
    queued, logged, undone, and redone
    SOLID PRINCIPLE: Single Responsibility - each command has one
    responsibility (execute)
    SOLID PRINCIPLE: Dependency Inversion - depends on Command
    abstraction
    SOLID PRINCIPLE: Open/Closed - new commands can be added
    without modifying Balance

    By encapsulating operations as command objects, we gain:
    - Ability to undo/redo operations
    - Ability to log operation history
    - Ability to queue operations for later execution
    - Decoupling requestor from executor
    """

    @abstractmethod
    def execute(self) -> None:
        """Execute the command."""
        raise NotImplementedError(
            "Subclasses must implement execute()")

    @abstractmethod
    def undo(self) -> None:
        """Undo the command (restore previous state)."""
        raise NotImplementedError(
            "Subclasses must implement undo()")

    @abstractmethod
    def get_description(self) -> str:
        """Get a description of the command."""
        raise NotImplementedError(
            "Subclasses must implement get_description()")


class ApplyTransactionCommand(Command):
    """
    Command to apply a transaction to the balance.

    Supports undo by storing the previous balance before the
    transaction.
    """

    def __init__(self, balance: "Balance", transaction: "Transaction") -> None:
        """
        Initialize the command.

        Args:
            balance: The Balance instance to apply the transaction to
            transaction: The Transaction to apply
        """
        self.balance = balance
        self.transaction = transaction
        self.previous_balance: float = 0.0

    def execute(self) -> None:
        """
        Execute the command: apply the transaction to the balance.

        Stores the current balance before applying the transaction,
        allowing the operation to be undone later.
        """
        # Save current balance before applying transaction
        self.previous_balance = self.balance.get_balance()

        # Apply the transaction
        self.balance.apply_transaction(self.transaction)

    def undo(self) -> None:
        """
        Undo the command: restore the balance to its previous state.

        By design, we reset the balance to the value it had before
        the command was executed.
        """
        # Reset balance to the state before this transaction
        self.balance._balance = self.previous_balance

    def get_description(self) -> str:
        """Get a description of the command."""
        return f"Apply {self.transaction}"
