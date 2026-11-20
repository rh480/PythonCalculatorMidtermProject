"""Input validation for calculator operands."""

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP, localcontext
from typing import Any

from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError, OperationError


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
                value = value.strip()

            number = Decimal(str(value))

            if not number.is_finite():
                raise ValidationError(
                    "Input must be a finite number."
                )

            if abs(number) > config.max_input_value:
                raise ValidationError(
                    f"Value exceeds maximum allowed: "
                    f"{config.max_input_value}"
                )

            return number

        except (InvalidOperation, ValueError, TypeError) as error:
            raise ValidationError(
                f"Invalid number format: {value}"
            ) from error

    #Precision handling for arithmetic results
    @staticmethod
    def apply_precision(value: Decimal, places: int) -> Decimal:
        """
        Round a finite Decimal to the given number of decimal places.

        Whole numbers are returned without a fractional part (5, not
        5.0000000000) and trailing zeros are removed from other results.
        """
        # An exponent of zero or more means there is no fractional part.
        if value.as_tuple().exponent >= 0:
            return value

        # Quantizing needs enough digits of precision to hold the result,
        # so widen the context temporarily instead of failing.
        with localcontext() as context:
            context.prec = max(context.prec, value.adjusted() + places + 2)
            context.rounding = ROUND_HALF_UP
            rounded = value.quantize(Decimal(1).scaleb(-places))

            if rounded == rounded.to_integral_value():
                return Decimal(int(rounded))
            return rounded.normalize()

    @staticmethod
    def validate_result(result: Any, config: CalculatorConfig) -> Decimal:
        """
        Check an arithmetic result and round it to the configured precision.

        Raises:
            OperationError: If the result is not a finite number.
        """
        if not isinstance(result, Decimal):
            raise OperationError("Calculation produced a non-numeric result.")

        if not result.is_finite():
            raise OperationError(
                "Calculation produced a result that is not a finite number."
            )

        return InputValidator.apply_precision(result, config.precision)
