"""Module for external freelance income transactions."""


class ExternalFreelanceIncome:
    """
    Represents income from a third-party freelance platform.
    
    This class models external data that needs to be adapted into our internal
    Transaction format using the TransactionAdapter (Adapter pattern).
    
    Attributes:
        amount: The freelance income amount
        invoice_id: The external invoice identifier
        description: Description of the freelance work
        typ: Fixed to "income" since freelance transactions are always income
    """

    def __init__(self, amount: float, invoice_id: str, description: str) -> None:
        """
        Initialize an external freelance income transaction.
        
        Args:
            amount: The freelance income amount (must be positive)
            invoice_id: The invoice ID from the freelance platform
            description: Description of the freelance work performed
        """
        if amount < 0:
            raise ValueError("Amount must be positive")
        if not invoice_id:
            raise ValueError("Invoice ID cannot be empty")
        if not description:
            raise ValueError("Description cannot be empty")

        self.amount: float = amount
        self.invoice_id: str = invoice_id
        self.description: str = description
        self.typ: str = "income"  # Fixed: freelance transactions are always income

    def __str__(self) -> str:
        """Return a string representation."""
        return f"ExternalFreelanceIncome(amount={self.amount}, invoice_id={self.invoice_id}, description={self.description})"

    def __repr__(self) -> str:
        """Return a detailed representation for debugging."""
        return (
            f"ExternalFreelanceIncome(amount={self.amount}, invoice_id={self.invoice_id}, "
            f"description={self.description}, typ={self.typ})"
        )

