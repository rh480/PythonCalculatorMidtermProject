"""Tests for the Calculation model."""

import logging
from datetime import datetime
from decimal import Decimal

import pytest

from app.calculation import Calculation
from app.exceptions import OperationError
from app.operations import OperationFactory


# --- Results ---------------------------------------------------------------
# Calculation works out its own result from the operation's class name.
@pytest.mark.parametrize(
    "operation, operand1, operand2, expected",
    [
        ("Addition", "2", "3", "5"),
        ("Subtraction", "5", "3", "2"),
        ("Multiplication", "4", "2", "8"),
        ("Division", "8", "2", "4"),
        ("Power", "2", "3", "8"),
        ("Root", "16", "2", "4"),
        ("Modulus", "10", "3", "1"),
        ("IntDivide", "7", "2", "3"),
        ("Percent", "50", "200", "25"),
        ("AbsDiff", "3", "10", "7"),
    ],
)
def test_calculation_operations(operation, operand1, operand2, expected):
    calculation = Calculation(operation, Decimal(operand1), Decimal(operand2))
    assert calculation.result == Decimal(expected)


def test_modulus_and_int_divide_zero_results_have_no_negative_sign():
    # Decimal would produce -0 here; Calculation must show a plain 0.
    assert str(Calculation("Modulus", Decimal("-6"), Decimal("3")).result) == "0"
    assert str(Calculation("IntDivide", Decimal("-1"), Decimal("2")).result) == "0"


@pytest.mark.parametrize("name", sorted(OperationFactory._operations))
def test_every_factory_operation_works_in_calculation(name):
    """Each operation registered in the factory must also work inside Calculation.

    Calculation keeps its own table of operations, so this catches the mistake of
    adding an operation to the factory but forgetting the table.
    """
    operation = OperationFactory.create_operation(name)
    calculation = Calculation(str(operation), Decimal("8"), Decimal("2"))
    assert calculation.result == operation.execute(Decimal("8"), Decimal("2"))


# --- Errors ----------------------------------------------------------------
def test_division_by_zero():
    with pytest.raises(OperationError, match="Division by zero is not allowed"):
        Calculation("Division", Decimal("8"), Decimal("0"))


@pytest.mark.parametrize(
    "operation, message",
    [
        ("Modulus", "Modulus by zero is not allowed"),
        ("IntDivide", "Integer division by zero is not allowed"),
        ("Percent", "Cannot calculate a percentage with zero as the second number"),
    ],
)
def test_zero_divisor_raises_operation_error(operation, message):
    with pytest.raises(OperationError, match=message):
        Calculation(operation, Decimal("5"), Decimal("0"))


def test_negative_power():
    with pytest.raises(OperationError, match="Negative exponents are not supported"):
        Calculation("Power", Decimal("2"), Decimal("-3"))


def test_root_of_negative_number():
    with pytest.raises(OperationError, match="Cannot calculate root of negative number"):
        Calculation("Root", Decimal("-16"), Decimal("2"))


def test_root_with_zero_degree():
    with pytest.raises(OperationError, match="Zero root is undefined"):
        Calculation("Root", Decimal("16"), Decimal("0"))


def test_zero_with_negative_root_degree():
    # pow(0, -1) fails inside Python; Calculation wraps it in an OperationError.
    with pytest.raises(OperationError, match="Calculation failed"):
        Calculation("Root", Decimal("0"), Decimal("-1"))


def test_unknown_operation():
    with pytest.raises(OperationError, match="Unknown operation"):
        Calculation("Unknown", Decimal("5"), Decimal("3"))


def test_calculation_error():
    # Build a Calculation by hand so the arithmetic itself fails, to prove that
    # ArithmeticError is turned into an OperationError.
    calculation = Calculation.__new__(Calculation)
    calculation.operation = "Addition"

    class ErrorValue:
        def __add__(self, other):
            raise ArithmeticError("Test arithmetic error")

    calculation.operand1 = ErrorValue()
    calculation.operand2 = Decimal("3")

    with pytest.raises(OperationError, match="Calculation failed: Test arithmetic error"):
        calculation.calculate()


# --- Saving and loading ----------------------------------------------------
def test_calculation_to_dict():
    timestamp = datetime(2026, 1, 1, 12, 0, 0)
    calculation = Calculation(
        operation="Addition",
        operand1=Decimal("5.0"),
        operand2=Decimal("3.0"),
        timestamp=timestamp,
    )

    data = calculation.to_dict()

    assert data["operation"] == "Addition"
    assert data["operand1"] == "5.0"
    assert data["operand2"] == "3.0"
    assert data["result"] == "8.0"
    assert data["timestamp"] == timestamp.isoformat()


def test_calculation_from_dict():
    data = {
        "operation": "Addition",
        "operand1": "5.0",
        "operand2": "3.0",
        "result": "8.0",
        "timestamp": "2026-01-01T12:00:00",
    }

    calculation = Calculation.from_dict(data)

    assert calculation.operation == "Addition"
    assert calculation.operand1 == Decimal("5.0")
    assert calculation.operand2 == Decimal("3.0")
    assert calculation.result == Decimal("8.0")
    assert calculation.timestamp == datetime(2026, 1, 1, 12, 0, 0)


def test_to_dict_and_from_dict_round_trip():
    original = Calculation("Percent", Decimal("1"), Decimal("8"))
    assert Calculation.from_dict(original.to_dict()) == original


def test_from_dict_with_invalid_data():
    data = {
        "operation": "Addition",
        "operand1": "abc",  # not a number
        "operand2": "3",
        "result": "5",
        "timestamp": "2026-01-01T12:00:00",
    }
    with pytest.raises(OperationError, match="Invalid calculation data"):
        Calculation.from_dict(data)


def test_from_dict_with_missing_field():
    with pytest.raises(OperationError, match="Invalid calculation data"):
        Calculation.from_dict({"operation": "Addition"})


def test_from_dict_result_mismatch_logs_warning(caplog):
    # If the saved result differs from the recomputed one, a warning is logged
    # (it signals a damaged history file) but loading still works.
    data = {
        "operation": "Addition",
        "operand1": "2",
        "operand2": "3",
        "result": "10",  # wrong on purpose
        "timestamp": datetime.now().isoformat(),
    }

    with caplog.at_level(logging.WARNING):
        calculation = Calculation.from_dict(data)

    assert calculation.result == Decimal("5")
    assert "Loaded calculation result 10 differs from computed result 5" in caplog.text


# --- Display and comparison ------------------------------------------------
def test_str():
    calculation = Calculation("Addition", Decimal("2"), Decimal("3"))
    assert str(calculation) == "Addition(2, 3) = 5"


def test_repr():
    result = repr(Calculation("Addition", Decimal("2"), Decimal("3")))
    assert "Calculation(operation='Addition'" in result
    assert "operand1=2" in result
    assert "operand2=3" in result
    assert "result=5" in result


def test_format_result():
    calculation = Calculation("Division", Decimal("1"), Decimal("3"))
    assert calculation.format_result(precision=2) == "0.33"
    assert calculation.format_result(precision=10) == "0.3333333333"


def test_equality():
    first = Calculation("Addition", Decimal("2"), Decimal("3"))
    same = Calculation("Addition", Decimal("2"), Decimal("3"))
    different = Calculation("Subtraction", Decimal("5"), Decimal("3"))
    assert first == same
    assert first != different


def test_equality_with_non_calculation():
    assert Calculation("Addition", Decimal("2"), Decimal("3")) != "not a calculation"