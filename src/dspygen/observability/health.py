"""Health check system for dspygen."""
import os
import time
from collections.abc import Callable
from dataclasses import dataclass, field


@dataclass
class HealthStatus:
    """Result of a single health check execution."""
    name: str
    status: str          # "ok" | "warn" | "fail"
    message: str
    duration_ms: float


@dataclass
class HealthCheck:
    """A named health check that can be registered globally."""
    name: str
    check_fn: Callable[[], bool]
    critical: bool = True


REGISTRY: list[HealthCheck] = []


def register_check(name: str, fn: Callable[[], bool], critical: bool = True) -> None:
    """Add a health check to the global registry."""
    REGISTRY.append(HealthCheck(name=name, check_fn=fn, critical=critical))


def check_all() -> list[HealthStatus]:
    """Run all registered health checks and return their statuses."""
    results: list[HealthStatus] = []
    for hc in REGISTRY:
        start = time.perf_counter()
        try:
            ok = hc.check_fn()
            elapsed_ms = (time.perf_counter() - start) * 1000
            status = "ok" if ok else ("fail" if hc.critical else "warn")
            message = "ok" if ok else ("check failed" if hc.critical else "check returned False")
        except Exception as exc:
            elapsed_ms = (time.perf_counter() - start) * 1000
            status = "fail" if hc.critical else "warn"
            message = str(exc)
        results.append(HealthStatus(name=hc.name, status=status, message=message, duration_ms=elapsed_ms))
    return results


# ---------------------------------------------------------------------------
# Pre-registered built-in checks
# ---------------------------------------------------------------------------

def _check_dspy_importable() -> bool:
    import importlib
    return importlib.util.find_spec("dspy") is not None


def _check_mcp_importable() -> bool:
    import importlib
    return importlib.util.find_spec("mcp") is not None


def _check_lsp_importable() -> bool:
    import importlib
    return importlib.util.find_spec("pygls") is not None


def _check_openai_key_set() -> bool:
    return bool(os.environ.get("OPENAI_API_KEY"))


def _check_config_file_exists() -> bool:
    return os.path.exists(".dspygen.env")


register_check("dspy_importable", _check_dspy_importable, critical=True)
register_check("mcp_importable", _check_mcp_importable, critical=True)
register_check("lsp_importable", _check_lsp_importable, critical=True)
register_check("openai_key_set", _check_openai_key_set, critical=False)
register_check("config_file_exists", _check_config_file_exists, critical=False)
