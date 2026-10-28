
"""
Color helpers for the REPL.

All color choices live here, so changing the look of the app means
editing one file instead of every print statement.
"""

from colorama import Fore, Style, init

# Automatically reset colors after each print.
# Also supports ANSI colors in Windows terminals.
init(autoreset=True)


def success(text: str) -> str:
    """Green: a calculation result or a confirmed action."""
    return f"{Fore.GREEN}{text}"


def error(text: str) -> str:
    """Red: something failed, such as invalid input."""
    return f"{Fore.RED}{text}"


def warning(text: str) -> str:
    """Yellow: an action could not be completed."""
    return f"{Fore.YELLOW}{text}"


def info(text: str) -> str:
    """Cyan: headings, help text, and general information."""
    return f"{Fore.CYAN}{text}"


def prompt(text: str) -> str:
    """Bright text for input prompts."""
    return f"{Style.BRIGHT}{text}"
