
"""Tests for the calculator history observers."""

import logging
from decimal import Decimal
from unittest.mock import Mock, patch

import pytest

from app.calculation import Calculation
from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.history import LoggingObserver, AutoSaveObserver


@pytest.fixture
def calculation():
    """Create a sample calculation for observer tests."""
    return Calculation(
        operation="Addition",
        operand1=Decimal("5"),
        operand2=Decimal("3"),
        result=Decimal("8"),
    )


# LoggingObserver tests

@patch("logging.info")
def test_logging_observer_logs_calculation(
    logging_info_mock, calculation
):
    """Log the details of a completed calculation."""
    observer = LoggingObserver()

    observer.update(calculation)

    logging_info_mock.assert_called_once_with(
        "Calculation: %s(%s, %s) = %s",
        "Addition",
        Decimal("5"),
        Decimal("3"),
        Decimal("8"),
    )


def test_logging_observer_no_calculation():
    """Reject a missing calculation."""
    observer = LoggingObserver()

    with pytest.raises(AttributeError):
        observer.update(None)


# AutoSaveObserver tests

def test_autosave_observer_triggers_save(calculation):
    """Save history when automatic saving is enabled."""
    calculator_mock = Mock(spec=Calculator)
    calculator_mock.config = Mock(spec=CalculatorConfig)
    calculator_mock.config.auto_save = True

    observer = AutoSaveObserver(calculator_mock)
    observer.update(calculation)

    calculator_mock.save_history.assert_called_once_with()


@patch("logging.info")
def test_autosave_observer_logs_autosave(
    logging_info_mock, calculation
):
    """Log when history is automatically saved."""
    calculator_mock = Mock(spec=Calculator)
    calculator_mock.config = Mock(spec=CalculatorConfig)
    calculator_mock.config.auto_save = True

    observer = AutoSaveObserver(calculator_mock)
    observer.update(calculation)

    logging_info_mock.assert_called_once_with(
        "Calculation history saved automatically"
    )


def test_autosave_observer_does_not_save_when_disabled(calculation):
    """Do not save history when automatic saving is disabled."""
    calculator_mock = Mock(spec=Calculator)
    calculator_mock.config = Mock(spec=CalculatorConfig)
    calculator_mock.config.auto_save = False

    observer = AutoSaveObserver(calculator_mock)
    observer.update(calculation)

    calculator_mock.save_history.assert_not_called()


def test_autosave_observer_invalid_calculator():
    """Reject an object without the required calculator interface."""
    with pytest.raises(TypeError):
        AutoSaveObserver(None)


def test_autosave_observer_no_calculation():
    """Reject a missing calculation."""
    calculator_mock = Mock(spec=Calculator)
    calculator_mock.config = Mock(spec=CalculatorConfig)
    calculator_mock.config.auto_save = False

    observer = AutoSaveObserver(calculator_mock)

    with pytest.raises(AttributeError):
        observer.update(None)
