"""Arithmetic operations and the factory that creates them."""

from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Dict, Type

from app.exceptions import OperationError


########################
# Operation Classes    #
########################

class Operation(ABC):
    """
    Base class for all calculator operations.

    Each operation must implement the execute method.
    Individual operations can also validate their inputs.
    """

    description = ""

    @abstractmethod
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Perform a calculation using two numbers.

        Args:
            a: The first number.
            b: The second number.

        Returns:
            Decimal: The result of the calculation.
        """
        pass

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """
        Check the inputs before performing a calculation.

        Individual operations can override this method
        to check for invalid inputs.
        """
        pass

    @staticmethod
    def _require_nonzero(value: Decimal, message: str) -> None:
        """Raise an error if a value is zero."""
        if value == 0:
            raise OperationError(message)

    def __str__(self) -> str:
        """Return the name of the operation class."""
        return self.__class__.__name__


class Addition(Operation):
    """Add two numbers."""

    description = "Add two numbers"

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """Return the sum of two numbers."""
        self.validate_operands(a, b)
        return a + b


class Subtraction(Operation):
    """Subtract the second number from the first."""

    description = "Subtract the second number from the first"

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """Return the difference between two numbers."""
        self.validate_operands(a, b)
        return a - b


class Multiplication(Operation):
    """Multiply two numbers."""

    description = "Multiply two numbers"

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """Return the product of two numbers."""
        self.validate_operands(a, b)
        return a * b


class Division(Operation):
    """Divide the first number by the second."""

    description = "Divide the first number by the second"

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """Check that the divisor is not zero."""
        self._require_nonzero(
            b, "Division by zero is not allowed."
        )

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """Return the result of dividing the first number by the second."""
        self.validate_operands(a, b)
        return a / b


class Power(Operation):
    """Raise the first number to the power of the second."""

    description = "Raise the first number to the power of the second"

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """Check that the power calculation is valid."""
        if a == 0 and b <= 0:
            raise OperationError(
                "Zero cannot be raised to zero or a negative power."
            )

        if a < 0 and b != b.to_integral_value():
            raise OperationError(
                "Cannot raise a negative number to a fractional power."
            )

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """Return the first number raised to the second number's power."""
        self.validate_operands(a, b)
        return a ** b


class Root(Operation):
    """Calculate the b-th root of the first number."""

    description = "Take the b-th root of a (root a b)"

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """Check that the root calculation is valid."""
        self._require_nonzero(
            b, "The degree of the root cannot be zero."
        )

        if a == 0 and b < 0:
            raise OperationError(
                "Zero cannot have a negative root degree."
            )

        if a < 0:
            if b != b.to_integral_value() or b % 2 == 0:
                raise OperationError(
                    "Cannot take an even or non-integer root "
                    "of a negative number."
                )

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """Return the b-th root of the first number."""
        self.validate_operands(a, b)

        if a < 0:
            return -((-a) ** (Decimal(1) / b))

        return a ** (Decimal(1) / b)


class Modulus(Operation):
    """Calculate the remainder after division."""

    description = "Remainder of dividing the first number by the second"

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """Check that the divisor is not zero."""
        self._require_nonzero(
            b, "Cannot calculate modulus with zero."
        )

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """Return the remainder after dividing the first number by the second."""
        self.validate_operands(a, b)
        return a % b


class IntegerDivision(Operation):
    """Divide two numbers and discard the fractional part."""

    description = "Divide and discard the fractional part"

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """Check that the divisor is not zero."""
        self._require_nonzero(
            b, "Integer division by zero is not allowed."
        )

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """Return the result of integer division."""
        self.validate_operands(a, b)
        return a // b


class Percentage(Operation):
    """Calculate what percentage the first number is of the second."""

    description = "What percent a is of b: (a / b) * 100"

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """Check that the second number is not zero."""
        self._require_nonzero(
            b,
            "Cannot calculate a percentage with zero as the second number."
        )

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """Return the percentage of the first number compared to the second."""
        self.validate_operands(a, b)
        return (a / b) * 100


class AbsoluteDifference(Operation):
    """Calculate the absolute difference between two numbers."""

    description = "Absolute difference between two numbers"

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """Return the non-negative difference between two numbers."""
        self.validate_operands(a, b)
        return abs(a - b)


########################
# Operation Factory    #
########################

class OperationFactory:
    """
    Create operation objects using command names.

    The factory matches a command to its operation class
    and creates an instance of that class.
    """

    # Match each command name to its operation class.
    _operations: Dict[str, Type[Operation]] = {
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
    }

    @classmethod
    def create_operation(cls, name: str) -> Operation:
        """
        Create an operation based on its command name.

        Args:
            name: The name of the requested operation.

        Returns:
            Operation: An instance of the requested operation.

        Raises:
            OperationError: If the operation name is unknown.
        """
        operation_class = cls._operations.get(name.lower())

        if operation_class is None:
            raise OperationError(f"Unknown operation: {name}")

        return operation_class()

    @classmethod
    def available_operations(cls) -> Dict[str, str]:
        """Return the command names and descriptions of available operations."""
        return {
            name: operation.description
            for name, operation in cls._operations.items()
        }