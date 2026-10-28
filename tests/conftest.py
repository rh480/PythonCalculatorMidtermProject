"""Shared pytest setup."""

import pytest

ENV_VARS = [
    "CALCULATOR_BASE_DIR", "CALCULATOR_LOG_DIR", "CALCULATOR_LOG_FILE",
    "CALCULATOR_HISTORY_DIR", "CALCULATOR_HISTORY_FILE",
    "CALCULATOR_MAX_HISTORY_SIZE", "CALCULATOR_AUTO_SAVE",
    "CALCULATOR_PRECISION", "CALCULATOR_MAX_INPUT_VALUE",
    "CALCULATOR_DEFAULT_ENCODING",
]


@pytest.fixture(autouse=True)
def isolated_environment(tmp_path, monkeypatch):
    """Ignore .env values and send logs/history to a temp folder."""
    for name in ENV_VARS:
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("CALCULATOR_BASE_DIR", str(tmp_path))
    