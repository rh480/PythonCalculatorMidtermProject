
"""Command-line interface for the basic calculator."""

from decimal import Decimal, InvalidOperation
from app.calculator_memento import CalculatorMemento

from app.calculation import Calculation
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

    def __init__(self):
        """Initialize available operations and an empty history."""
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


def calculator():
    """Run the calculator command-line interface."""
    calc = Calculator()

    print("Welcome to the calculator! Type 'exit' to quit.")

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
        

        if user_input == "undo":
            if calc.undo():
                print("Last calculation undone.")
            else:
                print("Nothing to undo.")
            continue

        if user_input == "redo":
            if calc.redo():
                print("Calculation restored.")
            else:
                print("Nothing to redo.")
            continue

    
        if user_input == "clear":
            calc.clear_history()
            print("Calculation history cleared.")
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
