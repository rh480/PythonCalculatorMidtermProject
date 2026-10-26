"""Custom exceptions for the calculator application."""


class CalculatorError(Exception):
    #Base class for all calculator errors.
    pass

class ValidationError(CalculatorError):
    #Raised when user input is invalid.
    pass

class OperationError(CalculatorError):
    #Raised when an operation cannot be performed (e.g. divide by zero).
    pass

class ConfigurationError(CalculatorError):
    #Raised when configuration values are invalid.
    pass

class PersistenceError(OperationError):
    #Raised when history cannot be saved or loaded.
    pass