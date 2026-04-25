"""
Personal Finance Manager Application

This module demonstrates Object-Oriented Design Patterns applied
to personal finance tracking.

DESIGN PATTERNS IMPLEMENTED:
1. Singleton Pattern - Balance class ensures only one instance
   exists
2. Observer Pattern - LowBalanceAlertObserver and PrintObserver
   react to balance changes
3. Adapter Pattern - TransactionAdapter converts external freelance
   income to internal format
4. Command Pattern - ApplyTransactionCommand provides undo/redo
   capability

SOLID PRINCIPLES:
- Single Responsibility: Each class has one reason to change
- Open/Closed: New observers and adapters can be added without
  modifying existing code
- Dependency Inversion: Balance depends on observer abstraction,
  not concrete implementations
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


def setup_observers(balance: Balance) -> None:
    """
    Register observers to the balance instance.

    Observer Pattern: Attach observers that react to balance changes.
    """
    print("Setting up observers...")

    print_observer = PrintObserver()
    balance.register_observer(print_observer)
    print("  ✓ PrintObserver registered - will print balance after each "
          "transaction")

    low_balance_alert = LowBalanceAlertObserver(threshold=100)
    balance.register_observer(low_balance_alert)
    print("  ✓ LowBalanceAlertObserver registered - will alert when "
          "balance < $100")
    print()


def process_standard_transactions(balance: Balance,
                                  history: CommandHistory) -> None:
    """
    Process standard income and expense transactions.

    Command Pattern: Execute transactions through command history to
    enable undo/redo.
    """
    msg = ("\n1. Processing standard transactions with Command "
           "Pattern (undo/redo capable):")
    print(msg)

    transactions = [
        Transaction(500, TransactionCategory.INCOME),
        Transaction(150, TransactionCategory.EXPENSE),
        Transaction(200, TransactionCategory.INCOME),
    ]

    for i, transaction in enumerate(transactions, 1):
        print(f"\n   Transaction {i}: {transaction}")
        command = ApplyTransactionCommand(balance, transaction)
        history.execute(command)


def process_external_transaction(balance: Balance,
                                 history: CommandHistory) -> None:
    """
    Process external freelance income using adapter pattern.

    Adapter Pattern: Convert external format (ExternalFreelanceIncome)
    to internal format (Transaction).
    """
    msg = ("\n2. Processing external freelance income (using "
           "Adapter Pattern):")
    print(msg)

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


def demonstrate_undo_redo(balance: Balance,
                          history: CommandHistory) -> None:
    """
    Demonstrate undo/redo capabilities.

    Command Pattern: Show how transactions can be undone and redone
    using the command history.
    """
    msg = ("\n3. Demonstrating Undo/Redo Capability "
           "(Command Pattern):")
    print(msg)

    print(f"\n   Command History Summary:")
    summary = history.get_history_summary()
    print("   " + summary.replace("\n", "\n   "))

    print("   Undoing last transaction...")
    if history.undo():
        print(f"   ✓ Undo successful! {balance.summary()}")

    print("\n   Undoing one more transaction...")
    if history.undo():
        print(f"   ✓ Undo successful! {balance.summary()}")

    print("\n   Redoing last transaction...")
    if history.redo():
        print(f"   ✓ Redo successful! {balance.summary()}")


def print_application_summary() -> None:
    """Print summary of design patterns used in the application."""
    print("=" * 70)
    print("Application completed successfully!")
    print("=" * 70)
    print()
    print("PATTERN SUMMARY:")
    print("  • Singleton: Balance.get_instance() always returns the "
          "same object")
    msg = ("  • Observer: PrintObserver and LowBalanceAlertObserver "
           "updated automatically")
    print(msg)
    print("  • Adapter: ExternalFreelanceIncome converted to "
          "Transaction format")
    msg = ("  • Command: ApplyTransactionCommand enables undo/redo of "
           "transactions")
    print(msg)
    print()


def main() -> None:
    """
    Main application entry point.

    Orchestrates the demonstration of design patterns:
    - Singleton Pattern: Single Balance instance
    - Observer Pattern: Automatic notifications on balance changes
    - Adapter Pattern: External-to-internal format conversion
    - Command Pattern: Transaction execution with undo/redo
    """
    print("=" * 70)
    print("Personal Finance Manager - Design Patterns Demonstration")
    print("=" * 70)
    print()

    balance = Balance.get_instance()
    balance.reset()
    print("✓ Singleton Pattern: Balance instance created (only one)")
    print()

    setup_observers(balance)

    print("Initializing command history for undo/redo capability...")
    history = CommandHistory()
    print("  ✓ CommandHistory initialized")
    print()

    print("Processing transactions...")
    print("-" * 70)

    process_standard_transactions(balance, history)
    print("\n" + "-" * 70)

    process_external_transaction(balance, history)
    print("\n" + "-" * 70)
    print(f"\nCurrent {balance.summary()}")

    demonstrate_undo_redo(balance, history)

    print("\n" + "-" * 70)
    print(f"\nFinal {balance.summary()}")
    print()

    print_application_summary()


if __name__ == "__main__":
    main()
