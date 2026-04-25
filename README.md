# Personal Finance Manager - Design Patterns Implementation

A comprehensive demonstration of Object-Oriented Design Patterns applied to personal finance tracking in Python.

## Project Overview

This application implements a personal finance manager that:
- Tracks income and expenses with a centralized balance
- Alerts users when balance falls below a threshold
- Converts external freelance income data into internal format
- Provides undo/redo capability for transactions
- Demonstrates four key design patterns working together

## Design Patterns Implemented

### 1. **Singleton Pattern** (Creational) - Balance Management

**Purpose**: Ensure only one instance of the Balance class exists throughout the application.

**Implementation**: 
- `Balance` class with `__new__()` override
- `Balance.get_instance()` provides global access point
- Tests verify same object returned on multiple calls

**SOLID Principles**:
- Single Responsibility: Balance only manages financial state
- Dependency Inversion: Clients depend on Balance interface

```python
balance = Balance.get_instance()  # Always returns same instance
balance.add_income(100)
balance.apply_transaction(transaction)
```

### 2. **Observer Pattern** (Behavioral) - Event Notification

**Purpose**: Decouple balance updates from their reactive behaviors.

**Implementation**:
- `IBalanceObserver` abstract base class defines interface
- `PrintObserver`: Prints balance after each transaction
- `LowBalanceAlertObserver`: Triggers alert when balance < threshold
- `Balance` maintains observer list and notifies on updates

**SOLID Principles**:
- Open/Closed: New observers added without modifying Balance
- Dependency Inversion: Balance depends on abstraction, not concrete observers
- Interface Segregation: Minimal update() interface

```python
# Register observers
print_observer = PrintObserver()
balance.register_observer(print_observer)

low_balance_observer = LowBalanceAlertObserver(threshold=100)
balance.register_observer(low_balance_observer)

# Both notified automatically on transaction
balance.apply_transaction(transaction)
```

### 3. **Adapter Pattern** (Structural) - External Data Integration

**Purpose**: Convert incompatible external data formats to internal representation.

**Implementation**:
- `ExternalFreelanceIncome`: Third-party freelance platform format
- `TransactionAdapter`: Converts external to internal Transaction format
- Validates external data and maps to standard Transaction

**SOLID Principles**:
- Open/Closed: New adapters for new external formats without modifying Balance
- Single Responsibility: Adapter only handles conversion
- Dependency Inversion: Application uses Transaction interface

```python
# External data from third-party
freelance_income = ExternalFreelanceIncome(
    amount=1200, 
    invoice_id="INV-98765",
    description="Mobile App Project"
)

# Adapt to internal format
adapter = TransactionAdapter(freelance_income)
transaction = adapter.to_transaction()

# Now usable with Balance
balance.apply_transaction(transaction)
```

### 4. **Command Pattern** (Behavioral) - Undo/Redo Transactions

**Purpose**: Encapsulate transaction operations as objects to enable undo/redo.

**Implementation**:
- `Command` abstract base class with execute/undo interface
- `ApplyTransactionCommand`: Encapsulates transaction application
- `CommandHistory`: Manages command execution, undo, and redo stacks

**SOLID Principles**:
- Open/Closed: New command types without modifying CommandHistory
- Single Responsibility: Each class has one reason to change
- Dependency Inversion: History depends on Command abstraction

```python
history = CommandHistory()

# Execute transactions through history (enables undo/redo)
command = ApplyTransactionCommand(balance, transaction)
history.execute(command)

# Undo/redo operations
history.undo()       # Reverses last transaction
history.redo()       # Restores last undone transaction

# View operation history
print(history.get_history_summary())
```

## Project Structure

```
.
├── balance/
│   ├── balance.py              # Singleton Balance class
│   ├── balance_observer.py     # Observer interface and implementations
│   ├── test_balance.py         # 8 unit tests
│   └── test_balance_observer.py # 1 integration test
│
├── transaction/
│   ├── transaction.py          # Transaction entity
│   ├── transaction_category.py # TransactionCategory enum (INCOME/EXPENSE)
│   ├── transaction_adapter.py  # Adapter pattern implementation
│   ├── external_income_transaction.py # External freelance data
│   ├── test_transaction.py     # 3 unit tests
│   └── test_transaction_adapter.py # 1 test
│
├── command/
│   ├── transaction_command.py  # Command pattern implementation
│   ├── command_history.py      # CommandHistory invoker class
│   └── test_command.py         # 14 comprehensive tests
│
├── main.py                      # Application entry point
├── REFLECTION.md               # Detailed pattern reflection (700+ words)
└── README.md                   # This file
```

## Installation & Running

### Requirements
- Python 3.10+ 
- Standard library only (no external dependencies)

### Setup
```bash
cd personal-finance-manager/cd14600-project-starter/starter
```

### Run Application
```bash
python main.py
```

Expected output:
- Demonstrates all 4 patterns
- Processes transactions with observers
- Shows undo/redo capability
- Completes in <1 second

### Run Tests
```bash
# All tests
python -m unittest balance.test_balance transaction.test_transaction \
  transaction.test_transaction_adapter balance.test_balance_observer \
  command.test_command -v

# Specific module tests
python -m unittest balance.test_balance -v
python -m unittest command.test_command -v

# Expected: 27 tests, all passing ✓
```

## Code Quality

- **Type Hints**: 100% - All functions have Python 3.10+ type hints
- **Documentation**: Comprehensive docstrings with SOLID principle explanations
- **Code Style**: PEP8 compliant throughout
- **Test Coverage**: 27 tests across all modules
- **Modularity**: Clear separation of concerns across 6 modules

## Key Testing Results

```
Ran 27 tests - OK ✓

Module breakdown:
- balance.test_balance: 8 tests ✓
- transaction.test_transaction: 3 tests ✓
- transaction.test_transaction_adapter: 1 test ✓
- balance.test_balance_observer: 1 test ✓
- command.test_command: 14 tests ✓
```

## SOLID Principles Compliance

**S - Single Responsibility**
- Balance: manages state only
- Each observer: one reaction type
- Adapter: conversion only

**O - Open/Closed**
- Add observers without modifying Balance
- Add adapters for new external formats
- Add commands without modifying CommandHistory

**L - Liskov Substitution**
- All observers are interchangeable
- All commands have compatible contract

**I - Interface Segregation**
- `IBalanceObserver`: single `update()` method
- `Command`: focused interface

**D - Dependency Inversion**
- Balance → IBalanceObserver abstraction
- CommandHistory → Command abstraction

## Key Features

✓ Singleton Pattern - Enforces single Balance instance  
✓ Observer Pattern - Automatic notification of balance changes  
✓ Adapter Pattern - Converts external freelance income  
✓ Command Pattern - Undo/redo transactions  
✓ Type Hints - 100% coverage (Python 3.10+)  
✓ Unit Tests - 27 passing tests  
✓ PEP8 Compliance - Clean, Pythonic code  
✓ Documentation - Comprehensive reflecting document included  

## Reflection & Documentation

See [REFLECTION.md](REFLECTION.md) for a detailed 700+ word reflection explaining:
- Each pattern's purpose and implementation
- SOLID principle compliance for each pattern
- Benefits and trade-offs observed
- How all patterns work together
- Lessons learned during implementation
- Rubric compliance verification

## Future Enhancements

- Multiple external format adapters (factory pattern)
- Transaction history persistence
- Advanced budgeting strategies (strategy pattern)
- Transaction validation (decorator pattern)
- Batch transaction processing (composite pattern)

---
**Status**: Complete - All patterns implemented, tested, and documented ✓  
**Version**: 1.0.0  
**Python**: 3.10+  
**Dependencies**: None (standard library only)
# Purpose of this Folder

This folder should contain the scaffolded project files to get a student started on their project. This repo will be added to the Classroom for students to use, so please do not have any solutions in this folder.
