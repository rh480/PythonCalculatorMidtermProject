"""Basic arithmetic operations for the calculator."""

def addition(a: float, b:float) -> float:
    #Returns the sum of two numbers. The function takes two float inputs, 'a' and 'b', and returns their sum as a float.
    return a + b


def subtraction(a: float, b:float) -> float:
    #Returns the difference of two numbers. The function takes two float inputs, 'a' and 'b', and returns their difference as a float.
    return a - b

def multiplication(a: float, b:float) -> float:
    #Returns the product of two numbers. The function takes two float inputs, 'a' and 'b', and returns their product as a float.
    return a * b

def division(a: float, b: float) -> float:
    #Returns the quotient of two numbers. The function takes two float inputs, 'a' and 'b', and returns their quotient as a float.
    if b == 0:  # Checks if 'b' is zero. If it is, we raise an error and stop the function.
        raise ValueError("Division by zero is not allowed.")  # This sends an error message when someone tries to divide by zero.
    return a / b  # If 'b' is not zero, divide the first number (a) by the second number (b) and return the result.