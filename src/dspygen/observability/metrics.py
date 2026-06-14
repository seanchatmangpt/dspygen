"""Simple in-memory metrics — no external dependency required."""
import time
import functools
from threading import Lock

METRICS_REGISTRY: dict[str, object] = {}
_registry_lock = Lock()


class Counter:
    """Monotonically increasing counter."""

    def __init__(self, name: str) -> None:
        self.name = name
        self._value: float = 0.0
        self._lock = Lock()
        _register(name, self)

    def inc(self, amount: float = 1.0) -> None:
        with self._lock:
            self._value += amount

    @property
    def value(self) -> float:
        with self._lock:
            return self._value

    def reset(self) -> None:
        with self._lock:
            self._value = 0.0

    def to_dict(self) -> dict:
        return {"type": "counter", "name": self.name, "value": self.value}


class Gauge:
    """Settable / incrementable / decrementable gauge."""

    def __init__(self, name: str) -> None:
        self.name = name
        self._value: float = 0.0
        self._lock = Lock()
        _register(name, self)

    def set(self, v: float) -> None:
        with self._lock:
            self._value = v

    def inc(self, amount: float = 1.0) -> None:
        with self._lock:
            self._value += amount

    def dec(self, amount: float = 1.0) -> None:
        with self._lock:
            self._value -= amount

    @property
    def value(self) -> float:
        with self._lock:
            return self._value

    def to_dict(self) -> dict:
        return {"type": "gauge", "name": self.name, "value": self.value}


def _register(name: str, obj: object) -> None:
    with _registry_lock:
        METRICS_REGISTRY[name] = obj


def track_call(fn):
    """Decorator that tracks call count, error count, and average duration for a function."""
    call_counter = Counter(f"{fn.__module__}.{fn.__qualname__}.calls")
    error_counter = Counter(f"{fn.__module__}.{fn.__qualname__}.errors")
    duration_gauge = Gauge(f"{fn.__module__}.{fn.__qualname__}.avg_duration_ms")
    _total_duration: list[float] = [0.0]

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        call_counter.inc()
        start = time.perf_counter()
        try:
            result = fn(*args, **kwargs)
            return result
        except Exception:
            error_counter.inc()
            raise
        finally:
            elapsed_ms = (time.perf_counter() - start) * 1000
            _total_duration[0] += elapsed_ms
            duration_gauge.set(_total_duration[0] / call_counter.value)

    return wrapper


def get_all_metrics() -> dict:
    """Return all registered metrics as a JSON-serializable dict."""
    with _registry_lock:
        return {name: obj.to_dict() for name, obj in METRICS_REGISTRY.items()}
