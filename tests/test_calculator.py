
"""Tests for the Calculator class and command-line interface."""

from decimal import Decimal

import pytest
import pandas as pd

from app.calculator_config import CalculatorConfig
from app.exceptions import PersistenceError, ValidationError
from app.history import LoggingObserver

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
        ("abs_diff 4 10", "Result: 6")
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

    assert "Invalid number" in output


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
    calc.set_operation(Addition())

    calc.perform_operation(Decimal("2"), Decimal("3"))
    calc.undo()

    assert calc.history == []


def test_redo_restores_undone_calculation():
    calc = Calculator()
    calc.set_operation(Addition())

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
    calc.set_operation(Addition())

    calc.perform_operation(Decimal("2"), Decimal("3"))
    calc.clear_history()

    assert calc.history == []

    assert calc.undo() is True
    assert len(calc.history) == 1
    assert calc.history[0].result == Decimal("5")



# Tests for CSV persistence

@pytest.fixture
def temporary_calc(tmp_path):
    """Create a calculator that uses temporary files."""
    config = CalculatorConfig(base_dir=tmp_path)
    return Calculator(config=config)


def test_save_and_load_history(temporary_calc, tmp_path):
    temporary_calc.set_operation(Addition())
    temporary_calc.perform_operation(Decimal("2"), Decimal("3"))

    file_path = tmp_path / "test_history.csv"
    temporary_calc.save_history(file_path)

    # Load the saved history into a separate calculator.
    config = CalculatorConfig(base_dir=tmp_path / "other")
    restored_calc = Calculator(config=config)
    restored_calc.load_history(file_path)

    assert len(restored_calc.history) == 1
    assert restored_calc.history[0].result == Decimal("5")


def test_save_empty_history(temporary_calc, tmp_path):
    file_path = tmp_path / "empty_history.csv"

    temporary_calc.save_history(file_path)

    dataframe = pd.read_csv(file_path)

    assert dataframe.empty
    assert "operation" in dataframe.columns
    assert "timestamp" in dataframe.columns


def test_load_missing_history_file(temporary_calc, tmp_path):
    file_path = tmp_path / "missing.csv"

    temporary_calc.load_history(file_path)

    assert temporary_calc.history == []


def test_load_invalid_history_file(temporary_calc, tmp_path):
    file_path = tmp_path / "invalid.csv"
    file_path.write_text("wrong_column\nvalue\n", encoding="utf-8")

    with pytest.raises(PersistenceError):
        temporary_calc.load_history(file_path)


def test_get_history_dataframe(temporary_calc):
    temporary_calc.set_operation(Addition())
    temporary_calc.perform_operation(Decimal("2"), Decimal("3"))

    dataframe = temporary_calc.get_history_dataframe()

    assert len(dataframe) == 1
    assert dataframe.iloc[0]["operation"] == "Addition"
    assert Decimal(dataframe.iloc[0]["result"]) == Decimal("5")


# Tests for undo and redo behavior

def test_new_calculation_clears_redo_stack(temporary_calc):
    temporary_calc.set_operation(Addition())

    temporary_calc.perform_operation(Decimal("2"), Decimal("3"))
    temporary_calc.undo()

    temporary_calc.perform_operation(Decimal("4"), Decimal("5"))

    assert temporary_calc.redo() is False


def test_clear_empty_history_does_not_create_undo_state(temporary_calc):
    temporary_calc.clear_history()

    assert temporary_calc.undo() is False


# Tests for additional CLI commands

def test_help_command(monkeypatch, capsys):
    output = run_calculator(
        monkeypatch, capsys, ["help", "exit"]
    )

    assert "Operations:" in output
    assert "save" in output
    assert "load" in output

#  test clear command and undo/redo commands
def test_clear_command(monkeypatch, capsys):
    output = run_calculator(
        monkeypatch,
        capsys,
        ["add 2 3", "clear", "history", "exit"],
    )

    assert "Calculation history cleared." in output
    assert "No calculation history yet." in output


def test_undo_command(monkeypatch, capsys):
    output = run_calculator(
        monkeypatch, capsys, ["add 2 3", "undo", "history", "exit"]
    )

    assert "Last action undone." in output
    assert "No calculation history yet." in output


def test_redo_command(monkeypatch, capsys):
    output = run_calculator(
        monkeypatch, capsys,
        ["add 2 3", "undo", "redo", "history", "exit"],
    )

    assert "Last action restored." in output
    assert "Addition(2, 3) = 5" in output



# Test save command and error handling

def test_save_command(monkeypatch, capsys, tmp_path):
    config = CalculatorConfig(base_dir=tmp_path)
    calc = Calculator(config=config)
    calc.set_operation(Addition())
    calc.perform_operation(Decimal("2"), Decimal("3"))

    monkeypatch.setattr("app.calculator.Calculator", lambda: calc)

    output = run_calculator(monkeypatch, capsys, ["save", "exit"])

    assert "History saved to" in output
    assert calc.config.history_file.exists()


def test_save_command_with_empty_history(monkeypatch, capsys, tmp_path):
    config = CalculatorConfig(base_dir=tmp_path)
    calc = Calculator(config=config)

    monkeypatch.setattr("app.calculator.Calculator", lambda: calc)

    output = run_calculator(monkeypatch, capsys, ["save", "exit"])

    assert "History saved to" in output
    assert calc.config.history_file.exists()


def test_save_command_handles_persistence_error(
    monkeypatch, capsys, tmp_path
):
    config = CalculatorConfig(base_dir=tmp_path)
    calc = Calculator(config=config)

    def fail_save(*args, **kwargs):
        raise PersistenceError("Test save failure")

    monkeypatch.setattr(calc, "save_history", fail_save)
    monkeypatch.setattr("app.calculator.Calculator", lambda: calc)

    output = run_calculator(monkeypatch, capsys, ["save", "exit"])

    assert "Save failed: Test save failure" in output



# Tests for load command and error handling

def test_load_command(monkeypatch, capsys, tmp_path):
    """Test loading saved history through the CLI."""
    config = CalculatorConfig(base_dir=tmp_path)
    calc = Calculator(config=config)

    # Create and save a calculation.
    calc.set_operation(Addition())
    calc.perform_operation(Decimal("2"), Decimal("3"))
    calc.save_history()

    # Clear the in-memory history before loading.
    calc.history = []
    assert calc.history == []

    monkeypatch.setattr("app.calculator.Calculator", lambda: calc)

    output = run_calculator(monkeypatch, capsys, ["load", "exit"])

    assert "History loaded" in output
    assert len(calc.history) == 1
    assert calc.history[0].result == Decimal("5")


def test_load_command_with_missing_file(monkeypatch, capsys, tmp_path):
    """Test the CLI message when no saved history file exists."""
    config = CalculatorConfig(base_dir=tmp_path)
    calc = Calculator(config=config)

    assert not calc.config.history_file.exists()

    monkeypatch.setattr("app.calculator.Calculator", lambda: calc)

    output = run_calculator(monkeypatch, capsys, ["load", "exit"])

    assert "No saved history file found." in output


def test_load_command_handles_persistence_error(
    monkeypatch, capsys, tmp_path
):
    """Test that the CLI handles history-loading errors."""
    config = CalculatorConfig(base_dir=tmp_path)
    calc = Calculator(config=config)

    # Create a file so the CLI proceeds to load_history().
    config.history_file.parent.mkdir(parents=True, exist_ok=True)
    config.history_file.write_text(
        "wrong_column\nvalue\n",
        encoding="utf-8",
    )

    monkeypatch.setattr("app.calculator.Calculator", lambda: calc)

    output = run_calculator(monkeypatch, capsys, ["load", "exit"])

    assert "Load failed:" in output



# Tests for logging setup
def _read(path):
    """Return the text of a file."""
    return path.read_text(encoding="utf-8")

def test_logging_setup_records_initialization(calc):
    assert "Calculator initialized" in _read(calc.config.log_file)


def test_logging_setup_error_is_raised(monkeypatch):
    def fail(*args, **kwargs):
        raise OSError("Permission denied")

    monkeypatch.setattr("app.calculator.configure_logger", fail)

    with pytest.raises(OSError, match="Permission denied"):
        Calculator()

def test_undo_redo_and_clear_are_logged(calc):
    calc.set_operation(Addition())
    calc.perform_operation("1", "1")
    calc.undo()
    calc.redo()
    calc.clear_history()

    text = calc.config.log_file.read_text(encoding="utf-8")
    assert "Undo performed" in text
    assert "Redo performed" in text
    assert "History cleared" in text

# Tests for registering and removing observers

def test_register_observer(calc):
    observer = LoggingObserver()
    calc.register_observer(observer)

    assert observer in calc.observers


def test_remove_observer(calc):
    observer = LoggingObserver()
    calc.register_observer(observer)
    calc.remove_observer(observer)

    assert observer not in calc.observers


def test_removed_observer_is_not_notified(calc):
    seen = []

    class Spy:
        def update(self, calculation):
            seen.append(calculation)

    spy = Spy()
    calc.register_observer(spy)
    calc.remove_observer(spy)
    calc.set_operation(Addition())
    calc.perform_operation(Decimal("1"), Decimal("1"))

    assert seen == []


# Tests for input validation

@pytest.mark.parametrize("a, b", [("abc", "1"), ("1", "nan"), ("1e1000", "1")])
def test_invalid_input_is_rejected_and_not_recorded(calc, a, b):
    calc.set_operation(Addition())

    with pytest.raises(ValidationError):
        calc.perform_operation(a, b)

    assert calc.history == []


def test_rejected_input_is_logged(calc):
    calc.set_operation(Addition())

    with pytest.raises(ValidationError):
        calc.perform_operation("abc", "1")

    assert "Calculation rejected" in _read(calc.config.log_file)


def test_numeric_strings_are_accepted(calc):
    calc.set_operation(Addition())

    assert calc.perform_operation("10", " 5 ") == Decimal("15")


def test_validator_keeps_whole_numbers_readable(calc):
    calc.set_operation(Addition())
    calc.perform_operation("10", "0")

    assert str(calc.history[0].operand1) == "10"


# Tests for history limit and overflow

def test_history_is_trimmed_to_max_size(tmp_path):
    calc = Calculator(CalculatorConfig(base_dir=tmp_path, max_history_size=2))
    calc.set_operation(Addition())

    for number in ("1", "2", "3"):
        calc.perform_operation(number, "0")

    assert [c.operand1 for c in calc.history] == [Decimal("2"), Decimal("3")]


def test_decimal_overflow_becomes_operation_error(calc):
    calc.set_operation(Power())

    with pytest.raises(OperationError, match="Calculation failed"):
        calc.perform_operation("999999", "999999")

    assert calc.history == []


# Tests for factory-based REPL
@pytest.mark.parametrize("interrupt", [EOFError(), KeyboardInterrupt()])
def test_repl_exits_on_interrupt(monkeypatch, capsys, interrupt):
    def fake_input(_):
        raise interrupt

    monkeypatch.setattr("builtins.input", fake_input)
    calculator()

    assert "Goodbye!" in capsys.readouterr().out

def test_removed_alias_is_unknown(monkeypatch, capsys):
    output = run_calculator(
        monkeypatch, capsys, ["absolute_difference 4 10", "exit"]
    )

    assert "Unknown operation" in output


def test_repl_reports_oversized_input(monkeypatch, capsys):
    output = run_calculator(
        monkeypatch, capsys, ["add 1e1000 1", "exit"]
    )

    assert "Value exceeds maximum allowed" in output


def test_repl_reports_overflow(monkeypatch, capsys):
    output = run_calculator(
        monkeypatch, capsys, ["power 999999 999999", "exit"]
    )

    assert "Calculation failed" in output

def test_dynamic_help_includes_registered_operation():
    from decimal import Decimal
    from app.operations import Operation, OperationFactory, operation_help, HELP_REGISTRY

    command_name = "test_dynamic_help"

    @operation_help(command_name)
    class TestDynamicOperation(Operation):
        description = "Temporary operation for testing dynamic help"

        def execute(self, a: Decimal, b: Decimal) -> Decimal:
            return a + b

    try:
        operations = OperationFactory.available_operations()

        assert command_name in operations
        assert operations[command_name] == "Temporary operation for testing dynamic help"
        assert command_name in OperationFactory.get_supported_operations()
    finally:
        HELP_REGISTRY.pop(command_name, None)


