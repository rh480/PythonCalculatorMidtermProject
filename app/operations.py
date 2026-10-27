"""Arithmetic operations for the calculator.

Each operation is a class with an execute(a, b) method that takes two Decimal
numbers and returns a Decimal. OperationFactory creates operation objects from
command names such as 'add' or 'int_divide'.
"""

from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Dict

from app.exceptions import ValidationError


def without_negative_zero(value: Decimal) -> Decimal:
    """Return 0 instead of -0.

    Decimal keeps the sign on a zero result (for example -6 % 3 gives -0),
    which would be displayed as "-0".
    """
    return Decimal(0) if value == 0 else value


class Operation(ABC):
    """
    Abstract base class for calculator operations.

    Every operation takes exactly two numbers. Subclasses must implement
    execute() and may override validate_operands() to reject bad input.
    """

    @abstractmethod
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """Perform the operation on a and b and return the result."""
        pass  # pragma: no cover

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """Raise ValidationError if the operands are not allowed (default: accept all)."""
        pass

    def __str__(self) -> str:
        """Return the class name, which Calculation uses to find the operation."""
        return self.__class__.__name__


class DivisorOperation(Operation):
    """Base for operations whose second operand cannot be zero.

    Division, Modulus, IntDivide and Percent all share this zero check, so it
    lives here once. Subclasses only set their own error message.
    """

    zero_message = "Second operand cannot be zero"

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError(self.zero_message)


class Addition(Operation):
    """Add two numbers."""

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b)
        return a + b


class Subtraction(Operation):
    """Subtract the second number from the first."""

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b)
        return a - b


class Multiplication(Operation):
    """Multiply two numbers."""

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b)
        return a * b


class Division(DivisorOperation):
    """Divide the first number by the second."""

    zero_message = "Division by zero is not allowed"

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b)
        return a / b


class Power(Operation):
    """Raise the first number to the power of the second."""

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        super().validate_operands(a, b)
        if b < 0:  # negative exponents are not supported
            raise ValidationError("Negative exponents not supported")

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b)
        return Decimal(pow(float(a), float(b)))


class Root(Operation):
    """Calculate the b-th root of a."""

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        super().validate_operands(a, b)
        if a < 0:  # roots of negative numbers are not supported
            raise ValidationError("Cannot calculate root of negative number")
        if b == 0:  # a root of degree zero is undefined
            raise ValidationError("Zero root is undefined")
        if a == 0 and b < 0:  # would mean dividing by zero
            raise ValidationError("Zero cannot have a negative root degree")

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b)
        return Decimal(pow(float(a), 1 / float(b)))


class Modulus(DivisorOperation):
    """Remainder after dividing a by b (takes the sign of a)."""

    zero_message = "Modulus by zero is not allowed"

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b)
        return without_negative_zero(a % b)


class IntDivide(DivisorOperation):
    """Quotient of a divided by b with the fractional part discarded."""

    zero_message = "Integer division by zero is not allowed"

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b)
        return without_negative_zero(a // b)  # // truncates toward zero


class Percent(DivisorOperation):
    """Percentage of a with respect to b: (a / b) * 100."""

    zero_message = "Cannot calculate a percentage with zero as the second number"

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b)
        return (a / b) * 100


class AbsDiff(Operation):
    """Absolute (non-negative) difference between a and b."""

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b)
        return abs(a - b)


class OperationFactory:
    """
    Factory that creates operation instances from command names.

    Keeping creation in one place means the REPL and Calculator never need to
    know which class handles which command.
    """

    # Maps each command name to the class that implements it
    _operations: Dict[str, type] = {
        'add': Addition,
        'subtract': Subtraction,
        'multiply': Multiplication,
        'divide': Division,
        'power': Power,
        'root': Root,
        'modulus': Modulus,
        'int_divide': IntDivide,
        'percent': Percent,
        'abs_diff': AbsDiff,
    }

    @classmethod
    def register_operation(cls, name: str, operation_class: type) -> None:
        """Register a new operation class under a command name.

        Raises:
            TypeError: If operation_class does not inherit from Operation.
        """
        if not issubclass(operation_class, Operation):
            raise TypeError("Operation class must inherit from Operation")
        cls._operations[name.lower()] = operation_class

    @classmethod
    def create_operation(cls, operation_type: str) -> Operation:
        """Create an operation instance from its command name (case-insensitive).

        Raises:
            ValueError: If the operation type is unknown.
        """
        operation_class = cls._operations.get(operation_type.lower())
        if not operation_class:
            raise ValueError(f"Unknown operation: {operation_type}")
        return operation_class()