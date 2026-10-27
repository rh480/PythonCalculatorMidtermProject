"""Tests for the calculator operations and the operation factory."""

from decimal import Decimal

import pytest

from app.exceptions import ValidationError
from app.operations import (
    AbsDiff,
    Addition,
    Division,
    IntDivide,
    Modulus,
    Multiplication,
    Operation,
    OperationFactory,
    Percent,
    Power,
    Root,
    Subtraction,
)


def run(operation_class, a, b):
    """Run an operation on plain numbers.

    The numbers go through str() before Decimal() so that 1.5 stays exactly
    1.5 instead of picking up binary floating-point noise.
    """
    return operation_class().execute(Decimal(str(a)), Decimal(str(b)))


'''Operation base class tests'''


def test_operation_str_is_class_name():
    # Calculation finds an operation by its class name, so str() must return it.
    assert str(Addition()) == "Addition"
    assert str(AbsDiff()) == "AbsDiff"


'''Addition tests'''

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (4, 3, 7),  # Test case 1: Adding two positive integers. The expected result is 7.
        (-1, 1, 0),  # Test case 2: Adding a negative and a positive integer. The expected result is 0.
        (0, 0, 0),  # Test case 3: Adding two zeros. The expected result is 0.
        (-2, 5, 3),  # Test case 4: Adding a negative and a positive integer. The expected result is 3.
        (1.5, 2.5, 4.0),  # Test case 5: Adding two decimal numbers. The expected result is 4.0.
    ],
)
def test_addition(a, b, expected):
    assert run(Addition, a, b) == Decimal(str(expected))


'''Subtraction tests'''

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (4, 3, 1),  # Test case 1: Subtracting two positive integers. The expected result is 1.
        (-1, 1, -2),  # Test case 2: Subtracting a positive integer from a negative integer. The expected result is -2.
        (0, 0, 0),  # Test case 3: Subtracting two zeros. The expected result is 0.
        (-2, 5, -7),  # Test case 4: Subtracting a positive integer from a negative integer. The expected result is -7.
        (1.5, 2.5, -1.0),  # Test case 5: Subtracting two decimal numbers. The expected result is -1.0.
    ],
)
def test_subtraction(a, b, expected):
    assert run(Subtraction, a, b) == Decimal(str(expected))


'''Multiplication tests'''

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (4, 3, 12),  # Test case 1: Multiplying two positive integers. The expected result is 12.
        (-1, 1, -1),  # Test case 2: Multiplying a negative integer by a positive integer. The expected result is -1.
        (0, 0, 0),  # Test case 3: Multiplying two zeros. The expected result is 0.
        (-2, 5, -10),  # Test case 4: Multiplying a negative integer by a positive integer. The expected result is -10.
        (1.5, 2.5, 3.75),  # Test case 5: Multiplying two decimal numbers. The expected result is 3.75.
    ],
)
def test_multiplication(a, b, expected):
    assert run(Multiplication, a, b) == Decimal(str(expected))


'''Division tests'''

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (10, 2, 5),  # Test case 1: Dividing two positive integers. The expected result is 5.
        (-10, 2, -5),  # Test case 2: Dividing a negative integer by a positive integer. The expected result is -5.
        (10, -2, -5),  # Test case 3: Dividing a positive integer by a negative integer. The expected result is -5.
        (-10, -2, 5),  # Test case 4: Dividing two negative integers. The expected result is 5.
        (7, 2, 3.5),  # Test case 5: Dividing two integers that do not divide evenly. The expected result is 3.5.
    ],
)
def test_division(a, b, expected):
    assert run(Division, a, b) == Decimal(str(expected))


def test_division_by_zero():
    # Dividing by zero raises a ValidationError with the correct message.
    with pytest.raises(ValidationError, match="Division by zero is not allowed"):
        run(Division, 10, 0)


'''Power tests'''

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (4, 3, 64),  # Test case 1: Raising a positive integer to a positive power. The expected result is 64.
        (-1, 1, -1),  # Test case 2: Raising a negative integer to the power of one. The expected result is -1.
        (1, 0, 1),  # Test case 3: Raising one to the power of zero. The expected result is 1.
        (0, 0, 1),  # Test case 4: Raising zero to the power of zero. The expected result is 1.
        (1.5, 3, 3.375),  # Test case 5: Raising a decimal number to a positive power. The expected result is 3.375.
    ],
)
def test_power(a, b, expected):
    # Power goes through float internally, so compare approximately.
    assert float(run(Power, a, b)) == pytest.approx(expected)


@pytest.mark.parametrize("a, b", [(5, -1), (0, -1), (2, -2)])
def test_power_negative_exponent(a, b):
    # Negative exponents are not supported (this includes zero to a negative power).
    with pytest.raises(ValidationError, match="Negative exponents not supported"):
        run(Power, a, b)


'''Root tests'''

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (16, 4, 2),  # Test case 1: Taking the fourth root of a positive integer. The expected result is 2.
        (27, 3, 3),  # Test case 2: Taking the cube root of a positive integer. The expected result is 3.
        (0, 3, 0),  # Test case 3: Taking the cube root of zero. The expected result is 0.
        (16, -4, 0.5),  # Test case 4: A negative degree gives the reciprocal root. The expected result is 0.5.
        (0.25, 0.5, 0.0625),  # Test case 5: Taking the 0.5th root of a decimal number. The expected result is 0.0625.
    ],
)
def test_root(a, b, expected):
    assert float(run(Root, a, b)) == pytest.approx(expected)


def test_root_zero_degree():
    # A root of degree zero is undefined.
    with pytest.raises(ValidationError, match="Zero root is undefined"):
        run(Root, 16, 0)


@pytest.mark.parametrize("a, b", [(-16, 4), (-27, 3)])
def test_root_of_negative_number(a, b):
    # Roots of negative numbers are not supported (even odd roots such as the cube root of -27).
    with pytest.raises(ValidationError, match="Cannot calculate root of negative number"):
        run(Root, a, b)


def test_root_zero_with_negative_degree():
    # Zero cannot have a negative root degree (it would mean dividing by zero).
    with pytest.raises(ValidationError, match="Zero cannot have a negative root degree"):
        run(Root, 0, -1)


'''Modulus tests'''

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (10, 3, 1),  # Test case 1: Modulus of two positive integers. The expected result is 1.
        (-10, 3, -1),  # Test case 2: Negative dividend. Decimal remainders take the sign of the first number, so -1.
        (10, -3, 1),  # Test case 3: Negative divisor. The remainder keeps the sign of the first number, so 1.
        (-10, -3, -1),  # Test case 4: Two negative integers. The expected result is -1.
        (0, 3, 0),  # Test case 5: Modulus of zero and a positive integer. The expected result is 0.
        (7.5, 2, 1.5),  # Test case 6: Modulus of a decimal number and an integer. The expected result is 1.5.
        (10.5, 0.5, 0),  # Test case 7: Modulus of two decimal numbers that divide evenly. The expected result is 0.
    ],
)
def test_modulus(a, b, expected):
    assert run(Modulus, a, b) == Decimal(str(expected))


def test_modulus_zero_result_has_no_negative_sign():
    # Decimal would give -0 here; the operation returns a plain 0.
    assert str(run(Modulus, -6, 3)) == "0"


def test_modulus_by_zero():
    with pytest.raises(ValidationError, match="Modulus by zero is not allowed"):
        run(Modulus, 10, 0)


'''Integer Division tests'''

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (15, 5, 3),  # Test case 1: Two integers that divide evenly. The expected result is 3.
        (7, 2, 3),  # Test case 2: Two integers that do not divide evenly. 3.5 is truncated to 3.
        (15, -3, -5),  # Test case 3: A positive and a negative integer. The expected result is -5.
        (-7, 2, -3),  # Test case 4: -3.5 is truncated toward zero, giving -3 (not -4).
        (0, 5, 0),  # Test case 5: Zero divided by a positive integer. The expected result is 0.
        (7.9, 2, 3),  # Test case 6: A decimal dividend. 3.95 is truncated to 3.
    ],
)
def test_int_divide(a, b, expected):
    assert run(IntDivide, a, b) == Decimal(str(expected))


def test_int_divide_zero_result_has_no_negative_sign():
    # -1 // 2 truncates to -0 in Decimal; the operation returns a plain 0.
    assert str(run(IntDivide, -1, 2)) == "0"


def test_int_divide_by_zero():
    with pytest.raises(ValidationError, match="Integer division by zero is not allowed"):
        run(IntDivide, 10, 0)


'''Percent tests'''

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (25, 100, 25),  # Test case 1: 25 as a percentage of 100. The expected result is 25.
        (50, 200, 25),  # Test case 2: 50 as a percentage of 200. The expected result is 25.
        (15, 30, 50),  # Test case 3: 15 as a percentage of 30. The expected result is 50.
        (10, 0.5, 2000),  # Test case 4: 10 as a percentage of 0.5. The expected result is 2000.
        (0, 100, 0),  # Test case 5: Zero as a percentage of 100. The expected result is 0.
        (1, 8, 12.5),  # Test case 6: 1 as a percentage of 8. The expected result is 12.5.
    ],
)
def test_percent(a, b, expected):
    assert run(Percent, a, b) == Decimal(str(expected))


def test_percent_by_zero():
    with pytest.raises(
        ValidationError,
        match="Cannot calculate a percentage with zero as the second number",
    ):
        run(Percent, 10, 0)


'''Absolute Difference tests'''

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (10, 4, 6),  # Test case 1: Two positive integers. The expected result is 6.
        (4, 10, 6),  # Test case 2: The same integers in reverse order. The expected result is 6.
        (-5, -10, 5),  # Test case 3: Two negative integers. The expected result is 5.
        (-3, 2, 5),  # Test case 4: A negative and a positive integer. The expected result is 5.
        (0, 0, 0),  # Test case 5: Two zeros. The expected result is 0.
        (5, 5, 0),  # Test case 6: Two equal integers. The expected result is 0.
        (5.5, 2.2, 3.3),  # Test case 7: Two decimal numbers. The expected result is 3.3.
    ],
)
def test_absolute_difference(a, b, expected):
    assert run(AbsDiff, a, b) == Decimal(str(expected))


'''Operation factory tests'''

@pytest.mark.parametrize(
    "command, operation_class",
    [
        ("add", Addition),
        ("subtract", Subtraction),
        ("multiply", Multiplication),
        ("divide", Division),
        ("power", Power),
        ("root", Root),
        ("modulus", Modulus),
        ("int_divide", IntDivide),
        ("percent", Percent),
        ("abs_diff", AbsDiff),
    ],
)
def test_factory_creates_each_operation(command, operation_class):
    # Every REPL command name maps to the right class, in any letter case.
    assert isinstance(OperationFactory.create_operation(command), operation_class)
    assert isinstance(OperationFactory.create_operation(command.upper()), operation_class)


def test_factory_unknown_operation():
    with pytest.raises(ValueError, match="Unknown operation: invalid_op"):
        OperationFactory.create_operation("invalid_op")


def test_factory_register_valid_operation(monkeypatch):
    # Work on a copy of the registry so this test does not leak into others.
    monkeypatch.setattr(OperationFactory, "_operations", dict(OperationFactory._operations))

    class NewOperation(Operation):
        def execute(self, a, b):
            return a

    OperationFactory.register_operation("New_Op", NewOperation)
    assert isinstance(OperationFactory.create_operation("new_op"), NewOperation)


def test_factory_register_invalid_operation(monkeypatch):
    monkeypatch.setattr(OperationFactory, "_operations", dict(OperationFactory._operations))

    class NotAnOperation:
        pass

    with pytest.raises(TypeError, match="Operation class must inherit"):
        OperationFactory.register_operation("invalid", NotAnOperation)