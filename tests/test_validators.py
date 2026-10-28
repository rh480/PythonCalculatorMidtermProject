"""Tests for InputValidator."""

from decimal import Decimal

import pytest

from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError
from app.input_validators import InputValidator

# Configuration with a maximum input value of 1 million
config = CalculatorConfig(max_input_value=Decimal("1000000"))

#parametrize test cases for valid inputs
@pytest.mark.parametrize(
    "value, expected",
    [
        (123, Decimal("123")),
        (123.456, Decimal("123.456")),
        ("123", Decimal("123")),
        ("123.456", Decimal("123.456")),
        (-789, Decimal("-789")),
        (-789.123, Decimal("-789.123")),
        ("-789", Decimal("-789")),
        ("-789.123", Decimal("-789.123")),
        (0, Decimal("0")),
        ("  456  ", Decimal("456")),
        (1_000_000, Decimal("1000000")),  # exactly the maximum is allowed
    ],
)
#valid numbers and numeric strings convert to Decimal
def test_validate_number_valid(value, expected):
    """Valid numbers and numeric strings convert to Decimal."""
    assert InputValidator.validate_number(value, config) == expected

#parametrize test cases for invalid inputs
@pytest.mark.parametrize(
    "value, message",
    [
        ("abc", "Invalid number format: abc"),
        ("", "Invalid number format: "),
        ("   ", "Invalid number format: "),
        (None, "Invalid number format: None"),
        ([], "Invalid number format: "),
        ("nan", "Invalid number format: nan"),
    ],
)
#invalid inputs raise ValidationError with appropriate message
def test_validate_number_invalid_format(value, message):
    """Input that is not a number raises ValidationError."""
    with pytest.raises(ValidationError, match=message):
        InputValidator.validate_number(value, config)

#parametrize test cases for inputs exceeding max_input_value
@pytest.mark.parametrize(
    "value",
    [
        Decimal("1000001"),
        "1000001",
        -Decimal("1000001"),
        "-1000001",
        "inf",
        "-inf",
    ],
)
#values beyond the configured maximum (including infinity) are rejected
def test_validate_number_exceeds_max(value):
    """Values beyond the configured maximum (including infinity) are rejected."""
    with pytest.raises(ValidationError, match="Value exceeds maximum allowed"):
        InputValidator.validate_number(value, config)
        