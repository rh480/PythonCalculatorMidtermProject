# app/operations.py
"""Arithmetic operations and the factory that creates them."""

from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Dict, Type

from app.exceptions import OperationError


def without_negative_zero(value: Decimal) -> Decimal:
    """Return Decimal(0) instead of -0 so results print cleanly."""
    return Decimal(0) if value == 0 else value


class Operation(ABC):
    """Base class: every operation takes exactly two numbers."""

    description = ""  # shown in the help menu

    @abstractmethod
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """Apply the operation to a and b and return the result."""

    @staticmethod
    def _require_nonzero(value: Decimal, message: str) -> None:
        """Shared guard so zero checks are not repeated in each class."""
        if value == 0:
            raise OperationError(message)


class Addition(Operation):
    description = "Add two numbers"

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        return a + b


class Subtraction(Operation):
    description = "Subtract the second number from the first"

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        return a - b


class Multiplication(Operation):
    description = "Multiply two numbers"

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        return a * b


class Division(Operation):
    description = "Divide the first number by the second"

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self._require_nonzero(b, "Division by zero is not allowed.")
        return a / b





def power(a: float, b: float) -> float:
    #Returns the result of raising 'a' to the power of 'b'. The function takes two float inputs, 'a' and 'b', and returns 'a' raised to the power of 'b' as a float.
    if a == 0 and b < 0: # Checks if 'a' is zero and 'b' is negative. If both conditions are true, it raises a ValueError with the message "Zero cannot be raised to a negative power."
        raise ValueError("Zero cannot be raised to a negative power.")
    return a ** b


def root(a: float, b: float) -> float:
    #Calculate the b-th root of a.
    if b == 0: # Checks if 'b' is zero. If it is, we raise an error and stop the function.
        raise ValueError("The degree of the root cannot be zero.")
    if a == 0 and b < 0: # Checks if 'a' is zero and 'b' is negative. If both conditions are true, it raises a ValueError with the message "Zero cannot have a negative root degree."
        raise ValueError("Zero cannot have a negative root degree.")
    if a < 0: # Checks if 'a' is negative. If it is, we check if 'b' is an even integer or not. If 'b' is an even integer or a non-integer, we raise a ValueError with the message "Cannot take an even or non-integer root of a negative number."
        if not float(b).is_integer() or int(b) % 2 == 0:
            raise ValueError(
                "Cannot take an even or non-integer root of a negative number."
            )
        return -((-a) ** (1 / b))

    return a ** (1 / b)


def modulus(a: float, b: float) -> float:
    #Return the remainder after dividing a by b.
    if b == 0: # Checks if 'b' is zero. If it is, we raise an error and stop the function.
        raise ValueError("Cannot calculate modulus with zero.")
    result = a % b
    return 0.0 if result == 0 else result


def int_divide(a: float, b: float) -> float:
    #Returns the integer quotient of two numbers. The function takes two float inputs, 'a' and 'b', and returns the quotient with the fractional part discarded as a float.
    if b == 0:  # Checks if 'b' is zero. If it is, we raise an error and stop the function.
        raise ValueError("Integer division by zero is not allowed.")  # This sends an error message when someone tries to perform integer division by zero.
    return float(int(a / b))  # Divides 'a' by 'b', discards the fractional part, converts the result to a float, and returns it.


def percent(a: float, b: float) -> float:
    #Returns the percentage of 'a' with respect to 'b'. The function takes two float inputs, 'a' and 'b', and returns (a / b) * 100 as a float.
    if b == 0:  # Checks if 'b' is zero. If it is, we raise an error and stop the function.
        raise ValueError("Cannot calculate a percentage with zero as the second number.")  # This sends an error message when someone tries to calculate a percentage with zero as the second number.
    return (a / b) * 100  # Divides 'a' by 'b', multiplies the result by 100, and returns the percentage.

def absolute_difference(a: float, b: float) -> float:
    #Returns the absolute difference between two numbers. The function takes two float inputs, 'a' and 'b', and returns the non-negative difference between them as a float.
    return abs(a - b)  # Subtracts 'b' from 'a', takes the absolute value, and returns the result.