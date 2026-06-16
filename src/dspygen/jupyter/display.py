"""DSPyGen Jupyter display helpers.

Works in both IPython/Jupyter environments and plain Python scripts.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# IPython availability guard
# ---------------------------------------------------------------------------

try:
    from IPython.display import HTML, JSON
    from IPython.display import display as _ip_display
    _IPYTHON_AVAILABLE = True
except ImportError:
    _IPYTHON_AVAILABLE = False

    def _ip_display(*args, **kwargs):  # type: ignore[misc]
        pass


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _is_jsonable(obj: Any) -> bool:
    """Return True if *obj* can be JSON-serialised."""
    import json
    try:
        json.dumps(obj)
        return True
    except (TypeError, ValueError):
        return False


def _obj_to_dict(obj: Any) -> dict | None:
    """Convert common result types to a plain dict for display."""
    if isinstance(obj, dict):
        return obj
    if hasattr(obj, "__dict__"):
        return {k: v for k, v in obj.__dict__.items() if not k.startswith("_")}
    if hasattr(obj, "_asdict"):  # namedtuple / dataclass
        return obj._asdict()
    return None


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def display_module_output(output: Any) -> None:
    """
    Render the output of a DSPyGen module call in the best available format.

    Priority order:
      1. DSPy Prediction / typed dict  →  IPython JSON widget
      2. Object with __dict__           →  IPython JSON widget
      3. Plain string                   →  IPython HTML <pre>
      4. Fallback                       →  print()

    In non-IPython environments, always falls back to print().
    """
    if output is None:
        print("[dspygen] Module returned None.")
        return

    if not _IPYTHON_AVAILABLE:
        print(output)
        return

    # Try JSON display first (works well for dspy.Prediction and dicts)
    as_dict = _obj_to_dict(output)
    if as_dict is not None and _is_jsonable(as_dict):
        try:
            _ip_display(JSON(as_dict))
            return
        except Exception:
            pass

    # String / fallback
    if isinstance(output, str):
        _ip_display(HTML(f"<pre style='white-space:pre-wrap'>{_escape_html(output)}</pre>"))
        return

    # Last resort
    _ip_display(HTML(f"<pre style='white-space:pre-wrap'>{_escape_html(str(output))}</pre>"))


def display_pipeline_result(results: list[dict[str, Any]]) -> None:
    """
    Render a list of pipeline step results as a formatted table.

    Each element of *results* should be a dict with at least:
      - ``step``   — step name
      - ``module`` — module name
      - ``result`` — the step output (or None)
      - ``error``  — (optional) error message string
    """
    if not results:
        print("[dspygen_pipeline] No results to display.")
        return

    if not _IPYTHON_AVAILABLE:
        _print_pipeline_table(results)
        return

    try:
        rows_html = ""
        for item in results:
            step = _escape_html(str(item.get("step", "")))
            module = _escape_html(str(item.get("module", "")))
            result = item.get("result")
            error = item.get("error")

            if error:
                status_cell = f"<td style='color:red;padding:4px 12px'>ERROR: {_escape_html(error[:80])}</td>"
            else:
                preview = _escape_html(str(result)[:120]) if result is not None else "<em>None</em>"
                status_cell = f"<td style='padding:4px 12px'>{preview}</td>"

            rows_html += (
                f"<tr>"
                f"<td style='padding:4px 12px'><strong>{step}</strong></td>"
                f"<td style='padding:4px 12px'><code>{module}</code></td>"
                f"{status_cell}"
                f"</tr>"
            )

        html = (
            "<h4>Pipeline Results</h4>"
            "<table style='border-collapse:collapse;width:100%'>"
            "<thead>"
            "<tr style='background:#f0f0f0'>"
            "<th style='padding:4px 12px;text-align:left'>Step</th>"
            "<th style='padding:4px 12px;text-align:left'>Module</th>"
            "<th style='padding:4px 12px;text-align:left'>Output preview</th>"
            "</tr>"
            "</thead>"
            f"<tbody>{rows_html}</tbody>"
            "</table>"
        )
        _ip_display(HTML(html))
    except Exception:
        _print_pipeline_table(results)


def display_agent_state(state: Any) -> None:
    """
    Render an agent state object or dict.

    Supports:
      - Plain dicts
      - Objects with a ``state`` attribute (dict or object)
      - Objects with ``__dict__``
      - Fallback to str()
    """
    if state is None:
        print("[dspygen] Agent state is None.")
        return

    # Unwrap common wrapper patterns
    if hasattr(state, "state"):
        state = state.state

    as_dict = _obj_to_dict(state)

    if not _IPYTHON_AVAILABLE:
        if as_dict is not None:
            for k, v in as_dict.items():
                print(f"  {k}: {v}")
        else:
            print(state)
        return

    if as_dict is not None and _is_jsonable(as_dict):
        try:
            _ip_display(JSON(as_dict))
            return
        except Exception:
            pass

    _ip_display(HTML(f"<pre style='white-space:pre-wrap'>{_escape_html(str(state))}</pre>"))


# ---------------------------------------------------------------------------
# Private plain-text fallbacks
# ---------------------------------------------------------------------------

def _print_pipeline_table(results: list[dict[str, Any]]) -> None:
    col_w = 20
    print(f"\n{'Step':<{col_w}} {'Module':<{col_w}} Output preview")
    print("-" * 80)
    for item in results:
        step = str(item.get("step", ""))[:col_w - 1]
        module = str(item.get("module", ""))[:col_w - 1]
        error = item.get("error")
        if error:
            preview = f"ERROR: {error[:40]}"
        else:
            result = item.get("result")
            preview = str(result)[:40] if result is not None else "None"
        print(f"{step:<{col_w}} {module:<{col_w}} {preview}")


def _escape_html(text: str) -> str:
    """Minimal HTML escaping."""
    return (
        text
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
