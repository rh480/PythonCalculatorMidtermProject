import pytest
from app.operations import addition, subtraction, multiplication, division

def test_addition():
    # Tests the addition function with two positive numbers.
    assert addition(1, 1) == 2

def test_subtraction():
    # Tests the subtraction function with two positive numbers.
    assert subtraction(1, 1) == 0

def test_multiplication():
    # Tests the multiplication function with two positive numbers.
    assert multiplication(1, 1) == 1

def test_division_positive():
    # Tests the division function with two positive numbers.
    assert division(1, 1) == 1

def test_division_negative():
    # Tests the division function with a zero denominator.
    with pytest.raises(ValueError):
        division(1, 0)