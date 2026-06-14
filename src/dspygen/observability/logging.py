"""Structured logging setup using loguru."""
from loguru import logger
import sys
import os
import time
import functools


def configure_logging(level: str = "INFO", json: bool = False, file: str | None = None) -> None:
    """Configure loguru with stderr output, optional JSON format, and optional file output.

    Environment variable overrides:
      DSPYGEN_LOG_LEVEL  — log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
      DSPYGEN_LOG_FORMAT — set to "json" to enable JSON output
      DSPYGEN_LOG_FILE   — path to write logs to a file
    """
    effective_level = os.environ.get("DSPYGEN_LOG_LEVEL", level).upper()
    use_json = json or os.environ.get("DSPYGEN_LOG_FORMAT", "").lower() == "json"
    log_file = file or os.environ.get("DSPYGEN_LOG_FILE")

    # Remove all default handlers
    logger.remove()

    if use_json:
        fmt = "{time:YYYY-MM-DDTHH:mm:ss.SSSZZ} | {level} | {name} | {message} | {extra}"
        logger.add(sys.stderr, level=effective_level, format=fmt, serialize=True, colorize=False)
    else:
        fmt = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{extra[name]}</cyan> | "
            "<level>{message}</level>"
        )
        logger.add(sys.stderr, level=effective_level, format=fmt, colorize=True)

    if log_file:
        logger.add(
            log_file,
            level=effective_level,
            serialize=use_json,
            rotation="10 MB",
            retention="7 days",
        )


def get_logger(name: str):
    """Return a bound loguru logger with a name context field."""
    return logger.bind(name=name)


def log_call(fn):
    """Decorator that logs function entry/exit with timing."""
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        bound = logger.bind(name=fn.__module__)
        bound.debug(f"Entering {fn.__qualname__}")
        start = time.perf_counter()
        try:
            result = fn(*args, **kwargs)
            elapsed_ms = (time.perf_counter() - start) * 1000
            bound.debug(f"Exiting  {fn.__qualname__} [{elapsed_ms:.1f}ms]")
            return result
        except Exception as exc:
            elapsed_ms = (time.perf_counter() - start) * 1000
            bound.error(f"Exception in {fn.__qualname__} [{elapsed_ms:.1f}ms]: {exc}")
            raise

    return wrapper


# Auto-configure on import when DSPYGEN_LOG_LEVEL is set
if os.environ.get("DSPYGEN_LOG_LEVEL"):
    configure_logging()
