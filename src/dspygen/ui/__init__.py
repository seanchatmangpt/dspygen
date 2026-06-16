"""dspygen terminal UI utilities using rich."""
from dspygen.ui.console import (
    RICH_AVAILABLE,
    console,
    print_code,
    print_error,
    print_info,
    print_json,
    print_success,
    print_table,
    print_warning,
    spinner,
)
from dspygen.ui.errors import (
    DspygenError,
    LMNotConfiguredError,
    ModuleNotFoundError,
    format_error,
    handle_error,
)

__all__ = [
    "console",
    "print_success",
    "print_error",
    "print_warning",
    "print_info",
    "print_table",
    "print_json",
    "print_code",
    "spinner",
    "RICH_AVAILABLE",
    "DspygenError",
    "LMNotConfiguredError",
    "ModuleNotFoundError",
    "format_error",
    "handle_error",
]
