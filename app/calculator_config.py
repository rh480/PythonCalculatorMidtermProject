"""Calculator configuration from constructor arguments, environment, or defaults."""

import codecs
import os
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Optional, Union

from dotenv import load_dotenv

from app.exceptions import ConfigurationError

# Load environment variables from a .env file into the program's environment
load_dotenv()


def get_project_root() -> Path:
    """Return the project root directory (one level above the app package)."""
    return Path(__file__).parent.parent


def _read_env(name: str, default: str, cast):
    """Read an environment variable and convert it, or raise ConfigurationError."""
    raw = os.getenv(name, default)
    try:
        return cast(raw)
    except ValueError:
        raise ConfigurationError(f"Invalid value for {name}: {raw!r}") from None


class CalculatorConfig:
    """
    Calculator configuration settings.

    Each value is taken from the constructor argument if given, otherwise from
    its CALCULATOR_* environment variable (loaded from .env), otherwise from a
    built-in default. Settings are validated as soon as the object is created.
    """

    def __init__(
        self,
        base_dir: Optional[Path] = None,
        max_history_size: Optional[int] = None,
        auto_save: Optional[bool] = None,
        precision: Optional[int] = None,
        max_input_value: Optional[Union[int, float, Decimal]] = None,
        default_encoding: Optional[str] = None,
    ):
        """Initialize configuration, then validate it."""
        # Base directory defaults to the project root
        self.base_dir = base_dir or Path(
            os.getenv("CALCULATOR_BASE_DIR", str(get_project_root()))
        ).resolve()

        # Maximum number of history entries
        self.max_history_size = (
            max_history_size if max_history_size is not None
            else _read_env("CALCULATOR_MAX_HISTORY_SIZE", "1000", int)
        )

        # Whether history is saved automatically after each calculation
        self.auto_save = (
            auto_save if auto_save is not None
            else os.getenv("CALCULATOR_AUTO_SAVE", "true").strip().lower()
            in ("true", "1", "yes")
        )

        # Number of decimal places shown in results
        self.precision = (
            precision if precision is not None
            else _read_env("CALCULATOR_PRECISION", "10", int)
        )

        # Largest absolute value accepted as input (kept as Decimal to match
        # the Decimal-based InputValidator)
        raw_max = (
            max_input_value if max_input_value is not None
            else os.getenv("CALCULATOR_MAX_INPUT_VALUE", "1e999")
        )
        try:
            self.max_input_value = Decimal(str(raw_max))
        except InvalidOperation:
            raise ConfigurationError(
                f"Invalid value for max_input_value: {raw_max!r}"
            ) from None

        # Encoding used when reading and writing files
        self.default_encoding = (
            default_encoding or os.getenv("CALCULATOR_DEFAULT_ENCODING", "utf-8")
        )

        self.validate()  # fail fast on startup

    @property
    def log_dir(self) -> Path:
        """Directory where log files are stored."""
        return Path(os.getenv(
            "CALCULATOR_LOG_DIR", str(self.base_dir / "logs")
        )).resolve()

    @property
    def history_dir(self) -> Path:
        """Directory where history files are stored."""
        return Path(os.getenv(
            "CALCULATOR_HISTORY_DIR", str(self.base_dir / "history")
        )).resolve()

    @property
    def history_file(self) -> Path:
        """Path of the CSV file used to save and load history."""
        return Path(os.getenv(
            "CALCULATOR_HISTORY_FILE",
            str(self.history_dir / "calculator_history.csv"),
        )).resolve()

    @property
    def log_file(self) -> Path:
        """Path of the log file."""
        return Path(os.getenv(
            "CALCULATOR_LOG_FILE", str(self.log_dir / "calculator.log")
        )).resolve()

    def validate(self) -> None:
        """Raise ConfigurationError if any setting is invalid."""
        if self.max_history_size <= 0:
            raise ConfigurationError("max_history_size must be positive")
        if self.precision <= 0:
            raise ConfigurationError("precision must be positive")
        if self.max_input_value.is_nan() or self.max_input_value <= 0:
            raise ConfigurationError("max_input_value must be positive")
        try:
            codecs.lookup(self.default_encoding)
        except LookupError:
            raise ConfigurationError(
                f"Unknown encoding: {self.default_encoding}"
            ) from None
        