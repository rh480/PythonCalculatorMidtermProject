
from app.calculator import calculator


def test_addition_command(monkeypatch, capsys):
    """Check that the calculator displays an addition result."""
    inputs = iter(["add 2 3", "exit"])
    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )

    calculator()

    output = capsys.readouterr().out
    assert "Result: 5.0" in output

def test_subtraction_command(monkeypatch, capsys):
    """Check that the calculator displays a subtraction result."""
    inputs = iter(["subtract 2 3", "exit"])
    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )

    calculator()

    output = capsys.readouterr().out
    assert "Result: -1.0" in output

def test_multiplication_command(monkeypatch, capsys):
    """Check that the calculator displays a multiplication result."""
    inputs = iter(["multiply 2 3", "exit"])
    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )

    calculator()

    output = capsys.readouterr().out
    assert "Result: 6.0" in output

def test_division_command(monkeypatch, capsys):
    """Check that the calculator displays a division result."""
    inputs = iter(["divide 6 2", "exit"])
    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )

    calculator()

    output = capsys.readouterr().out
    assert "Result: 3.0" in output


def test_invalid_operation(monkeypatch, capsys):
    """Check that an unsupported command is rejected."""
    inputs = iter(["unknown 2 3", "exit"])
    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )

    calculator()

    output = capsys.readouterr().out
    assert "Unknown operation" in output


def test_division_by_zero(monkeypatch, capsys):
    """Check that division by zero is handled gracefully."""
    inputs = iter(["divide 5 0", "exit"])
    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )

    calculator()

    output = capsys.readouterr().out
    assert "Division by zero is not allowed" in output
