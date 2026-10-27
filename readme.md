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

## Technologies

- Python
- pytest and pytest-cov
- pandas
- python-dotenv
- Git and GitHub
- GitHub Actions

## Project Structure

```text
PythonCalculatorMidtermProject/
├── .github/
│   └── workflows/       # GitHub Actions workflows
├── app/
│   ├── calculator.py    # Calculator logic and CLI
│   ├── calculator_config.py
│   ├── history.py       # Calculation history and persistence
│   ├── operations.py    # Arithmetic operations
│   └── logger.py        # Logging utilities
├── tests/               # Automated tests
├── .env                 # Local configuration
├── .gitignore
├── main.py              # Application entry point
├── readme.md
└── requirements.txt
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

The interactive interface supports commands for calculator operations and, where implemented, the following management actions:

| Command | Purpose |
|---|---|
| `help` | Display usage information |
| `history` | View recorded calculations |
| `clear` | Clear calculation history |
| `undo` | Undo the most recent supported action |
| `redo` | Redo an undone action |
| `save` | Save calculation history |
| `load` | Load saved calculation history |
| `exit` | Exit the application |

Use the application's built-in help to confirm the exact command syntax and arguments.

## Design Patterns

The project applies design patterns to organize responsibilities and improve maintainability.

- **Factory Pattern:** Provides a structured way to create or select supported arithmetic operations.
- **Memento Pattern:** Supports undo and redo by preserving and restoring calculator state.
- **Observer Pattern:** Allows components such as logging and automatic history saving to respond to calculator events.
- **Command Pattern or other optional enhancement:** Document this only if the corresponding implementation is included in the current codebase.

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

Open `htmlcov/index.html` in a browser to inspect line-by-line coverage.

Tests should cover arithmetic operations, input validation, exception handling, undo and redo, history persistence, configuration, and observer behavior.

## Continuous Integration

The repository includes a GitHub Actions workflow under `.github/workflows/`. The workflow can automatically run configured checks when code is pushed or a pull request is opened.

See the **Actions** tab in the repository for workflow runs and results.

## Future Improvements

Potential enhancements include additional edge-case tests, improved CLI usability, more detailed logging, and expanded documentation for individual modules.

## Author

**Rashmi Hazarika**

GitHub: [rh480](https://github.com/rh480)

## License

No license has been specified. All rights are reserved by default unless a license is added to the repository.