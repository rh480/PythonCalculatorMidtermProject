"""Represent a completed calculator operation."""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Any, Dict

def _parse_decimal(value: Any, name: str) -> Decimal:
    """Convert saved text to a finite Decimal or raise ValueError."""
    try:
        number = Decimal(str(value).strip())
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError(f"Invalid {name} in saved history: {value!r}") from None

    if not number.is_finite():
        raise ValueError(f"Non-finite {name} in saved history: {value!r}")

    return number

@dataclass
class Calculation:
    """Store the details and timestamp of a completed calculation."""

    operation: str
    operand1: Decimal
    operand2: Decimal
    result: Decimal
    timestamp: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        """Return a readable summary of the calculation."""
        return (
            f"{self.operation}({self.operand1}, {self.operand2}) "
            f"= {self.result}"
        )

    
    def to_dict(self) -> Dict[str, Any]:
        """Convert calculation details to a dictionary for saving."""
        return {
            "operation": self.operation,
            "operand1": str(self.operand1),
            "operand2": str(self.operand2),
            "result": str(self.result),
            "timestamp": self.timestamp.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Calculation":
        """Restore a calculation from saved dictionary data."""
        return cls(
            operation=data["operation"],
            operand1=_parse_decimal(data["operand1"], "operand1"),
            operand2=_parse_decimal(data["operand2"], "operand2"),
            result=_parse_decimal(data["result"], "result"),
            timestamp=datetime.fromisoformat(data["timestamp"])
        )