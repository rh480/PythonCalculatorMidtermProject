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
- **Logging:** Record application activity and diagnostic information.
- **Error handling:** Validate inputs and handle calculation errors with appropriate exceptions.
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

- Python 3.10 or a compatible version supported by the installed dependencies
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

Ensure the configuration values match the defaults and validation rules implemented in `app/calculator_config.py`. Keep local secrets and environment-specific settings out of version control.

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

Arithmetic operations use the format `operation number1 number2`.

Example:

```text
add 5 3
Result: 8
```

Use `help` within the application to view the registered operations and their descriptions.

## Design Patterns

The project uses design patterns to organize application responsibilities and improve maintainability.

- **Factory Pattern:** `OperationFactory` creates or selects supported arithmetic operations based on user input.
- **Memento Pattern:** Preserves calculator state to support undo and redo functionality.
- **Observer Pattern:** Uses observers such as `LoggingObserver` and `AutoSaveObserver` to respond to calculator events.
- **Command Pattern:** Encapsulates management actions in command classes, separating the request to perform an action from the calculator methods that carry it out.
- **Decorator-based registration:** Uses the `operation_help` decorator to register arithmetic operation classes dynamically, allowing the help menu to discover registered operations.

## Calculation History and Logging

Calculation history can be persisted to CSV files for later retrieval. The configured history path determines where saved records are stored. Automatic saving can be controlled through the `.env` configuration.

Logging records application events and can help diagnose errors. Log file locations and encoding are configurable.

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

Run the coverage command to view the current test coverage percentage and identify lines that are not covered by tests.

## Continuous Integration

The repository includes a GitHub Actions workflow under `.github/workflows/`. The workflow can automatically run configured checks when code is pushed or a pull request is opened.

See the **Actions** tab in the repository for workflow runs and results.

## Future Improvements

Potential enhancements include improving the calculator’s overall interface by allowing users to customize output colors, text styles, layout, and display preferences. The CLI layout could be reorganized to make menus, commands, calculation results, and error messages easier to read and navigate. Additional improvements may include adding clearer prompts, expanding edge-case tests for arithmetic operations and history persistence, enhancing error handling, improving logging, and expanding documentation for individual modules and design patterns.
