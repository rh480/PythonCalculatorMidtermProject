"""Tests for CalculatorMemento."""

import dataclasses
from datetime import datetime
from decimal import Decimal

import pytest

from app.calculation import Calculation
from app.calculator_memento import CalculatorMemento


@pytest.fixture
def history():
    return [
        Calculation("Addition", Decimal("2"), Decimal("3"), Decimal("5")),
        Calculation("Subtraction", Decimal("5"), Decimal("1"), Decimal("4")),
    ]


def test_create_and_get_history(history):
    memento = CalculatorMemento.create(history)

    assert memento.get_history() == history
    assert isinstance(memento.history, tuple)


def test_snapshot_is_not_affected_by_later_changes(history):
    memento = CalculatorMemento.create(history)

    history.append(Calculation("Addition", Decimal("1"), Decimal("1"), Decimal("2")))

    assert len(memento.get_history()) == 2


def test_get_history_returns_a_copy(history):
    memento = CalculatorMemento.create(history)

    memento.get_history().clear()

    assert len(memento.get_history()) == 2


def test_memento_is_frozen(history):
    memento = CalculatorMemento.create(history)

    with pytest.raises(dataclasses.FrozenInstanceError):
        memento.history = ()


def test_empty_history_snapshot():
    assert CalculatorMemento.create([]).get_history() == []


def test_to_dict_and_from_dict_round_trip(history):
    memento = CalculatorMemento.create(history)

    data = memento.to_dict()
    restored = CalculatorMemento.from_dict(data)

    assert data["history"][0]["operation"] == "Addition"
    assert restored.get_history() == history
    assert restored.timestamp == memento.timestamp
    assert isinstance(restored.timestamp, datetime)
    