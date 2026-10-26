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

def power(a: float, b: float) -> float:
    #Returns the result of raising 'a' to the power of 'b'. The function takes two float inputs, 'a' and 'b', and returns 'a' raised to the power of 'b' as a float.
    if a == 0 and b < 0: # Checks if 'a' is zero and 'b' is negative. If both conditions are true, it raises a ValueError with the message "Zero cannot be raised to a negative power."
        raise ValueError("Zero cannot be raised to a negative power.")
    return a ** b



def root(a: float, b: float) -> float:
    #Calculate the b-th root of a.
    if b == 0: # Checks if 'b' is zero. If it is, we raise an error and stop the function.
        raise ValueError("The degree of the root cannot be zero.")
    if a == 0 and b < 0: # Checks if 'a' is zero and 'b' is negative. If both conditions are true, it raises a ValueError with the message "Zero cannot have a negative root degree."
        raise ValueError("Zero cannot have a negative root degree.")
    if a < 0: # Checks if 'a' is negative. If it is, we check if 'b' is an even integer or not. If 'b' is an even integer or a non-integer, we raise a ValueError with the message "Cannot take an even or non-integer root of a negative number."
        if not float(b).is_integer() or int(b) % 2 == 0:
            raise ValueError(
                "Cannot take an even or non-integer root of a negative number."
            )
        return -((-a) ** (1 / b))

    return a ** (1 / b)


def modulus(a: float, b: float) -> float:
    #Return the remainder after dividing a by b.
    if b == 0: # Checks if 'b' is zero. If it is, we raise an error and stop the function.
        raise ValueError("Cannot calculate modulus with zero.")
    result = a % b
    return 0.0 if result == 0 else result


def int_divide(a: float, b: float) -> float:
    #Returns the integer quotient of two numbers. The function takes two float inputs, 'a' and 'b', and returns the quotient with the fractional part discarded as a float.
    if b == 0:  # Checks if 'b' is zero. If it is, we raise an error and stop the function.
        raise ValueError("Integer division by zero is not allowed.")  # This sends an error message when someone tries to perform integer division by zero.
    return float(int(a / b))  # Divides 'a' by 'b', discards the fractional part, converts the result to a float, and returns it.


def percent(a: float, b: float) -> float:
    #Returns the percentage of 'a' with respect to 'b'. The function takes two float inputs, 'a' and 'b', and returns (a / b) * 100 as a float.
    if b == 0:  # Checks if 'b' is zero. If it is, we raise an error and stop the function.
        raise ValueError("Cannot calculate a percentage with zero as the second number.")  # This sends an error message when someone tries to calculate a percentage with zero as the second number.
    return (a / b) * 100  # Divides 'a' by 'b', multiplies the result by 100, and returns the percentage.
