"""Custom exceptions for the calculator application."""


class CalculatorError(Exception):
    '''Base class for all calculator errors.'''
    pass

class ValidationError(CalculatorError):
    """Raised when input validation fails."""    
    pass

class OperationError(CalculatorError):
    """Raised when a calculator operation fails."""
    pass

class ConfigurationError(CalculatorError):
    '''Raised when configuration values are invalid'''
    pass

class PersistenceError(OperationError):
    """Raised when calculation history cannot be saved or loaded."""
    pass
