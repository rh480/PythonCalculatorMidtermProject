
"""Tests for calculator logging configuration."""

import logging

from app.logger import configure_logger


def test_configure_logger_writes_to_file(tmp_path):
    """Create a log file and write a message to it."""
    log_file = tmp_path / "logs" / "calculator.log"

    configure_logger(log_file)
    logging.info("Test log message")

    for handler in logging.getLogger().handlers:
        handler.flush()

    assert log_file.exists()
    assert "Test log message" in log_file.read_text(
        encoding="utf-8"
    )
