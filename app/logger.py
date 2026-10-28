
"""Configure logging for the calculator application."""

import logging
from pathlib import Path


def configure_logger(
    log_file: str | Path,
    encoding: str = "utf-8",
) -> None:
    """Set up logging to write messages to a file."""
    path = Path(log_file)
    path.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        filename=str(path),
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding=encoding,
        force=True,
    )
