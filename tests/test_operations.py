import pytest
from decimal import Decimal
from typing import Any, Dict, Type

from app.exceptions import OperationError
from app.operations import (
    Operation,
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
    OperationFactory,
)


########################
# Base Operation Tests #
########################

class TestOperation:
    """Test the base Operation class."""

    def test_str_representation(self):
        """Test that the operation name is returned as a string."""

        class TestOp(Operation):
            def execute(self, a: Decimal, b: Decimal) -> Decimal:
                return a

        assert str(TestOp()) == "TestOp"


class BaseOperationTest:
    """Base class for testing calculator operations."""

    operation_class: Type[Operation]
    valid_test_cases: Dict[str, Dict[str, Any]]
    invalid_test_cases: Dict[str, Dict[str, Any]]

    def test_valid_operations(self):
        """Test that operations return the expected results."""
        operation = self.operation_class()

        for name, case in self.valid_test_cases.items():
            a = Decimal(str(case["a"]))
            b = Decimal(str(case["b"]))
            expected = Decimal(str(case["expected"]))

            result = operation.execute(a, b)

            assert result == expected, f"Failed case: {name}"

    def test_invalid_operations(self):
        """Test that invalid inputs raise the expected errors."""
        operation = self.operation_class()

        for name, case in self.invalid_test_cases.items():
            a = Decimal(str(case["a"]))
            b = Decimal(str(case["b"]))
            error = case.get("error", OperationError)
            message = case.get("message", "")

            with pytest.raises(error, match=message):
                operation.execute(a, b)


########################
# Addition Tests       #
########################

class TestAddition(BaseOperationTest):
    """Test Addition."""

    operation_class = Addition

    valid_test_cases = {
        "positive_numbers": {"a": "4", "b": "3", "expected": "7"},
        "negative_numbers": {"a": "-2", "b": "-5", "expected": "-7"},
        "mixed_signs": {"a": "-1", "b": "1", "expected": "0"},
        "zero_values": {"a": "0", "b": "0", "expected": "0"},
        "decimals": {"a": "1.5", "b": "2.5", "expected": "4.0"},
    }

    invalid_test_cases = {}


########################
# Subtraction Tests    #
########################

class TestSubtraction(BaseOperationTest):
    """Test Subtraction."""

    operation_class = Subtraction

    valid_test_cases = {
        "positive_numbers": {"a": "4", "b": "3", "expected": "1"},
        "negative_numbers": {"a": "-1", "b": "1", "expected": "-2"},
        "mixed_signs": {"a": "-2", "b": "5", "expected": "-7"},
        "zero_values": {"a": "0", "b": "0", "expected": "0"},
        "decimals": {"a": "1.5", "b": "2.5", "expected": "-1.0"},
    }

    invalid_test_cases = {}


########################
# Multiplication Tests #
########################

class TestMultiplication(BaseOperationTest):
    """Test Multiplication."""

    operation_class = Multiplication

    valid_test_cases = {
        "positive_numbers": {"a": "4", "b": "3", "expected": "12"},
        "negative_numbers": {"a": "-2", "b": "-5", "expected": "10"},
        "mixed_signs": {"a": "-2", "b": "5", "expected": "-10"},
        "multiply_by_zero": {"a": "5", "b": "0", "expected": "0"},
        "decimals": {"a": "1.5", "b": "2.5", "expected": "3.75"},
    }

    invalid_test_cases = {}


########################
# Division Tests       #
########################

class TestDivision(BaseOperationTest):
    """Test Division."""

    operation_class = Division

    valid_test_cases = {
        "positive_numbers": {"a": "10", "b": "2", "expected": "5"},
        "negative_numbers": {"a": "-10", "b": "-2", "expected": "5"},
        "mixed_signs": {"a": "-10", "b": "2", "expected": "-5"},
        "decimal_result": {"a": "7", "b": "2", "expected": "3.5"},
        "divide_zero": {"a": "0", "b": "5", "expected": "0"},
    }

    invalid_test_cases = {
        "divide_by_zero": {
            "a": "10",
            "b": "0",
            "message": "Division by zero is not allowed",
        },
    }


########################
# Power Tests          #
########################

class TestPower(BaseOperationTest):
    """Test Power."""

    operation_class = Power

    valid_test_cases = {
        "positive_exponent": {"a": "4", "b": "3", "expected": "64"},
        "negative_base": {"a": "-1", "b": "3", "expected": "-1"},
        "zero_exponent": {"a": "5", "b": "0", "expected": "1"},
        "negative_exponent": {"a": "5", "b": "-1", "expected": "0.2"},
        "decimal_base": {"a": "1.5", "b": "3", "expected": "3.375"},
    }

    invalid_test_cases = {
        "zero_to_zero": {
            "a": "0",
            "b": "0",
            "message": "Zero cannot be raised to zero or a negative power",
        },
        "zero_to_negative": {
            "a": "0",
            "b": "-1",
            "message": "Zero cannot be raised to zero or a negative power",
        },
        "negative_base_fractional_exponent": {
            "a": "-4",
            "b": "0.5",
            "message": "Cannot raise a negative number to a fractional power",
        },
    }


########################
# Root Tests           #
########################

class TestRoot(BaseOperationTest):
    """Test Root."""

    operation_class = Root

    valid_test_cases = {
        "square_root": {"a": "16", "b": "2", "expected": "4"},
        "cube_root": {"a": "-27", "b": "3", "expected": "-3"},
        "root_of_zero": {"a": "0", "b": "3", "expected": "0"},
        "negative_degree": {"a": "16", "b": "-4", "expected": "0.5"},
        "fractional_degree": {"a": "0.25", "b": "0.5", "expected": "0.0625"},
    }

    invalid_test_cases = {
        "zero_degree": {
            "a": "16",
            "b": "0",
            "message": "The degree of the root cannot be zero",
        },
        "negative_base_even_root": {
            "a": "-16",
            "b": "4",
            "message": "Cannot take an even or non-integer root of a negative number",
        },
        "negative_base_fractional_root": {
            "a": "-16",
            "b": "1.5",
            "message": "Cannot take an even or non-integer root of a negative number",
        },
        "zero_to_negative_degree": {
            "a": "0",
            "b": "-1",
            "message": "Zero cannot have a negative root degree",
        },
    }


########################
# Modulus Tests        #
########################

class TestModulus(BaseOperationTest):
    """Test Modulus."""

    operation_class = Modulus

    valid_test_cases = {
        "positive_numbers": {"a": "10", "b": "3", "expected": "1"},
        "negative_dividend": {"a": "-10", "b": "3", "expected": "-1"},
        "negative_divisor": {"a": "10", "b": "-3", "expected": "1"},
        "zero_dividend": {"a": "0", "b": "3", "expected": "0"},
        "decimal_numbers": {"a": "7.5", "b": "2", "expected": "1.5"},
        "equal_division": {"a": "10.5", "b": "0.5", "expected": "0"},
    }

    invalid_test_cases = {
        "modulus_by_zero": {
            "a": "10",
            "b": "0",
            "message": "Cannot calculate modulus with zero",
        },
    }


########################
# Integer Division     #
########################

class TestIntegerDivision(BaseOperationTest):
    """Test Integer Division."""

    operation_class = IntegerDivision

    valid_test_cases = {
        "even_division": {"a": "15", "b": "5", "expected": "3"},
        "fractional_result": {"a": "7", "b": "2", "expected": "3"},
        "negative_result": {"a": "15", "b": "-3", "expected": "-5"},
        "negative_dividend": {"a": "-7", "b": "2", "expected": "-3"},
        "zero_dividend": {"a": "0", "b": "5", "expected": "0"},
    }

    invalid_test_cases = {
        "divide_by_zero": {
            "a": "10",
            "b": "0",
            "message": "Integer division by zero is not allowed",
        },
    }


########################
# Percentage Tests     #
########################

class TestPercentage(BaseOperationTest):
    """Test Percentage."""

    operation_class = Percentage

    valid_test_cases = {
        "basic_percentage": {"a": "25", "b": "100", "expected": "25"},
        "larger_denominator": {"a": "50", "b": "200", "expected": "25"},
        "half": {"a": "15", "b": "30", "expected": "50"},
        "small_denominator": {"a": "10", "b": "0.5", "expected": "2000"},
        "zero_percentage": {"a": "0", "b": "100", "expected": "0"},
        "decimal_percentage": {"a": "1", "b": "8", "expected": "12.5"},
    }

    invalid_test_cases = {
        "percentage_by_zero": {
            "a": "10",
            "b": "0",
            "message": "Cannot calculate a percentage with zero as the second number",
        },
    }


########################
# Absolute Difference  #
########################

class TestAbsoluteDifference(BaseOperationTest):
    """Test Absolute Difference."""

    operation_class = AbsoluteDifference

    valid_test_cases = {
        "positive_numbers": {"a": "10", "b": "4", "expected": "6"},
        "reverse_order": {"a": "4", "b": "10", "expected": "6"},
        "negative_numbers": {"a": "-5", "b": "-10", "expected": "5"},
        "mixed_signs": {"a": "-3", "b": "2", "expected": "5"},
        "zero_values": {"a": "0", "b": "0", "expected": "0"},
        "equal_numbers": {"a": "5", "b": "5", "expected": "0"},
        "decimals": {"a": "5.5", "b": "2.2", "expected": "3.3"},
    }

    invalid_test_cases = {}


########################
# Factory Tests        #
########################

class TestOperationFactory:
    """Test OperationFactory."""

    def test_create_valid_operations(self):
        """Test that each command creates the correct operation."""
        operation_map = {
            "add": Addition,
            "subtract": Subtraction,
            "multiply": Multiplication,
            "divide": Division,
            "power": Power,
            "root": Root,
            "modulus": Modulus,
            "int_divide": IntegerDivision,
            "percent": Percentage,
            "abs_diff": AbsoluteDifference,
        }

        for name, operation_class in operation_map.items():
            operation = OperationFactory.create_operation(name)
            assert isinstance(operation, operation_class)

            # Commands should also work with uppercase letters.
            operation = OperationFactory.create_operation(name.upper())
            assert isinstance(operation, operation_class)

    def test_create_invalid_operation(self):
        """Test that an unknown command raises an error."""
        with pytest.raises(
            OperationError,
            match="Unknown operation: invalid_op",
        ):
            OperationFactory.create_operation("invalid_op")

    def test_available_operations(self):
        """Test that the factory returns operation descriptions."""
        operations = OperationFactory.available_operations()

        assert "add" in operations
        assert "divide" in operations
        assert "root" in operations
        assert len(operations) == 10
