# transaction.py

from typing import Any
from transaction.transaction_category import TransactionCategory


class Transaction:
    """
    Represents a financial transaction with an amount and category.
    
    SOLID PRINCIPLE: Single Responsibility
    This class has one reason to change: the structure of a transaction.
    Transaction application logic is in the Balance class (not here).
    """

    def __init__(self, amount: float, category: Any) -> None:
        """
        Initialize a Transaction.
        
        Args:
            amount: The transaction amount (must be positive)
            category: The transaction category (typically INCOME or EXPENSE)
        """
        if amount < 0:
            raise ValueError("Transaction amount must be positive")
        
        self.amount: float = amount
        self.category: Any = category  # Accept any category; Balance will validate

    def __str__(self) -> str:
        """
        Return a formatted string representation of the transaction.
        
        Returns:
            str: Formatted string showing amount and category
        """
        return f"Transaction(${self.amount}, category='{self.category}')"

    def __eq__(self, other: Any) -> bool:
        """
        Check equality between two Transaction objects.
        
        Two transactions are equal if they have the same amount and category.
        
        Args:
            other: Another object to compare
            
        Returns:
            bool: True if transactions are equal, False otherwise
        """
        if not isinstance(other, Transaction):
            return False
        return self.amount == other.amount and self.category == other.category

    def __repr__(self) -> str:
        """
        Return a detailed string representation for debugging.
        
        Returns:
            str: Detailed representation
        """
        return f"Transaction(amount={self.amount}, category={self.category})"

