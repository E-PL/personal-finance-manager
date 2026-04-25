"""Command history for managing undo/redo operations."""

from typing import List
from command.transaction_command import Command


class CommandHistory:
    """
    Manages the history of executed commands and provides
    undo/redo capabilities.

    DESIGN PATTERN: Command + Memento (stores command history)
    PURPOSE: Track and manage command execution history
    SOLID PRINCIPLE: Single Responsibility - only manages command
    history

    This class acts as an Invoker that:
    - Executes commands
    - Maintains a history of executed commands
    - Allows undoing recent commands
    - Allows redoing undone commands
    """

    def __init__(self) -> None:
        """Initialize the command history."""
        self.history: List[Command] = []  # Executed commands
        self.redo_stack: List[Command] = []  # Undone commands

    def execute(self, command: Command) -> None:
        """
        Execute a command and record it in history.

        When a new command is executed, the redo stack is cleared
        (you can no longer redo after performing a new action).

        Args:
            command: The command to execute
        """
        command.execute()
        self.history.append(command)
        # Clear redo stack when a new command is executed
        self.redo_stack.clear()

    def undo(self) -> bool:
        """
        Undo the last command.

        Returns:
            bool: True if undo was successful, False if no
            commands to undo
        """
        if not self.history:
            return False

        command = self.history.pop()
        command.undo()
        self.redo_stack.append(command)
        return True

    def redo(self) -> bool:
        """
        Redo the last undone command.

        Returns:
            bool: True if redo was successful, False if no
            commands to redo
        """
        if not self.redo_stack:
            return False

        command = self.redo_stack.pop()
        command.execute()
        self.history.append(command)
        return True

    def get_history_summary(self) -> str:
        """
        Get a summary of the command history.

        Returns:
            str: A formatted summary of executed commands
        """
        if not self.history:
            return "No commands executed yet."

        summary = "Command History:\n"
        for i, command in enumerate(self.history, 1):
            summary += f"  {i}. {command.get_description()}\n"
        return summary

    def can_undo(self) -> bool:
        """Check if undo is available."""
        return len(self.history) > 0

    def can_redo(self) -> bool:
        """Check if redo is available."""
        return len(self.redo_stack) > 0

    def clear(self) -> None:
        """Clear all history and redo stack."""
        self.history.clear()
        self.redo_stack.clear()
