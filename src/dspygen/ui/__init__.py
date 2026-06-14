"""dspygen terminal UI utilities using rich."""
from dspygen.ui.console import (
    console,
    print_success,
    print_error,
    print_warning,
    print_info,
    print_table,
    print_json,
    print_code,
    spinner,
    RICH_AVAILABLE,
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
