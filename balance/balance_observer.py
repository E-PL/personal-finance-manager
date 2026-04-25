# balance_observer.py

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from balance.balance import Balance
    from transaction.transaction import Transaction


class IBalanceObserver(ABC):
    """
    Abstract base class for balance observers.
    
    DESIGN PATTERN: Observer
    PURPOSE: Define a contract for objects that want to be notified of balance changes
    SOLID PRINCIPLE: Single Responsibility - each observer has one specific responsibility
    SOLID PRINCIPLE: Dependency Inversion - Balance depends on this abstraction, not concrete observers
    SOLID PRINCIPLE: Open/Closed - new observers can be added without modifying Balance
    
    Any class that needs to react to balance changes should implement this interface.
    """

    @abstractmethod
    def update(self, balance: "Balance", transaction: "Transaction") -> None:
        """
        Handle a balance update notification.
        
        Args:
            balance: The Balance instance that changed
            transaction: The Transaction that was applied
        """
        raise NotImplementedError("Subclasses must implement update method.")


class PrintObserver(IBalanceObserver):
    """
    Observer that prints the balance whenever it is updated.
    
    SOLID PRINCIPLE: Single Responsibility - only prints balance updates
    This observer is not concerned with th balance value or transaction details,
    only with printing whenever an update occurs.
    """

    def update(self, balance: "Balance", transaction: "Transaction") -> None:
        """
        Print the updated balance after a transaction.
        
        Args:
            balance: The Balance instance that changed
            transaction: The transaction that was applied (for context)
        """
        print(f"Balance updated: {balance.summary()}")


class LowBalanceAlertObserver(IBalanceObserver):
    """
    Observer that triggers an alert when balance falls below a threshold.
    
    SOLID PRINCIPLE: Single Responsibility - only monitors for low balance
    This observer encapsulates the logic for determining when an alert should be triggered.
    """

    def __init__(self, threshold: float) -> None:
        """
        Initialize the low balance alert observer.
        
        Args:
            threshold: The balance threshold below which an alert should trigger
        """
        if threshold < 0:
            raise ValueError("Threshold must be non-negative")
        self.threshold: float = threshold
        self.alert_triggered: bool = False

    def update(self, balance: "Balance", transaction: "Transaction") -> None:
        """
        Check balance and trigger alert if it falls below threshold.
        
        Args:
            balance: The Balance instance that changed
            transaction: The transaction that was applied (for context)
        """
        current_balance = balance.get_balance()
        
        # Trigger alert if balance is below threshold
        if current_balance < self.threshold:
            self.alert_triggered = True
            self._trigger_alert(current_balance)
        else:
            # Clear alert if balance is above threshold
            self.alert_triggered = False

    def _trigger_alert(self, current_balance: float) -> None:
        """
        Trigger a low balance alert.
        
        Args:
            current_balance: The current balance value
        """
        print(f"** LOW BALANCE ALERT: Balance (${current_balance:.2f}) is below threshold (${self.threshold:.2f})")

