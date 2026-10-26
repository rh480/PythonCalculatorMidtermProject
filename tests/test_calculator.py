
from app.calculator import calculator


def test_addition_command(monkeypatch, capsys):
    #Check that the calculator displays an addition result.
    inputs = iter(["add 2 3", "exit"])
    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )

    calculator()

    output = capsys.readouterr().out
    assert "Result: 5.0" in output

def test_subtraction_command(monkeypatch, capsys):
    #Check that the calculator displays a subtraction result.
    inputs = iter(["subtract 2 3", "exit"])
    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )

    calculator()

    output = capsys.readouterr().out
    assert "Result: -1.0" in output

def test_multiplication_command(monkeypatch, capsys):
    #Check that the calculator displays a multiplication result.
    inputs = iter(["multiply 2 3", "exit"])
    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )

    calculator()

    output = capsys.readouterr().out
    assert "Result: 6.0" in output

def test_division_command(monkeypatch, capsys):
    #Check that the calculator displays a division result.
    inputs = iter(["divide 6 2", "exit"])
    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )

    calculator()

    output = capsys.readouterr().out
    assert "Result: 3.0" in output


def test_invalid_operation(monkeypatch, capsys):
    #Check that an unsupported command is rejected.
    inputs = iter(["unknown 2 3", "exit"])
    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )

    calculator()

    output = capsys.readouterr().out
    assert "Unknown operation" in output


def test_invalid_input(monkeypatch, capsys):
    #Check that invalid input is handled gracefully.
    inputs = iter(["add 2", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    calculator()

    output = capsys.readouterr().out
    assert "Invalid input" in output

def test_non_numeric_input(monkeypatch, capsys):
    #Check that non-numeric input is handled gracefully.
    inputs = iter(["add two three", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    calculator()

    output = capsys.readouterr().out
    assert "Cannot use letters" in output

def test_exit_command(monkeypatch, capsys):
    #Check that the calculator exits gracefully.
    inputs = iter(["exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    calculator()

    output = capsys.readouterr().out
    assert "Goodbye!" in output

def test_division_by_zero(monkeypatch, capsys):
    #Check that division by zero is handled gracefully.
    inputs = iter(["divide 5 0", "exit"])
    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )

    calculator()

    output = capsys.readouterr().out
    assert "Division by zero is not allowed" in output


def test_power_command(monkeypatch, capsys):
    #Check that the calculator displays a power result.
    inputs = iter(["power 2 3", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    calculator()

    output = capsys.readouterr().out
    assert "Result: 8.0" in output


def test_root_command(monkeypatch, capsys):
    #Check that the calculator displays a root result.
    inputs = iter(["root 27 3", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    calculator()

    output = capsys.readouterr().out
    assert "Result: 3.0" in output


def test_modulus_command(monkeypatch, capsys):
    #Check that the calculator displays a modulus result.
    inputs = iter(["modulus 10 3", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    calculator()

    output = capsys.readouterr().out
    assert "Result: 1.0" in output


def test_integer_division_command(monkeypatch, capsys):
    #Check that the calculator displays an integer division result.
    inputs = iter(["int_divide 7 2", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    calculator()

    output = capsys.readouterr().out
    assert "Result: 3.0" in output


def test_percent_command(monkeypatch, capsys):
    #Check that the calculator displays a percentage result.
    inputs = iter(["percent 1 8", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    calculator()

    output = capsys.readouterr().out
    assert "Result: 12.5" in output


def test_absolute_difference_command(monkeypatch, capsys):
    #Check that the calculator displays an absolute difference result.
    inputs = iter(["absolute_difference 4 10", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    calculator()

    output = capsys.readouterr().out
    assert "Result: 6.0" in output