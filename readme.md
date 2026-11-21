# Python Calculator Midterm Project

## Overview

This project is a command-line calculator application built with Python. It supports arithmetic operations, calculation history, undo and redo functionality, configurable settings, logging, and persistent history storage.

The project demonstrates object-oriented programming, software design patterns, input validation, automated testing, and continuous integration.

## Features

- **Arithmetic operations:** Addition, subtraction, multiplication, division, exponentiation, roots, modulus, integer division, percentage, and absolute difference.
- **Interactive CLI:** Perform calculations and access calculator commands from a command-line interface.
- **Undo and redo:** Restore previous calculator states and redo reverted actions.
- **Calculation history:** Review, clear, save, and load calculation history.
- **Persistent storage:** Store calculation records in CSV format, including operations, operands, results, and timestamps.
- **Configurable settings:** Customize precision, input limits, history size, file locations, and automatic saving through environment variables.
- **Precision:** Every result is rounded to the number of decimal places set in `CALCULATOR_PRECISION`.
- **Logging:** Record application activity and diagnostic information.
- **Error handling:** Validate inputs and results, and handle calculation errors with appropriate exceptions.
- **Automated testing:** Use pytest to verify application behavior and measure test coverage.
- **Continuous integration:** Run automated checks through GitHub Actions.

## Additional Features

- **Dynamic help:** Registers arithmetic operation classes using the `operation_help` decorator and automatically generates the operations help menu.
- **Color-coded output:** Uses Colorama to distinguish successful actions, errors, warnings, and informational messages in the CLI.
- **Command Design Pattern:** Encapsulates calculator management actions in dedicated command classes, separating command execution from the underlying calculator methods.

## Technologies

- Python
- Colorama
- pandas
- python-dotenv
- pytest and pytest-cov
- Git and GitHub
- GitHub Actions

## Project Structure

```text
PythonCalculatorMidtermProject/
├── .github/
│   └── workflows/               # GitHub Actions workflows
├── app/
│   ├── __init__.py               # Application package
│   ├── calculation.py            # Calculation model
│   ├── calculator.py              # Calculator logic and interactive CLI
│   ├── calculator_config.py       # Application configuration
│   ├── calculator_memento.py      # State snapshots for undo and redo
│   ├── color_coded.py             # Colorama output formatting helpers
│   ├── commands.py                # Command Design Pattern classes
│   ├── exceptions.py              # Custom application exceptions
│   ├── history.py                 # History observers and related behavior
│   ├── input_validators.py        # Input validation
│   ├── logger.py                  # Logging configuration and utilities
│   └── operations.py              # Arithmetic operations and dynamic help
├── tests/
│   ├── __init__.py                # Test package
│   ├── conftest.py                # Shared pytest fixtures
│   ├── test_calculation.py        # Calculation model tests
│   ├── test_calculator.py         # Calculator and CLI tests
│   ├── test_color.py              # Color formatting tests
│   ├── test_commands.py           # Command pattern tests
│   ├── test_config.py             # Configuration tests
│   ├── test_exceptions.py         # Exception tests
│   ├── test_history.py            # History tests
│   ├── test_logger.py             # Logging tests
│   ├── test_memento.py            # Memento pattern tests
│   ├── test_operations.py         # Arithmetic operation tests
│   └── test_validators.py         # Input validation tests
├── .env                           # Local environment configuration
├── .gitignore
├── main.py                        # Application entry point
├── readme.md                      # Project documentation
└── requirements.txt               # Project dependencies
```


## Prerequisites

- Python 3.11 or newer (the GitHub Actions workflow uses Python 3.13)
- Git
- A terminal or command prompt

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/rh480/PythonCalculatorMidtermProject.git
cd PythonCalculatorMidtermProject
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Or, using Command Prompt:

```cmd
.venv\Scripts\activate
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create or update the `.env` file in the project root:

```dotenv
CALCULATOR_LOG_DIR=logs
CALCULATOR_LOG_FILE=logs/calculator.log
CALCULATOR_HISTORY_DIR=history
CALCULATOR_HISTORY_FILE=history/calculator_history.csv

CALCULATOR_MAX_HISTORY_SIZE=100
CALCULATOR_AUTO_SAVE=true

CALCULATOR_PRECISION=10
CALCULATOR_MAX_INPUT_VALUE=1000000
CALCULATOR_DEFAULT_ENCODING=utf-8
```

These settings define logging and history file locations, the maximum history size, automatic saving, numerical precision, the maximum input value, and file encoding.

| Variable | Meaning | Built-in default |
|---|---|---|
| `CALCULATOR_LOG_DIR` | Directory for log files | `logs` |
| `CALCULATOR_LOG_FILE` | Log file path | `logs/calculator.log` |
| `CALCULATOR_HISTORY_DIR` | Directory for history files | `history` |
| `CALCULATOR_HISTORY_FILE` | CSV file used by `save`, `load`, and auto-save | `history/calculator_history.csv` |
| `CALCULATOR_MAX_HISTORY_SIZE` | Maximum number of history entries kept | `1000` |
| `CALCULATOR_AUTO_SAVE` | Save history after every calculation (`true` or `false`) | `true` |
| `CALCULATOR_PRECISION` | Decimal places kept in results (1 to 28) | `10` |
| `CALCULATOR_MAX_INPUT_VALUE` | Largest absolute value accepted as input | `1e999` |
| `CALCULATOR_DEFAULT_ENCODING` | Encoding for log and history files | `utf-8` |

The values are loaded with `python-dotenv` when the application starts. A real environment variable takes priority over the `.env` file, and any missing setting uses its built-in default. All values are validated at startup: if one is invalid (for example a precision of 0 or 29), the application prints `Configuration error: <reason>` and exits.

To change a setting for one run without editing `.env`:

```bash
CALCULATOR_PRECISION=2 python main.py            # macOS / Linux
```

```powershell
$env:CALCULATOR_PRECISION=2; python main.py      # Windows PowerShell
```

Keep local secrets and environment-specific settings out of version control.

## Running the Application

From the project root, run:

```bash
python main.py
```

The calculator starts in interactive command-line mode.

## Calculator Operations

The calculator supports the following operations:

| Operation | Description |
|---|---|
| Addition | Adds two numbers |
| Subtraction | Subtracts the second number from the first |
| Multiplication | Multiplies two numbers |
| Division | Divides the first number by the second |
| Power | Raises a number to a specified power |
| Root | Calculates a root |
| Modulus | Returns the remainder |
| Integer division | Returns the integer-division result |
| Percentage | Calculates the first value as a percentage of the second |
| Absolute difference | Returns the absolute difference between two values |

Division and other operations are subject to the application's input validation and error-handling rules.

### Precision

Every result is rounded half-up to `CALCULATOR_PRECISION` decimal places. Whole numbers are shown without a fractional part, and trailing zeros are removed. For example, `divide 1 3` gives `0.3333333333` with the default precision of 10 and `0.33` with a precision of 2. Only the result is rounded; the operands are stored as entered.

### Validation and error handling

- **Inputs** must be numbers. Text, empty input, `nan`, `inf`, and `-inf` are rejected, as are values larger than `CALCULATOR_MAX_INPUT_VALUE`.
- **Operations** reject invalid cases with a clear message: division, modulus, integer division, and percentage by zero; a root degree of zero; an even or fractional root of a negative number; and zero raised to zero or a negative power.
- **Results** must be finite numbers. A result that is not (including a Decimal overflow) is rejected, is not added to the history, and is logged as a warning.
- **Saved history** is validated when it is loaded. A CSV with missing columns, non-numeric or non-finite values, or an invalid timestamp is reported as an error and leaves the current history unchanged.

Errors are shown at the prompt and the calculator keeps running.

## CLI Commands

Enter commands in the interactive calculator to perform calculations or manage calculation history.

| Command | Purpose |
|---|---|
| `help` | Display registered arithmetic operations and available commands |
| `history` | View recorded calculations |
| `clear` | Clear calculation history |
| `undo` | Undo the most recent supported action |
| `redo` | Restore an undone action |
| `save` | Save calculation history to persistent storage |
| `load` | Load previously saved calculation history |
| `exit` | Exit the application |

Arithmetic operations are entered by name (for example `add`, `subtract`, `power`, `root`, `int_divide`, `percent`, or `abs_diff`). The calculator then asks for each number.

Example:

<pre>
<b>Enter an operation or command: add</b>
<b>Selected operation: add</b>
Enter first number: 5
Enter second number: 3

Result: 8
</pre>

Use `help` within the application to view the registered operations and their descriptions.

## Design Patterns

The project uses design patterns to organize application responsibilities and improve maintainability.

- **Factory Pattern:** `OperationFactory` creates or selects supported arithmetic operations based on user input.
- **Memento Pattern:** Preserves calculator state to support undo and redo functionality.
- **Observer Pattern:** Uses observers such as `LoggingObserver` and `AutoSaveObserver` to respond to calculator events.
- **Command Pattern:** Encapsulates management actions in command classes, separating the request to perform an action from the calculator methods that carry it out.
- **Decorator-based registration:** Uses the `operation_help` decorator to register arithmetic operation classes dynamically, allowing the help menu to discover registered operations.

## Calculation History and Logging

Calculation history can be persisted to CSV files for later retrieval. The configured history path determines where saved records are stored. Automatic saving can be controlled through the `.env` configuration. The CSV file has these columns: `operation`, `operand1`, `operand2`, `result`, and `timestamp`. Saved history is loaded again when the application starts.

Logging records application events and can help diagnose errors. Log file locations and encoding are configurable. Calculations and history actions are logged at `INFO`, rejected input and results at `WARNING`, and failures such as a history file that cannot be saved or loaded at `ERROR`. Example entries:

```text
2026-11-20 20:56:16,689 - INFO - Calculation: Addition(5, 3) = 8
2026-11-20 20:56:17,032 - WARNING - Calculation rejected: Cannot calculate modulus with zero.
```

To move the log file, change `CALCULATOR_LOG_DIR` or `CALCULATOR_LOG_FILE` in `.env`.

Generated history and log files may be created when the application runs, depending on the configured settings.

## Running Tests

Run the complete test suite from the project root:

```bash
python -m pytest
```

To run tests with coverage:

```bash
python -m pytest --cov=app --cov-report=term-missing
```

To check against the 90% threshold used in CI:

```bash
python -m pytest --cov=app --cov-fail-under=90
```

To generate an HTML coverage report:

```bash
python -m pytest --cov=app --cov-report=html
```

The test suite includes coverage for:

- Arithmetic operations and calculation behavior
- CLI commands and user interaction
- Dynamic operation registration and help
- Color formatting
- Command pattern behavior
- Configuration and input validation
- Exceptions and error handling
- Calculation history, persistence, and observers
- Memento-based undo and redo
- Logging utilities

Run the coverage command to view the current test coverage percentage and identify lines that are not covered by tests. Lines that cannot be meaningfully tested, such as the bodies of abstract methods and the `if __name__ == "__main__":` guard, are marked with `# pragma: no cover`.

## Continuous Integration

The repository includes a GitHub Actions workflow in `.github/workflows/tests.yml`. It runs on every push and every pull request to `main`. It checks out the code, sets up Python 3.13, installs the packages in `requirements.txt` along with `pytest` and `pytest-cov`, and runs `pytest --cov=app --cov-fail-under=90`. The build fails if any test fails or if test coverage drops below 90%.

See the **Actions** tab in the repository for workflow runs and results.

## Future Improvements

Potential enhancements include improving the calculator’s overall interface by allowing users to customize output colors, text styles, layout, and display preferences. The CLI layout could be reorganized to make menus, commands, calculation results, and error messages easier to read and navigate. Additional improvements may include adding clearer prompts, expanding edge-case tests for arithmetic operations and history persistence, enhancing error handling, improving logging, and expanding documentation for individual modules and design patterns.
