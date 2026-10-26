
import pytest
from app.operations import addition, division, multiplication, power, subtraction


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (4, 3, 7),  # Test case 1: Adding two positive integers. The expected result is 7.
        (-1, 1, 0),  # Test case 2: Adding a negative and a positive integer. The expected result is 0. 
        (0, 0, 0),  # Test case 3: Adding two zeros. The expected result is 0.
        (-2, 5, 3),  # Test case 4: Adding a negative and a positive integer. The expected result is 3.
        (1.5, 2.5, 4.0),  # Test case 5: Adding two decimal numbers. The expected result is 4.0.
    ],
)
def test_addition(a, b, expected):
    assert addition(a, b) == pytest.approx(expected)



@pytest.mark.parametrize(
    "a, b, expected",
    [
        (4, 3, 1),  # Test case 1: Subtracting two positive integers. The expected result is 1.
        (-1, 1, -2),  # Test case 2: Subtracting a positive integer from a negative integer. The expected result is -2.
        (0, 0, 0),  # Test case 3: Subtracting two zeros. The expected result is 0.
        (-2, 5, -7),  # Test case 4: Subtracting a positive integer from a negative integer. The expected result is -7.
        (1.5, 2.5, -1.0),  # Test case 5: Subtracting two decimal numbers. The expected result is -1.0.
    ],
)
def test_subtraction(a, b, expected):
    assert subtraction(a, b) == pytest.approx(expected)

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (4, 3, 12),  # Test case 1: Multiplying two positive integers. The expected result is 12.
        (-1, 1, -1),  # Test case 2: Multiplying a negative integer by a positive integer. The expected result is -1.
        (0, 0, 0),  # Test case 3: Multiplying two zeros. The expected result is 0.
        (-2, 5, -10),  # Test case 4: Multiplying a negative integer by a positive integer. The expected result is -10.
        (1.5, 2.5, 3.75),  # Test case 5: Multiplying two decimal numbers. The expected result is 3.75.
    ],
)
def test_multiplication(a, b, expected):
    assert multiplication(a, b) == pytest.approx(expected)


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (10, 2, 5), #Test case 1: Dividing two positive integers. The expected result is 5.
        (-10, 2, -5), #Test case 2: Dividing a negative integer by a positive integer. The expected result is -5.
        (10, -2, -5), #Test case 3: Dividing a positive integer by a negative integer. The expected result is -5.
        (-10, -2, 5), #Test case 4: Dividing two negative integers. The expected result is 5.
        (7, 2, 3.5), #Test case 5: Dividing two positive integers that do not divide evenly. The expected result is 3.5.
    ],
)
def test_division(a, b, expected):
    assert division(a, b) == pytest.approx(expected)


def test_division_by_zero():
    with pytest.raises(
        ValueError,
        match="Division by zero is not allowed.",
    ):
        division(10, 0)

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (4, 3, 64),  # Test case 1: Raising a positive integer to the power of another positive integer. The expected result is 64.
        (-1, 1, -1),  # Test case 2: Raising a negative integer to the power of a positive integer. The expected result is -1.
        (1, 0, 1),  # Test case 3: Raising one to the power of zero. The expected result is 1.
        (-2, 5, -32),  # Test case 4: Raising a negative integer to the power of a positive integer. The expected result is -32.
        (1.5, 3, 3.375),  # Test case 5: Raising a decimal number to the power of another decimal number. The expected result is 3.375.
    ],
)
def test_power(a, b, expected):
    assert power(a, b) == pytest.approx(expected)

def test_power_zero_to_negative_exponent():
    with pytest.raises(
        ValueError,
        match="Zero cannot be raised to a negative power."
    ):
        power(0, -1)