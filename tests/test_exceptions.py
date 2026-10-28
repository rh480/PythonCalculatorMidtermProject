"""Tests for the calculator exception hierarchy."""

import pytest

from app.exceptions import (
    CalculatorError,
    ConfigurationError,
    OperationError,
    PersistenceError,
    ValidationError,
)

ALL_ERRORS = [
    CalculatorError,
    ValidationError,
    OperationError,
    ConfigurationError,
    PersistenceError,
]


@pytest.mark.parametrize("error_class", ALL_ERRORS)
def test_error_carries_its_message(error_class):
    """Each exception can be raised and keeps the message it was given."""
    with pytest.raises(error_class) as exc_info:
        raise error_class("something went wrong")
    assert str(exc_info.value) == "something went wrong"


@pytest.mark.parametrize("error_class", ALL_ERRORS)
def test_every_error_is_a_calculator_error(error_class):
    """Catching CalculatorError handles every custom exception."""
    with pytest.raises(CalculatorError):
        raise error_class("problem")


def test_persistence_error_is_an_operation_error():
    """Existing 'except OperationError' handlers also catch PersistenceError."""
    with pytest.raises(OperationError):
        raise PersistenceError("Could not read history")


@pytest.mark.parametrize(
    "error_class", [ValidationError, ConfigurationError]
)
def test_sibling_errors_are_not_operation_errors(error_class):
    """ValidationError and ConfigurationError are separate from OperationError."""
    assert not issubclass(error_class, OperationError)
    