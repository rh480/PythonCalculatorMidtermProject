"""Tests for CalculatorConfig."""

from decimal import Decimal
from pathlib import Path

import pytest

from app.calculator_config import CalculatorConfig, get_project_root
from app.exceptions import ConfigurationError

ENV_VARS = [
    "CALCULATOR_BASE_DIR", "CALCULATOR_LOG_DIR", "CALCULATOR_LOG_FILE",
    "CALCULATOR_HISTORY_DIR", "CALCULATOR_HISTORY_FILE",
    "CALCULATOR_MAX_HISTORY_SIZE", "CALCULATOR_AUTO_SAVE",
    "CALCULATOR_PRECISION", "CALCULATOR_MAX_INPUT_VALUE",
    "CALCULATOR_DEFAULT_ENCODING",
]


@pytest.fixture(autouse=True)
def clean_env(monkeypatch):
    """Start every test with no calculator variables set (even from .env)."""
    for name in ENV_VARS:
        monkeypatch.delenv(name, raising=False)


def test_default_configuration(tmp_path):
    config = CalculatorConfig(base_dir=tmp_path)
    assert config.max_history_size == 1000
    assert config.auto_save is True
    assert config.precision == 10
    assert config.max_input_value == Decimal("1e999")
    assert config.default_encoding == "utf-8"
    assert config.log_dir == (tmp_path / "logs").resolve()
    assert config.history_dir == (tmp_path / "history").resolve()
    assert config.log_file == (tmp_path / "logs" / "calculator.log").resolve()
    assert config.history_file == (
        tmp_path / "history" / "calculator_history.csv"
    ).resolve()


def test_environment_overrides(monkeypatch):
    monkeypatch.setenv("CALCULATOR_MAX_HISTORY_SIZE", "500")
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "false")
    monkeypatch.setenv("CALCULATOR_PRECISION", "8")
    monkeypatch.setenv("CALCULATOR_MAX_INPUT_VALUE", "1000")
    monkeypatch.setenv("CALCULATOR_DEFAULT_ENCODING", "utf-16")
    config = CalculatorConfig()
    assert config.max_history_size == 500
    assert config.auto_save is False
    assert config.precision == 8
    assert config.max_input_value == Decimal("1000")
    assert config.default_encoding == "utf-16"


def test_path_environment_overrides(monkeypatch):
    monkeypatch.setenv("CALCULATOR_LOG_DIR", "./test_logs")
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", "./test_history")
    monkeypatch.setenv("CALCULATOR_HISTORY_FILE", "./test_history/test_history.csv")
    monkeypatch.setenv("CALCULATOR_LOG_FILE", "./test_logs/test_log.log")
    config = CalculatorConfig()
    assert config.log_dir == Path("./test_logs").resolve()
    assert config.history_dir == Path("./test_history").resolve()
    assert config.history_file == Path("./test_history/test_history.csv").resolve()
    assert config.log_file == Path("./test_logs/test_log.log").resolve()


def test_custom_arguments_override_environment(monkeypatch):
    monkeypatch.setenv("CALCULATOR_PRECISION", "8")
    config = CalculatorConfig(
        max_history_size=300,
        auto_save=True,
        precision=5,
        max_input_value=Decimal("500"),
        default_encoding="ascii",
    )
    assert config.max_history_size == 300
    assert config.auto_save is True
    assert config.precision == 5
    assert config.max_input_value == Decimal("500")
    assert config.default_encoding == "ascii"


@pytest.mark.parametrize("value", [500, 500.5, "500"])
def test_max_input_value_is_converted_to_decimal(value):
    assert CalculatorConfig(max_input_value=value).max_input_value == Decimal(str(value))


@pytest.mark.parametrize(
    "value, expected",
    [("true", True), ("TRUE", True), ("1", True), ("yes", True),
     ("false", False), ("0", False), ("no", False)],
)
def test_auto_save_environment_values(monkeypatch, value, expected):
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", value)
    assert CalculatorConfig().auto_save is expected


@pytest.mark.parametrize(
    "kwargs, message",
    [
        ({"max_history_size": -1}, "max_history_size must be positive"),
        ({"max_history_size": 0}, "max_history_size must be positive"),
        ({"precision": -1}, "precision must be positive"),
        ({"precision": 0}, "precision must be positive"),
        ({"max_input_value": Decimal("-1")}, "max_input_value must be positive"),
        ({"max_input_value": 0}, "max_input_value must be positive"),
        ({"max_input_value": "nan"}, "max_input_value must be positive"),
        ({"default_encoding": "not-a-codec"}, "Unknown encoding"),
    ],
)
def test_invalid_arguments(kwargs, message):
    with pytest.raises(ConfigurationError, match=message):
        CalculatorConfig(**kwargs)

@pytest.mark.parametrize(
    "var, value",
    [
        ("CALCULATOR_MAX_HISTORY_SIZE", "abc"),
        ("CALCULATOR_PRECISION", "abc"),
        ("CALCULATOR_MAX_INPUT_VALUE", "abc"),
    ],
)

def test_non_numeric_environment_values(monkeypatch, var, value):
    monkeypatch.setenv(var, value)
    with pytest.raises(ConfigurationError, match="Invalid value"):
        CalculatorConfig()

def test_validate_detects_later_changes():
    config = CalculatorConfig()
    config.max_history_size = 0
    with pytest.raises(ConfigurationError, match="max_history_size must be positive"):
        config.validate()


def test_get_project_root():
    assert (get_project_root() / "app").is_dir()
    