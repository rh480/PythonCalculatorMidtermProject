
from unittest.mock import Mock

from app.commands import (
    UndoCommand,
    RedoCommand,
    ClearHistoryCommand,
    HistoryCommand,
    SaveHistoryCommand,
    LoadHistoryCommand,
)


def test_undo_command():
    calculator = Mock()
    calculator.undo.return_value = True

    assert UndoCommand(calculator).execute() is True
    calculator.undo.assert_called_once_with()


def test_redo_command():
    calculator = Mock()
    calculator.redo.return_value = True

    assert RedoCommand(calculator).execute() is True
    calculator.redo.assert_called_once_with()


def test_clear_history_command():
    calculator = Mock()

    ClearHistoryCommand(calculator).execute()

    calculator.clear_history.assert_called_once_with()


def test_history_command():
    calculator = Mock()
    calculator.show_history.return_value = ["add(2, 3) = 5"]

    assert HistoryCommand(calculator).execute() == ["add(2, 3) = 5"]
    calculator.show_history.assert_called_once_with()


def test_save_history_command():
    calculator = Mock()

    SaveHistoryCommand(calculator).execute()

    calculator.save_history.assert_called_once_with()


def test_load_history_command():
    calculator = Mock()

    LoadHistoryCommand(calculator).execute()

    calculator.load_history.assert_called_once_with()
