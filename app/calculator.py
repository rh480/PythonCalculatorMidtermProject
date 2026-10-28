
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
from app.color_coded import success, error as color_error, warning, info, prompt


from app.operations import OperationFactory


class Calculator:
    """Manage calculator operations and calculation history."""

    def __init__(self, config=None):
        """Set up configuration, logging, an empty history and saved history."""
        self.config = config or CalculatorConfig()

        self.history = []
        self.undo_stack = []
        self.redo_stack = []
        self.operation_strategy = None

        self.operations = OperationFactory
        # Configure logging before registering observers.
        configure_logger(
            self.config.log_file,
            self.config.default_encoding,
        )

        self.config.history_dir.mkdir(parents=True, exist_ok=True)

        self.observers = []
        self.register_observer(LoggingObserver())
        self.register_observer(AutoSaveObserver(self))
        logging.info("Calculator initialized")

        # Restore previously saved history when available.
        try:
            self.load_history()
        except PersistenceError as error:
            logging.warning("Could not load saved history: %s", error)

        self.config.history_dir.mkdir(parents=True, exist_ok=True)
    
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
    
    def remove_observer(self, observer):
        """Stop notifying an observer."""
        self.observers.remove(observer)

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
        try:
            a = InputValidator.validate_number(a, self.config)
            b = InputValidator.validate_number(b, self.config)
            try:
                result = self.operation_strategy.execute(a, b)
            except ArithmeticError as error:  # Decimal overflow and similar
                raise OperationError(f"Calculation failed: {error}") from error
        except CalculatorError as error:
            logging.warning("Calculation rejected: %s", error)
            raise

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
        if len(self.history) > self.config.max_history_size:
            self.history.pop(0)

        self.notify_observers(calculation)
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
            print(info("Goodbye!"))
            break

        if user_input == "history":
            entries = calc.show_history()

            if not entries:
                print(warning("No calculation history yet."))
            else:
                for index, entry in enumerate(entries, start=1):
                    print(info(f"{index}. {entry}"))

            continue

        if user_input == "help":
            print(info("Operations:"))

            for name, description in OperationFactory.available_operations().items():
                print(info(f"  {name:<12} - {description}"))

            print(
                info(
                    "Commands: history, clear, undo, redo, "
                    "save, load, help, exit"
                )
            )
            print(info("Example: add 5 3"))
            continue

        if user_input == "undo":
            if calc.undo():
                print(success("Last action undone."))
            else:
                print(warning("Nothing to undo."))
            continue

        if user_input == "redo":
            if calc.redo():
                print(success("Last action restored."))
            else:
                print(warning("Nothing to redo."))
            continue

        if user_input == "clear":
            calc.clear_history()
            print(success("Calculation history cleared."))
            continue

        if user_input == "save":
            try:
                calc.save_history()
                print(success(f"History saved to {calc.config.history_file}"))
            except PersistenceError as error:
                print(color_error(f"Save failed: {error}"))
            continue


        if user_input == "load":
            try:
                if not calc.config.history_file.exists():
                    print(warning("No saved history file found."))
                    continue

                calc.load_history()
                print(
                    success(
                        f"History loaded. "
                        f"{len(calc.history)} calculation(s) available."
                    )
                )
            except PersistenceError as error:
                print(color_error(f"Load failed: {error}"))
            continue


        parts = user_input.split()

        if len(parts) != 3:
            print(color_error("Invalid input. Example: add 5 3"))
            continue

        operation_name, first, second = parts

        try:
            calc.set_operation(OperationFactory.create_operation(operation_name))
            result = calc.perform_operation(first, second)
            print(success(f"Result: {result}"))
        except CalculatorError as error:
            print(color_error(f"Error: {error}"))
            


def main():
    """Start the calculator application."""
    calculator()


if __name__ == "__main__":
    main()
