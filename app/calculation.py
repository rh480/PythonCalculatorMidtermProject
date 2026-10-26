
"""Represent a completed calculator operation."""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict

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

    
    # Convert calculation details to a dictionary for saving.
    def to_dict(self) -> Dict[str, Any]:
        return {
            "operation": self.operation,
            "operand1": str(self.operand1),
            "operand2": str(self.operand2),
            "result": str(self.result),
            "timestamp": self.timestamp.isoformat()
        }

    # Restore a calculation from saved dictionary data.
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Calculation":
        return cls(
            operation=data["operation"],
            operand1=float(Decimal(data["operand1"])),
            operand2=float(Decimal(data["operand2"])),
            result=float(Decimal(data["result"])),
            timestamp=datetime.fromisoformat(data["timestamp"])
        )

