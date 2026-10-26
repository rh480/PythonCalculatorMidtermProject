
"""Represent a completed calculator operation."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Calculation:
    """Store the details and timestamp of a completed calculation."""

    operation: str
    operand1: float
    operand2: float
    result: float
    timestamp: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        """Return a readable summary of the calculation."""
        return (
            f"{self.operation}({self.operand1}, {self.operand2}) "
            f"= {self.result}"
        )
