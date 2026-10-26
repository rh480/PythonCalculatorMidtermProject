
"""Command-line interface for the basic calculator."""

from unittest import result

from app import history
from app.calculation import Calculation

from app.operations import (
    addition,
    subtraction,
    multiplication,
    division,
    power,
    root,
    modulus,
    int_divide,
    percent,
    absolute_difference,
)


def calculator():
    """Run the basic calculator REPL."""

    history = []  # Stores successful calculations during the current session.

    operations = {
        "add": addition,
        "subtract": subtraction,
        "multiply": multiplication,
        "divide": division,
        "power": power,
        "root": root,
        "modulus": modulus,
        "int_divide": int_divide,
        "percent": percent,
        "absolute_difference": absolute_difference,
    }

    print("Welcome to the calculator! Type 'exit' to quit.")

    while True:
        user_input = input(
            "Enter an operation and two numbers: "
        ).strip().lower()

        #exit command to terminate the calculator
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        parts = user_input.split()

        #History command to display previous calculations
        if user_input.lower() == "history":
            if not history:
                print("No calculation history yet.")
            else:
                for index, entry in enumerate(history, start=1):
                    print(f"{index}. {entry}")
            continue

        # Validate that the user input has exactly three parts: operation, first number, and second number.
        if len(parts) != 3:
            print("Invalid input. Example: add 5 3")
            continue

        operation_name, first, second = parts

        # Check if the operation is supported.
        if operation_name not in operations:
            print(f"Unknown operation: {operation_name}. Example: add 5 3")
            continue

        # Validate that both inputs are numbers.
        try:
            a = float(first)
            b = float(second)
        except ValueError:
            print("Cannot use letters. Please enter numbers only. Example: add 5 3")
            continue

        # Perform the calculation.
        try:
            a = float(first)
            b = float(second)
            result = operations[operation_name](a, b)
        except ValueError as error:
            print(f"Error: {error}")
            continue

        print(f"Result: {result}") #successful calculation output

        #store successful calculation in history
        history.append(
            Calculation(
                operation=operation_name,
                operand1=a,
                operand2=b,
                result=result,
             )
        )
        


def main():
    """Start the calculator application."""
    calculator()


if __name__ == "__main__":
    main()
