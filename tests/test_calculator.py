
"""Tests for the Calculator class and command-line interface."""

from decimal import Decimal

import pytest

from app.calculator import Calculator, calculator
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


# Fixture to initialize Calculator for testing.
@pytest.fixture
def calc():
    """Return a fresh Calculator instance."""
    return Calculator()


# Test Calculator Initialization

def test_calculator_initialization(calc):
    assert calc.history == []
    assert calc.operation_strategy is None
    assert len(calc.operations) == 11


# Test Setting Operations

def test_set_operation(calc):
    operation = Addition()
    calc.set_operation(operation)

    assert calc.operation_strategy == operation


# Test Performing Operations

@pytest.mark.parametrize(
    "operation, a, b, expected",
    [
        (Addition(), "2", "3", "5"),
        (Subtraction(), "2", "3", "-1"),
        (Multiplication(), "2", "3", "6"),
        (Division(), "6", "2", "3"),
        (Power(), "2", "3", "8"),
        (Root(), "27", "3", "3"),
        (Modulus(), "10", "3", "1"),
        (IntegerDivision(), "7", "2", "3"),
        (Percentage(), "1", "8", "12.5"),
        (AbsoluteDifference(), "4", "10", "6"),
    ],
)
def test_perform_operation(calc, operation, a, b, expected):
    calc.set_operation(operation)

    result = calc.perform_operation(Decimal(a), Decimal(b))

    assert result == Decimal(expected)
    assert len(calc.history) == 1


def test_perform_operation_without_setting_operation(calc):
    with pytest.raises(OperationError, match="No operation set"):
        calc.perform_operation(Decimal("2"), Decimal("3"))


def test_perform_operation_records_calculation(calc):
    calc.set_operation(Addition())
    calc.perform_operation(Decimal("2"), Decimal("3"))

    assert calc.history[0].operation == "Addition"
    assert calc.history[0].operand1 == Decimal("2")
    assert calc.history[0].operand2 == Decimal("3")
    assert calc.history[0].result == Decimal("5")


# Test History Management

def test_show_history(calc):
    calc.set_operation(Addition())
    calc.perform_operation(Decimal("2"), Decimal("3"))

    history = calc.show_history()

    assert history == ["Addition(2, 3) = 5"]


def test_show_empty_history(calc):
    assert calc.show_history() == []


def test_clear_history(calc):
    calc.set_operation(Addition())
    calc.perform_operation(Decimal("2"), Decimal("3"))

    calc.clear_history()

    assert calc.history == []


# Test Command-Line Interface

def run_calculator(monkeypatch, capsys, inputs):
    """Run the calculator with simulated user input."""
    user_inputs = iter(inputs)
    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(user_inputs),
    )

    calculator()
    return capsys.readouterr().out


@pytest.mark.parametrize(
    "command, expected",
    [
        ("add 2 3", "Result: 5"),
        ("subtract 2 3", "Result: -1"),
        ("multiply 2 3", "Result: 6"),
        ("divide 6 2", "Result: 3"),
        ("power 2 3", "Result: 8"),
        ("root 27 3", "Result: 3"),
        ("modulus 10 3", "Result: 1"),
        ("int_divide 7 2", "Result: 3"),
        ("percent 1 8", "Result: 12.5"),
        ("absolute_difference 4 10", "Result: 6"),
    ],
)
def test_calculator_commands(monkeypatch, capsys, command, expected):
    output = run_calculator(
        monkeypatch, capsys, [command, "exit"]
    )

    assert expected in output


def test_invalid_operation(monkeypatch, capsys):
    output = run_calculator(
        monkeypatch, capsys, ["unknown 2 3", "exit"]
    )

    assert "Unknown operation" in output


def test_invalid_input(monkeypatch, capsys):
    output = run_calculator(
        monkeypatch, capsys, ["add 2", "exit"]
    )

    assert "Invalid input" in output


def test_non_numeric_input(monkeypatch, capsys):
    output = run_calculator(
        monkeypatch, capsys, ["add two three", "exit"]
    )

    assert "Invalid numbers" in output


def test_division_by_zero(monkeypatch, capsys):
    output = run_calculator(
        monkeypatch, capsys, ["divide 5 0", "exit"]
    )

    assert "Error:" in output
    assert "zero" in output.lower()


def test_exit_command(monkeypatch, capsys):
    output = run_calculator(
        monkeypatch, capsys, ["exit"]
    )

    assert "Goodbye!" in output


def test_history_command(monkeypatch, capsys):
    output = run_calculator(
        monkeypatch, capsys, ["add 2 3", "history", "exit"]
    )

    assert "Result: 5" in output
    assert "Addition(2, 3) = 5" in output


def test_empty_history_command(monkeypatch, capsys):
    output = run_calculator(
        monkeypatch, capsys, ["history", "exit"]
    )

    assert "No calculation history yet." in output


def test_undo_removes_last_calculation():
    calc = Calculator()
    calc.set_operation(calc.operations["add"]())

    calc.perform_operation(Decimal("2"), Decimal("3"))
    calc.undo()

    assert calc.history == []


def test_redo_restores_undone_calculation():
    calc = Calculator()
    calc.set_operation(calc.operations["add"]())

    calc.perform_operation(Decimal("2"), Decimal("3"))
    calc.undo()
    calc.redo()

    assert len(calc.history) == 1
    assert calc.history[0].result == Decimal("5")


def test_undo_returns_false_when_history_is_empty():
    calc = Calculator()

    assert calc.undo() is False


def test_redo_returns_false_when_nothing_was_undone():
    calc = Calculator()

    assert calc.redo() is False


def test_undo_restores_history_after_clear():
    calc = Calculator()
    calc.set_operation(calc.operations["add"]())

    calc.perform_operation(Decimal("2"), Decimal("3"))
    calc.clear_history()

    assert calc.history == []

    assert calc.undo() is True
    assert len(calc.history) == 1
    assert calc.history[0].result == Decimal("5")