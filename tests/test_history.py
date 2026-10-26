
def test_empty_history(capsys, monkeypatch):
    """Display a message when no calculations have been recorded."""
    inputs = iter(["history", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    from app.calculator import calculator
    calculator()

    captured = capsys.readouterr()
    assert "No calculation history yet." in captured.out


def test_calculation_history(capsys, monkeypatch):
    """Display completed calculations in the history."""
    inputs = iter(["add 2 3", "multiply 4 5", "history", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    from app.calculator import calculator
    calculator()

    captured = capsys.readouterr()
    assert "1. add(2.0, 3.0) = 5.0" in captured.out
    assert "2. multiply(4.0, 5.0) = 20.0" in captured.out
