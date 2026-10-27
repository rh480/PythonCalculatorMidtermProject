
"""Memento pattern for saving calculator state."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from app.calculation import Calculation


@dataclass(frozen=True)
class CalculatorMemento:
    """Store an immutable snapshot of calculator history."""

    history: tuple[Calculation, ...]
    timestamp: datetime = field(default_factory=datetime.now)

    @classmethod
    def create(cls, history: list[Calculation]) -> "CalculatorMemento":
        """Create a snapshot from the current calculation history."""
        return cls(history=tuple(history))

    def get_history(self) -> list[Calculation]:
        """Return a list containing the saved calculations."""
        return list(self.history)

    def to_dict(self) -> dict[str, Any]:
        """Convert the snapshot to a dictionary."""
        return {
            "history": [calculation.to_dict() for calculation in self.history],
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CalculatorMemento":
        """Reconstruct a snapshot from serialized data."""
        return cls(
            history=tuple(
                Calculation.from_dict(item) for item in data["history"]
            ),
            timestamp=datetime.fromisoformat(data["timestamp"]),
        )
