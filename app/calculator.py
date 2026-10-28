
"""Command-line interface for the basic calculator."""

import logging
from decimal import Decimal, InvalidOperation

import pandas as pd

from app.calculation import Calculation
from app.calculator_config import CalculatorConfig
from app.calculator_memento import CalculatorMemento
from app.exceptions import CalculatorError, OperationError, ValidationError, PersistenceError
from app.history import LoggingObserver, AutoSaveObserver
from app.input_validators import InputValidator
from app.logger import configure_logger


from app.operations import (
    OperationError,
    Addition,
    Subtraction,
    Multiplication,
    Division,
    Power,
    Root,
    Modulus,
    IntegerDivision,
    Percentage,
    AbsoluteDifference,
)


class Calculator:
    """Manage calculator operations and calculation history."""

    def __init__(self, config=None):
        """Set up configuration, logging, an empty history and saved history."""
        self.config = config or CalculatorConfig()

        self.history = []
        self.undo_stack = []
        self.redo_stack = []
        self.operation_strategy = None

        # Map commands to their operation classes.
        self.operations = {
            "add": Addition,
            "subtract": Subtraction,
            "multiply": Multiplication,
            "divide": Division,
            "power": Power,
            "root": Root,
            "modulus": Modulus,
            "int_divide": IntegerDivision,
            "percent": Percentage,
            "abs_diff": AbsoluteDifference,
            "absolute_difference": AbsoluteDifference,
        }

        self.observers = []
        self.register_observer(LoggingObserver())
        self.register_observer(AutoSaveObserver(self))

        # Configure logging before registering observers.
        configure_logger(
            self.config.log_file,
            self.config.default_encoding,
        )

        self.config.history_dir.mkdir(parents=True, exist_ok=True)

        # Restore previously saved history when available.
        try:
            self.load_history()
        except PersistenceError as error:
            logging.warning("Could not load saved history: %s", error)
    
    def register_observer(self, observer):
        """Add an observer that is told about every new calculation."""
        self.observers.append(observer)

    def notify_observers(self, calculation):
        """Tell every observer about a calculation.

        A failing observer (for example a save error) is logged but cannot
        stop the other observers or lose the calculation result.
        """
        for observer in self.observers:
            try:
                observer.update(calculation)
            except CalculatorError as error:
                logging.error(
                    "Observer %s failed: %s", type(observer).__name__, error
                )

    def save_history(self, file_path=None):
        """Save calculation history to a CSV file."""
        path = file_path or self.config.history_file

        columns = [
            "operation",
            "operand1",
            "operand2",
            "result",
            "timestamp",
        ]

        try:
            path.parent.mkdir(parents=True, exist_ok=True)

            records = [item.to_dict() for item in self.history]
            dataframe = pd.DataFrame(records, columns=columns)

            dataframe.to_csv(
                path,
                index=False,
                encoding=self.config.default_encoding,
            )
            logging.info("History saved to %s", path)

        except (OSError, ValueError, TypeError) as error:
            logging.error("Could not save history: %s", error)
            raise PersistenceError(
                f"Could not save history: {error}"
            ) from error

    def load_history(self, file_path=None):
        """Load calculation history from a CSV file."""
        path = file_path or self.config.history_file

        if not path.exists():
            return

        try:
            dataframe = pd.read_csv(
                path,
                dtype=str,
                keep_default_na=False,
                encoding=self.config.default_encoding,
            )

            required_columns = {
                "operation",
                "operand1",
                "operand2",
                "result",
                "timestamp",
            }

            if not required_columns.issubset(dataframe.columns):
                raise ValueError("History CSV is missing required columns.")

            loaded_history = [
                Calculation.from_dict(row)
                for row in dataframe.to_dict(orient="records")
            ]

            # Apply the configured history limit to loaded records.
            self.history = loaded_history[-self.config.max_history_size:]
            self.undo_stack.clear()
            self.redo_stack.clear()

            logging.info("Loaded %s calculations", len(self.history))

        except (OSError, ValueError, TypeError, KeyError) as error:
            logging.error("Could not load history: %s", error)
            raise PersistenceError(
                f"Could not load history: {error}"
            ) from error



    def get_history_dataframe(self):
        """Return calculation history as a pandas DataFrame."""
        return pd.DataFrame(
            [item.to_dict() for item in self.history],
            columns=[
                "operation",
                "operand1",
                "operand2",
                "result",
                "timestamp",
            ],
        )

    def show_history(self):
        """Return a formatted list of previous calculations."""
        return [
            f"{item.operation}({item.operand1}, {item.operand2}) = "
            f"{item.result}"
            for item in self.history
        ]

    def clear_history(self):
        """Clear calculation history while allowing undo."""
        if self.history:
            self.undo_stack.append(
                CalculatorMemento.create(self.history)
            )
            self.redo_stack.clear()
            self.history.clear()

    def set_operation(self, operation):
        """Set the operation strategy used for a calculation."""
        self.operation_strategy = operation


    def perform_operation(self, a, b):
        """Execute the selected operation and record the calculation."""
        if self.operation_strategy is None:
            raise OperationError("No operation set.")

        result = self.operation_strategy.execute(a, b)

        calculation = Calculation(
            operation=str(self.operation_strategy),
            operand1=a,
            operand2=b,
            result=result,
        )

        # Save the current history before adding the new calculation.
        self.undo_stack.append(
            CalculatorMemento.create(self.history)
        )

        # A new calculation invalidates previously undone actions.
        self.redo_stack.clear()

        self.history.append(calculation)
        return result


    def undo(self):
        """Restore the previous calculator history."""
        if not self.undo_stack:
            return False

        self.redo_stack.append(
            CalculatorMemento.create(self.history)
        )

        previous_state = self.undo_stack.pop()
        self.history = previous_state.get_history()
        return True

    def redo(self):
        """Reapply the last undone calculator history."""
        if not self.redo_stack:
            return False

        self.undo_stack.append(
            CalculatorMemento.create(self.history)
        )

        next_state = self.redo_stack.pop()
        self.history = next_state.get_history()
        return True


def calculator():
    """Run the calculator command-line interface."""
    calc = Calculator()

    print("Welcome to the calculator! Type 'exit' to quit. Type 'help' for commands.")

    while True:
        user_input = input(
            "Enter an operation and two numbers: "
        ).strip().lower()

        if user_input == "exit":
            print("Goodbye!")
            break

        if user_input == "history":
            entries = calc.show_history()

            if not entries:
                print("No calculation history yet.")
            else:
                for index, entry in enumerate(entries, start=1):
                    print(f"{index}. {entry}")

            continue

        if user_input == "help":
            print("Operations: " + ", ".join(calc.operations))
            print(
                "Commands: history, clear, undo, redo, "
                "save, load, help, exit"
            )
            print("Example: add 5 3")
            continue

        if user_input == "undo":
            print(
                "Last action undone."
                if calc.undo()
                else "Nothing to undo."
            )
            continue

        if user_input == "redo":
            print(
                "Last action restored."
                if calc.redo()
                else "Nothing to redo."
            )
            continue

        if user_input == "clear":
            calc.clear_history()
            print("Calculation history cleared.")
            continue

        if user_input == "save":
            try:
                calc.save_history()
                print(f"History saved to {calc.config.history_file}")
            except PersistenceError as error:
                print(f"Save failed: {error}")
            continue


        if user_input == "load":
            try:
                if not calc.config.history_file.exists():
                    print("No saved history file found.")
                    continue

                calc.load_history()
                print(
                    f"History loaded. "
                    f"{len(calc.history)} calculation(s) available."
                )
            except PersistenceError as error:
                print(f"Load failed: {error}")
            continue


        parts = user_input.split()

        if len(parts) != 3:
            print("Invalid input. Example: add 5 3")
            continue

        operation_name, first, second = parts

        if operation_name not in calc.operations:
            print(
                f"Unknown operation: {operation_name}. "
                "Example: add 5 3"
            )
            continue

        try:
            a = Decimal(first)
            b = Decimal(second)

            operation_class = calc.operations[operation_name]
            calc.set_operation(operation_class())

            result = calc.perform_operation(a, b)
            print(f"Result: {result}")

        except (InvalidOperation, ValueError):
            print(
                "Invalid numbers. Please enter valid numbers. "
                "Example: add 5 3"
            )
        except OperationError as error:
            print(f"Error: {error}")


def main():
    """Start the calculator application."""
    calculator()


if __name__ == "__main__":
    main()
