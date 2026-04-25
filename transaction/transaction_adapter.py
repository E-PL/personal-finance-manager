# transaction_adapter.py

from typing import TYPE_CHECKING
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory

if TYPE_CHECKING:
    from transaction.external_income_transaction import ExternalFreelanceIncome


class TransactionAdapter:
    """
    Adapter pattern implementation for converting external transactions to internal format.
    
    DESIGN PATTERN: Adapter
    PURPOSE: Convert incompatible external data formats (ExternalFreelanceIncome) 
             into our internal Transaction format without modifying either class.
    SOLID PRINCIPLE: Open/Closed - new external formats can be supported via new adapters
    SOLID PRINCIPLE: Single Responsibility - only handles external → internal conversion
    SOLID PRINCIPLE: Interface Segregation - adaptor presents only the to_transaction() interface
    
    Benefits:
    - Decouples external data sources from internal business logic
    - Makes the application flexible to support different external formats
    - Can add new adapters for new external data sources without changing existing code
    """

    def __init__(self, external_transaction: "ExternalFreelanceIncome") -> None:
        """
        Initialize the adapter with an external transaction.
        
        Args:
            external_transaction: The external transaction to adapt (e.g., ExternalFreelanceIncome)
        """
        self.external_transaction = external_transaction

    def to_transaction(self) -> Transaction:
        """
        Convert an external transaction to a standard Transaction.
        
        For ExternalFreelanceIncome:
        - The 'amount' is directly mapped to Transaction amount
        - The 'typ' field indicates it's always INCOME for freelance work
        - The invoice_id and description are metadata (not stored in Transaction)
        
        Returns:
            Transaction: A Transaction object compatible with the Balance class
            
        Raises:
            AttributeError: If external_transaction doesn't have expected attributes
            ValueError: If the external transaction type is not recognized
        """
        # Extract the external transaction's type field
        if not hasattr(self.external_transaction, 'typ'):
            raise AttributeError(
                f"External transaction must have 'typ' attribute. "
                f"Got {type(self.external_transaction).__name__}"
            )

        if not hasattr(self.external_transaction, 'amount'):
            raise AttributeError(
                f"External transaction must have 'amount' attribute. "
                f"Got {type(self.external_transaction).__name__}"
            )

        # Validate transaction type
        transaction_type = self.external_transaction.typ
        if transaction_type.lower() != "income":
            raise ValueError(
                f"Unsupported external transaction type: {transaction_type}. "
                f"Only 'income' is currently supported."
            )

        # Create and return a standard Transaction
        # ExternalFreelanceIncome is always income, so we use INCOME category
        return Transaction(
            amount=self.external_transaction.amount,
            category=TransactionCategory.INCOME
        )

