
import pytest
from app.operations import addition, subtraction, division, multiplication, power, root, modulus

'''Addition function tests'''

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
    # Test the addition function with various inputs and expected outputs.
    assert addition(a, b) == pytest.approx(expected)

'''Subtraction function tests'''

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
    # Test the subtraction function with various inputs and expected outputs.
    assert subtraction(a, b) == pytest.approx(expected)

'''Multiplication function tests'''

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
    # Test the multiplication function with various inputs and expected outputs.
    assert multiplication(a, b) == pytest.approx(expected)

'''Division function tests'''

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
    # Test the division function with various inputs and expected outputs.
    assert division(a, b) == pytest.approx(expected)


def test_division_by_zero():
    # Test that dividing by zero raises a ValueError with the correct message.
    with pytest.raises(
        ValueError,
        match="Division by zero is not allowed.",
    ):
        division(10, 0)

'''Power function tests'''

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (4, 3, 64),  # Test case 1: Raising a positive integer to the power of another positive integer. The expected result is 64.
        (-1, 1, -1),  # Test case 2: Raising a negative integer to the power of a positive integer. The expected result is -1.
        (1, 0, 1),  # Test case 3: Raising one to the power of zero. The expected result is 1.
        (0, 0, 1),  # Test case 4: Raising zero to the power of zero. The expected result is 1.
        (5, -1, 0.2),  # Test case 5: Raising five to the power of -1. The expected result is 0.2.
        (1.5, 3, 3.375),  # Test case 6: Raising a decimal number to the power of another decimal number. The expected result is 3.375.
    ],
)
def test_power(a, b, expected):
    # Test the power function with various inputs and expected outputs.
    assert power(a, b) == pytest.approx(expected)

def test_power_zero_to_negative_exponent():
    # Test that raising zero to a negative exponent raises a ValueError with the correct message.
    with pytest.raises(
        ValueError,
        match="Zero cannot be raised to a negative power."
    ):
        power(0, -1)

'''Root function tests'''

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (16, 4, 2),  # Test case 1: Taking the fourth root of a positive integer. The expected result is 2.
        (-27, 3, -3),  # Test case 2: Taking the cube root of a negative integer. The expected result is -3.
        (0, 3, 0),  # Test case 3: Taking the cube root of zero. The expected result is 0.
        (16, -4, 0.5),  # Test case 4: Taking the fourth root of a negative integer. The expected result is 0.5.
        (0.25, 0.5, 0.0625),  # Test case 5: Taking the 0.5th root of a decimal number. The expected result is 0.0625.
    ],
)
def test_root(a, b, expected):
    # Test the root function with various inputs and expected outputs.
    assert root(a, b) == pytest.approx(expected)

def test_root_zero_degree():
    # Test that taking the root with a degree of zero raises a ValueError with the correct message.
    with pytest.raises(ValueError, match="The degree of the root cannot be zero."):
        root(16, 0)

def test_root_negative():
    with pytest.raises(ValueError, match="Cannot take an even or non-integer root of a negative number."):
        root(-16, 4)

def test_root_zero_to_negative():
    with pytest.raises(ValueError, match="Zero cannot have a negative root degree."):
        root(0, -1)

'''Modulus function tests'''

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (10, 3, 1), #Test case 1: Modulus of two positive integers. The expected result is 1.
        (-10, 3, 2), #Test case 2: Modulus of a negative integer and a positive integer. The expected result is 2.
        (10, -3, -2), #Test case 3: Modulus of a positive integer and a negative integer. The expected result is -2.
        (-10, -3, -1), #Test case 4: Modulus of two negative integers. The expected result is -1.
        (0, 3, 0), #Test case 5: Modulus of zero and a positive integer. The expected result is 0.
        (7.5, 2, 1.5), #Test case 6: Modulus of a decimal number and a positive integer. The expected result is 1.5.
        (10.5, 0.5, 0), #Test case 7: Modulus of a decimal number and a decimal number. The expected result is 0.
    ],
)
def test_modulus(a, b, expected):
    assert modulus(a, b) == pytest.approx(expected)


def test_modulus_by_zero():
    with pytest.raises(ValueError):
        modulus(10, 0)
