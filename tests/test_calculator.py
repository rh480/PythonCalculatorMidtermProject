"""Tests for the Calculator class and command-line interface."""

from decimal import Decimal

import pytest
import pandas as pd

from app.calculator_config import CalculatorConfig
from app.exceptions import PersistenceError, ValidationError
from app.history import LoggingObserver

from app.calculator import Calculator, calculator, main
from app.operations import (
    Operation,
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
    "inputs, expected",
    [
        (["add", "2", "3", "exit"], "Result: 5"),
        (["subtract", "2", "3", "exit"], "Result: -1"),
        (["multiply", "2", "3", "exit"], "Result: 6"),
        (["divide", "6", "2", "exit"], "Result: 3"),
        (["power", "2", "3", "exit"], "Result: 8"),
        (["root", "27", "3", "exit"], "Result: 3"),
        (["modulus", "10", "3", "exit"], "Result: 1"),
        (["int_divide", "7", "2", "exit"], "Result: 3"),
        (["percent", "1", "8", "exit"], "Result: 12.5"),
        (["abs_diff", "4", "10", "exit"], "Result: 6")
    ],
)
def test_calculator_commands(monkeypatch, capsys, inputs, expected):
    output = run_calculator(
        monkeypatch, capsys, inputs
    )

    assert expected in output


def test_invalid_operation(monkeypatch, capsys):
    output = run_calculator(
        monkeypatch, capsys, ["unknown", "exit"]
    )

    assert "Unknown operation" in output


def test_invalid_input(monkeypatch, capsys):
    output = run_calculator(
        monkeypatch, capsys, ["add", "two", "3", "exit"]
    )

    assert "Invalid number" in output


def test_non_numeric_input(monkeypatch, capsys):
    output = run_calculator(
        monkeypatch, capsys, ["add", "2", "three", "exit"]
    )

    assert "Invalid number" in output


def test_division_by_zero(monkeypatch, capsys):
    output = run_calculator(
        monkeypatch, capsys, ["divide", "5", "0", "exit"]
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
        monkeypatch, capsys, ["add", "2", "3", "history", "exit"]
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

# parametrize test cases for saved rows with bad numbers or timestamps
@pytest.mark.parametrize(
    "row",
    [
        "Addition,1,2,abc,2026-01-01T12:00:00",        # not a number
        "Addition,1,2,nan,2026-01-01T12:00:00",        # not finite
        "Addition,1,2,Infinity,2026-01-01T12:00:00",   # not finite
        "Addition,1,2,3,not-a-date",                   # invalid timestamp
    ],
)
# malformed rows raise PersistenceError and leave the history untouched
def test_load_history_with_bad_values(temporary_calc, tmp_path, row):
    file_path = tmp_path / "bad_values.csv"
    file_path.write_text(
        "operation,operand1,operand2,result,timestamp\n" + row + "\n",
        encoding="utf-8",
    )

    with pytest.raises(PersistenceError, match="Could not load history"):
        temporary_calc.load_history(file_path)

    # Nothing from the bad file should have been loaded.
    assert temporary_calc.history == []


# an empty file has no columns, so it cannot be loaded
def test_load_empty_history_file(temporary_calc, tmp_path):
    file_path = tmp_path / "empty.csv"
    file_path.write_text("", encoding="utf-8")

    with pytest.raises(PersistenceError):
        temporary_calc.load_history(file_path)

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

# the help example must match how the REPL really asks for numbers
def test_help_example_matches_prompted_input(monkeypatch, capsys):
    output = run_calculator(
        monkeypatch, capsys, ["help", "exit"]
    )

    assert "Example: type 'add'" in output

#  test clear command and undo/redo commands
def test_clear_command(monkeypatch, capsys):
    output = run_calculator(
        monkeypatch,
        capsys,
        ["add", "2", "3", "clear", "history", "exit"],
    )

    assert "Calculation history cleared." in output
    assert "No calculation history yet." in output


def test_undo_command(monkeypatch, capsys):
    output = run_calculator(
        monkeypatch, capsys, ["add", "2", "3", "undo", "history", "exit"]
    )

    assert "Last action undone." in output
    assert "No calculation history yet." in output


def test_redo_command(monkeypatch, capsys):
    output = run_calculator(
        monkeypatch, capsys, ["add", "2", "3", "undo", "redo", "history", "exit"],
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


# Tests for precision and result validation

def test_result_is_rounded_to_configured_precision(tmp_path):
    calc = Calculator(CalculatorConfig(base_dir=tmp_path, precision=2))
    calc.set_operation(Division())

    result = calc.perform_operation("1", "3")

    assert result == Decimal("0.33")
    assert calc.history[0].result == Decimal("0.33")
    assert calc.show_history() == ["Division(1, 3) = 0.33"]


def test_default_precision_is_ten_places(calc):
    calc.set_operation(Division())

    assert calc.perform_operation("2", "3") == Decimal("0.6666666667")


def test_precision_does_not_change_operands(tmp_path):
    calc = Calculator(CalculatorConfig(base_dir=tmp_path, precision=1))
    calc.set_operation(Addition())

    calc.perform_operation("1.25", "1.25")

    assert calc.history[0].operand1 == Decimal("1.25")
    assert calc.history[0].result == Decimal("2.5")


class FixedResultOperation(Operation):
    """Test operation that returns whatever value it was given."""

    def __init__(self, value):
        self.value = value

    def execute(self, a, b):
        return self.value


@pytest.mark.parametrize(
    "value", [Decimal("Infinity"), Decimal("-Infinity"), Decimal("NaN"), 1.5, None]
)
def test_invalid_result_is_rejected_and_not_recorded(calc, value):
    calc.set_operation(FixedResultOperation(value))

    with pytest.raises(OperationError):
        calc.perform_operation("1", "1")

    assert calc.history == []
    assert calc.undo() is False


def test_rejected_result_is_logged(calc):
    calc.set_operation(FixedResultOperation(Decimal("Infinity")))

    with pytest.raises(OperationError):
        calc.perform_operation("1", "1")

    assert "Calculation rejected" in _read(calc.config.log_file)


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
        monkeypatch, capsys, ["absolute_difference", "4", "10", "exit"]
    )

    assert "Unknown operation" in output


def test_repl_reports_oversized_input(monkeypatch, capsys):
    output = run_calculator(
        monkeypatch, capsys, ["add", "1e1000", "1", "exit"]
    )

    assert "Value exceeds maximum allowed" in output


def test_repl_reports_overflow(monkeypatch, capsys):
    output = run_calculator(
        monkeypatch, capsys, ["power", "999999", "999999", "exit"]
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


# Tests for startup, observer and save failures

# a corrupt saved history file is ignored at startup and logged as a warning
def test_corrupt_saved_history_is_ignored_at_startup(tmp_path):
    config = CalculatorConfig(base_dir=tmp_path)
    config.history_file.parent.mkdir(parents=True, exist_ok=True)
    config.history_file.write_text("wrong_column\nvalue\n", encoding="utf-8")

    calc = Calculator(config=config)

    assert calc.history == []
    assert "Could not load saved history" in _read(config.log_file)


# an observer that fails is logged and does not stop the calculation
def test_failing_observer_does_not_stop_the_calculation(calc):
    class FailingObserver:
        def update(self, calculation):
            raise PersistenceError("Observer failure")

    calc.register_observer(FailingObserver())
    calc.set_operation(Addition())

    result = calc.perform_operation("1", "1")

    assert result == Decimal("2")
    assert len(calc.history) == 1
    assert "Observer FailingObserver failed" in _read(calc.config.log_file)


# saving to a location that cannot be created raises PersistenceError
def test_save_history_failure_raises_persistence_error(temporary_calc, tmp_path):
    # A file where a folder is needed makes the save fail.
    blocker = tmp_path / "not_a_folder"
    blocker.write_text("x", encoding="utf-8")

    with pytest.raises(PersistenceError, match="Could not save history"):
        temporary_calc.save_history(blocker / "history.csv")

    assert "Could not save history" in _read(temporary_calc.config.log_file)


# Tests for undo, redo and cancel messages in the CLI

def test_undo_command_with_nothing_to_undo(monkeypatch, capsys):
    output = run_calculator(
        monkeypatch, capsys, ["undo", "exit"]
    )

    assert "Nothing to undo." in output


def test_redo_command_with_nothing_to_redo(monkeypatch, capsys):
    output = run_calculator(
        monkeypatch, capsys, ["redo", "exit"]
    )

    assert "Nothing to redo." in output


# parametrize test cases for Ctrl+D and Ctrl+C at a number prompt
@pytest.mark.parametrize("interrupt", [EOFError(), KeyboardInterrupt()])
# interrupting a number prompt cancels only that calculation
def test_calculation_is_cancelled_by_interrupt(monkeypatch, capsys, interrupt):
    responses = iter(["add", interrupt, "exit"])

    def fake_input(_):
        response = next(responses)
        if isinstance(response, BaseException):
            raise response
        return response

    monkeypatch.setattr("builtins.input", fake_input)
    calculator()

    output = capsys.readouterr().out
    assert "Calculation cancelled." in output
    assert "Goodbye!" in output


# Tests for the program entry point

def test_main_starts_the_calculator(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "exit")

    main()

    assert "Goodbye!" in capsys.readouterr().out


# an invalid configuration value exits with a clear message, not a traceback
def test_main_reports_invalid_configuration(monkeypatch, capsys):
    monkeypatch.setenv("CALCULATOR_PRECISION", "99")

    with pytest.raises(SystemExit) as exit_info:
        main()

    assert exit_info.value.code == 1
    assert "Configuration error: precision must not exceed 28" in capsys.readouterr().out