# balance.py

from typing import List
from transaction.transaction_category import TransactionCategory


class Balance:
    """
    Singleton class to manage the balance.
    
    DESIGN PATTERN: Singleton
    PURPOSE: Ensures only one instance of Balance exists across the application.
    SOLID PRINCIPLE: Single Responsibility - manages state only; observers handle notifications
    SOLID PRINCIPLE: Dependency Inversion - depends on BalanceObserver abstraction, not concrete implementations
    
    Guarantees:
    - Exactly one instance throughout the application lifecycle
    - All code shares the same balance state
    - Thread-safe instance retrieval (Python GIL ensures thread safety for simple operations)
    """

    _instance: "Balance | None" = None

    def __new__(cls) -> "Balance":
        """
        Override __new__ to implement Singleton pattern.
        
        Returns:
            Balance: The single instance of Balance
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        """Initialize the balance (called only once via __new__)."""
        # Prevent re-initialization on subsequent get_instance() calls
        if self._initialized:
            return
        self._balance: float = 0.0
        self._observers: List["IBalanceObserver"] = []
        self._initialized = True

    @classmethod
    def get_instance(cls) -> "Balance":
        """
        Get the singleton instance of Balance.
        
        Returns:
            Balance: The single instance
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def reset(self) -> None:
        """Reset the net balance to zero."""
        self._balance = 0.0

    def add_income(self, amount: float) -> None:
        """
        Add income to the balance.
        
        Args:
            amount: The amount to add (must be positive)
        """
        if amount < 0:
            raise ValueError("Income amount must be positive")
        self._balance += amount

    def add_expense(self, amount: float) -> None:
        """
        Subtract expense from the balance.
        
        Args:
            amount: The amount to subtract (must be positive; will be subtracted)
        """
        if amount < 0:
            raise ValueError("Expense amount must be positive")
        self._balance -= amount

    def apply_transaction(self, transaction: "Transaction") -> None:
        """
        Apply a Transaction object to update the balance.
        Notifies all registered observers of the transaction.

        Args:
            transaction: The transaction to apply
            
        Raises:
            ValueError: If transaction category is invalid
        """
        # Validate transaction category
        if transaction.category not in TransactionCategory:
            raise ValueError(f"Invalid transaction category: {transaction.category}")

        # Apply the transaction
        if transaction.category == TransactionCategory.INCOME:
            self.add_income(transaction.amount)
        elif transaction.category == TransactionCategory.EXPENSE:
            self.add_expense(transaction.amount)

        # Notify all observers
        self._notify_observers(transaction)

    def get_balance(self) -> float:
        """
        Get the current net balance.
        
        Returns:
            float: The current balance
        """
        return self._balance

    def summary(self) -> str:
        """
        Return a summary string of the net balance.
        
        Returns:
            str: A formatted summary of the balance
        """
        return f"Current Balance: ${self._balance:.2f}"

    def register_observer(self, observer: "IBalanceObserver") -> None:
        """
        Register an observer to be notified of balance updates.
        
        DESIGN PATTERN: Observer
        PURPOSE: Decouples balance updates from alert/notification logic
        
        Args:
            observer: An object implementing the IBalanceObserver interface
        """
        if observer not in self._observers:
            self._observers.append(observer)

    def unregister_observer(self, observer: "IBalanceObserver") -> None:
        """
        Unregister an observer.
        
        Args:
            observer: The observer to remove
        """
        if observer in self._observers:
            self._observers.remove(observer)

    def _notify_observers(self, transaction: "Transaction") -> None:
        """
        Notify all registered observers of a transaction.
        
        Args:
            transaction: The transaction that was applied
        """
        for observer in self._observers:
            observer.update(self, transaction)


# Type hints require forward references
from transaction.transaction import Transaction  # noqa: E402, F401
from balance.balance_observer import IBalanceObserver  # noqa: E402, F401
    
