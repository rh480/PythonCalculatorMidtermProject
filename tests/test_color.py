
from colorama import Fore, Style

from app.color_coded import success, error, warning, info, prompt


def test_success_formats_message():
    assert success("Result: 5") == f"{Fore.GREEN}Result: 5"


def test_error_formats_message():
    assert error("Invalid input") == f"{Fore.RED}Invalid input"


def test_warning_formats_message():
    assert warning("Nothing to undo") == f"{Fore.YELLOW}Nothing to undo"


def test_info_formats_message():
    assert info("Available operations") == f"{Fore.CYAN}Available operations"


def test_prompt_formats_message():
    assert prompt("Enter a calculation: ") == (
        f"{Style.BRIGHT}Enter a calculation: "
    )
