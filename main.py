"""
Personal Finance Manager Application

This module demonstrates Object-Oriented Design Patterns applied to personal finance tracking.

DESIGN PATTERNS IMPLEMENTED:
1. Singleton Pattern - Balance class ensures only one instance exists
2. Observer Pattern - LowBalanceAlertObserver and PrintObserver react to balance changes
3. Adapter Pattern - TransactionAdapter converts external freelance income to internal format
4. Command Pattern - ApplyTransactionCommand provides undo/redo capability

SOLID PRINCIPLES:
- Single Responsibility: Each class has one reason to change
- Open/Closed: New observers and adapters can be added without modifying existing code
- Dependency Inversion: Balance depends on observer abstraction, not concrete implementations
- Interface Segregation: Minimal, focused interfaces
- Liskov Substitution: All observers are interchangeable

The application tracks financial transactions, manages balance,
and notifies observers of significant balance changes.
"""

from balance.balance import Balance
from balance.balance_observer import LowBalanceAlertObserver, PrintObserver
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory
from transaction.transaction_adapter import TransactionAdapter
from transaction.external_income_transaction import ExternalFreelanceIncome
from command.transaction_command import ApplyTransactionCommand
from command.command_history import CommandHistory


def main() -> None:
    """
    Main application entry point.
    
    Demonstrates:
    - Singleton Pattern: Getting the single Balance instance
    - Observer Pattern: Registering observers to receive notifications
    - Adapter Pattern: Converting external freelance income to internal format
    - Command Pattern: Executing, undoing, and redoing transactions
    - Transaction Processing: Applying various transactions to track balance changes
    """
    print("=" * 70)
    print("Personal Finance Manager - Design Patterns Demonstration")
    print("=" * 70)
    print()

    # SINGLETON PATTERN: Get the single instance of Balance
    # No matter where in the code, Balance.get_instance() always returns the same object
    balance = Balance.get_instance()
    balance.reset()
    print("✓ Singleton Pattern: Balance instance created (only one exists)")
    print()

    # OBSERVER PATTERN: Register observers to be notified of balance changes
    print("Setting up observers...")
    
    # Observer 1: Print balance after each transaction
    print_observer = PrintObserver()
    balance.register_observer(print_observer)
    print("  ✓ PrintObserver registered - will print balance after each transaction")
    
    # Observer 2: Alert when balance falls below threshold
    low_balance_alert = LowBalanceAlertObserver(threshold=100)
    balance.register_observer(low_balance_alert)
    print("  ✓ LowBalanceAlertObserver registered - will alert when balance < $100")
    print()

    # COMMAND PATTERN: Create command history for undo/redo
    print("Initializing command history for undo/redo capability...")
    history = CommandHistory()
    print("  ✓ CommandHistory initialized")
    print()

    print("Processing transactions...")
    print("-" * 70)

    # Standard income transactions using Command Pattern
    transactions = [
        Transaction(500, TransactionCategory.INCOME),    # Add $500 income
        Transaction(150, TransactionCategory.EXPENSE),   # Remove $150 expense
        Transaction(200, TransactionCategory.INCOME),    # Add $200 income
    ]

    print("\n1. Processing standard transactions with Command Pattern (undo/redo capable):")
    for i, transaction in enumerate(transactions, 1):
        print(f"\n   Transaction {i}: {transaction}")
        # Create command instead of applying directly
        command = ApplyTransactionCommand(balance, transaction)
        # Execute through history (enables undo/redo)
        history.execute(command)

    print("\n" + "-" * 70)

    # ADAPTER PATTERN: Convert external freelance income to internal Transaction
    print("\n2. Processing external freelance income (using Adapter Pattern):")
    freelance_income = ExternalFreelanceIncome(
        amount=1200,
        invoice_id="INV-98765",
        description="Mobile App Development Project"
    )
    print(f"\n   External Transaction: {freelance_income}")
    
    adapter = TransactionAdapter(freelance_income)
    adapted_transaction = adapter.to_transaction()
    print(f"   Adapted to: {adapted_transaction}")
    
    print("\n   Applying adapted transaction...")
    command = ApplyTransactionCommand(balance, adapted_transaction)
    history.execute(command)

    print("\n" + "-" * 70)
    print(f"\nCurrent {balance.summary()}")
    
    # Demonstrate UNDO/REDO capability (Command Pattern)
    print("\n3. Demonstrating Undo/Redo Capability (Command Pattern):")
    print(f"\n   Command History Summary:")
    print("   " + history.get_history_summary().replace("\n", "\n   "))
    
    print("   Undoing last transaction...")
    if history.undo():
        print(f"   ✓ Undo successful! {balance.summary()}")
    
    print("\n   Undoing one more transaction...")
    if history.undo():
        print(f"   ✓ Undo successful! {balance.summary()}")
    
    print("\n   Redoing last transaction...")
    if history.redo():
        print(f"   ✓ Redo successful! {balance.summary()}")

    print("\n" + "-" * 70)
    print(f"\nFinal {balance.summary()}")
    print()
    print("=" * 70)
    print("Application completed successfully!")
    print("=" * 70)
    print()
    print("PATTERN SUMMARY:")
    print("  • Singleton: Balance.get_instance() always returns the same object")
    print("  • Observer: PrintObserver and LowBalanceAlertObserver updated automatically")
    print("  • Adapter: ExternalFreelanceIncome converted to Transaction format")
    print("  • Command: ApplyTransactionCommand enables undo/redo of transactions")
    print()


if __name__ == "__main__":
    main()
