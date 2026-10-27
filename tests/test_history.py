
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
    assert "1. Addition(2, 3) = 5" in captured.out
    assert "2. Multiplication(4, 5) = 20" in captured.out
