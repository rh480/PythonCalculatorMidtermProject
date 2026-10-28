#Calculation tests

from datetime import datetime
from app.calculation import Calculation


def test_calculation_to_dict():
    timestamp = datetime(2026, 1, 1, 12, 0, 0)
    calculation = Calculation(
        operation="add",
        operand1=5.0,
        operand2=3.0,
        result=8.0,
        timestamp=timestamp
    )

    data = calculation.to_dict()

    assert data["operation"] == "add"
    assert float(data["operand1"]) == 5.0
    assert float(data["operand2"]) == 3.0
    assert float(data["result"]) == 8.0
    assert data["timestamp"] == timestamp.isoformat()


def test_calculation_from_dict():
    data = {
        "operation": "add",
        "operand1": "5.0",
        "operand2": "3.0",
        "result": "8.0",
        "timestamp": "2026-01-01T12:00:00"
    }

    calculation = Calculation.from_dict(data)

    assert calculation.operation == "add"
    assert calculation.operand1 == 5.0
    assert calculation.operand2 == 3.0
    assert calculation.result == 8.0
    assert calculation.timestamp == datetime(2026, 1, 1, 12, 0, 0)
    