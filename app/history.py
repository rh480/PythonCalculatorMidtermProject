
"""Observers for calculation history."""

import logging
from abc import ABC, abstractmethod

from app.calculation import Calculation


class HistoryObserver(ABC):
    """Base class for objects that react to calculations."""

    @abstractmethod
    def update(self, calculation: Calculation) -> None:
        """Handle a completed calculation."""
        pass


class LoggingObserver(HistoryObserver):
    """Record calculation results in the log."""

    def update(self, calculation: Calculation) -> None:
        if calculation is None:
            raise AttributeError("Calculation cannot be None")

        logging.info(
            "Calculation: %s(%s, %s) = %s",
            calculation.operation,
            calculation.operand1,
            calculation.operand2,
            calculation.result,
        )


class AutoSaveObserver(HistoryObserver):
    """Save history automatically when the feature is enabled."""

    def __init__(self, calculator):
        if not hasattr(calculator, "config") or not hasattr(
            calculator, "save_history"
        ):
            raise TypeError(
                "Calculator needs config and save_history attributes"
            )

        self.calculator = calculator

    def update(self, calculation: Calculation) -> None:
        if calculation is None:
            raise AttributeError("Calculation cannot be None")

        if self.calculator.config.auto_save:
            self.calculator.save_history()
            logging.info("Calculation history saved automatically")
