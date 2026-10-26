"""Input validation for calculator operands."""

from decimal import Decimal, InvalidOperation
from typing import Any

from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError


class InputValidator:
    """Validates and sanitizes calculator inputs."""

    @staticmethod
    def validate_number(value: Any, config: CalculatorConfig) -> Decimal:
        """
        Validate and convert input to Decimal.

        Args:
            value: Input value to validate (number or string).
            config: Calculator configuration (supplies max_input_value).

        Returns:
            Decimal: The validated number.

        Raises:
            ValidationError: If the input is not a number or is too large.
        """
        try:
            if isinstance(value, str):
                value = value.strip()  # allow "  456  "
            number = Decimal(str(value))  # str() first so 123.456 stays exactly 123.456
            if abs(number) > config.max_input_value:
                raise ValidationError(
                    f"Value exceeds maximum allowed: {config.max_input_value}"
                )
            return number.normalize()
        except InvalidOperation as e:
            raise ValidationError(f"Invalid number format: {value}") from e