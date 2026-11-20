"""Tests for InputValidator."""

from decimal import Decimal

import pytest

from app.calculator_config import CalculatorConfig
from app.exceptions import OperationError, ValidationError
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
    ],
)
#invalid inputs raise ValidationError with appropriate message
def test_validate_number_invalid_format(value, message):
    """Input that is not a number raises ValidationError."""
    with pytest.raises(ValidationError, match=message):
        InputValidator.validate_number(value, config)

#parametrize test cases for non-finite numbers
@pytest.mark.parametrize(
    "value",
    [
        "nan",
        "inf",
        "-inf",
    ],
)
#non-finite numbers are rejected
def test_validate_number_rejects_non_finite(value):
    """Non-finite numbers are rejected."""
    with pytest.raises(
        ValidationError,
        match="Input must be a finite number",
    ):
        InputValidator.validate_number(value, config)

#parametrize test cases for inputs exceeding max_input_value
@pytest.mark.parametrize(
    "value",
    [
        Decimal("1000001"),
        "1000001",
        -Decimal("1000001"),
        "-1000001",
    ],
)
#values beyond the configured maximum (including infinity) are rejected
def test_validate_number_exceeds_max(value):
    """Values beyond the configured maximum are rejected."""
    with pytest.raises(
        ValidationError,
        match="Value exceeds maximum allowed",
    ):
        InputValidator.validate_number(value, config)


# parametrize test cases for rounding results to a number of decimal places
@pytest.mark.parametrize(
    "value, places, expected",
    [
        ("3.14159265358979", 2, "3.14"),
        ("2.675", 2, "2.68"),          # halves round up
        ("-2.675", 2, "-2.68"),        # ...away from zero for negatives
        ("1.50000", 4, "1.5"),         # trailing zeros are removed
        ("5.0000", 3, "5"),            # whole numbers lose the fraction
        ("0.9999999", 3, "1"),         # rounding can reach a whole number
        ("-0.0000001", 3, "0"),        # tiny negatives become plain zero
        ("12345678901234567890.123456789", 10, "12345678901234567890.123456789"),
    ],
)
# results are rounded half-up and shown without trailing zeros
def test_apply_precision(value, places, expected):
    """Results are rounded half-up and shown without trailing zeros."""
    result = InputValidator.apply_precision(Decimal(value), places)

    assert str(result) == expected


# numbers with no fractional part need no rounding
def test_apply_precision_leaves_large_whole_numbers_alone():
    """Numbers with no fractional part are returned unchanged."""
    value = Decimal("1E+500")

    assert InputValidator.apply_precision(value, 10) is value


# parametrize test cases for results that are not finite numbers
@pytest.mark.parametrize(
    "result",
    [Decimal("NaN"), Decimal("sNaN"), Decimal("Infinity"), Decimal("-Infinity")],
)
# non-finite results are rejected with an OperationError
def test_validate_result_rejects_non_finite(result):
    """Results that are not finite numbers raise OperationError."""
    with pytest.raises(OperationError, match="not a finite number"):
        InputValidator.validate_result(result, config)


# parametrize test cases for results that are not Decimal values
@pytest.mark.parametrize("result", [5.0, "5", None, 5])
# non-Decimal results are rejected with an OperationError
def test_validate_result_rejects_non_decimal(result):
    """Results that are not Decimal values raise OperationError."""
    with pytest.raises(OperationError, match="non-numeric"):
        InputValidator.validate_result(result, config)


# valid results are rounded using the configured precision
def test_validate_result_applies_configured_precision():
    """Valid results are rounded to the configured precision."""
    precise = CalculatorConfig(precision=3)

    assert InputValidator.validate_result(Decimal("1.23456"), precise) == Decimal("1.235")
