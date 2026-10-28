
"""Command pattern for calculator REPL actions."""

from abc import ABC, abstractmethod


class Command(ABC):
    """Base class for executable calculator commands."""

    @abstractmethod
    def execute(self):
        """Execute the command."""
        pass


class UndoCommand(Command):
    """Undo the most recent calculator action."""

    def __init__(self, calculator):
        self.calculator = calculator

    def execute(self):
        return self.calculator.undo()


class RedoCommand(Command):
    """Restore the most recently undone calculator action."""

    def __init__(self, calculator):
        self.calculator = calculator

    def execute(self):
        return self.calculator.redo()


class ClearHistoryCommand(Command):
    """Clear the calculator history."""

    def __init__(self, calculator):
        self.calculator = calculator

    def execute(self):
        self.calculator.clear_history()


class HistoryCommand(Command):
    """Retrieve the calculator's formatted history."""

    def __init__(self, calculator):
        self.calculator = calculator

    def execute(self):
        return self.calculator.show_history()


class SaveHistoryCommand(Command):
    """Save the calculator's history."""

    def __init__(self, calculator):
        self.calculator = calculator

    def execute(self):
        return self.calculator.save_history()


class LoadHistoryCommand(Command):
    """Load the calculator's saved history."""

    def __init__(self, calculator):
        self.calculator = calculator

    def execute(self):
        return self.calculator.load_history()
