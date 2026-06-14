"""
Formatting provider for the dspygen LSP server.

Handles textDocument/formatting.

Formatter selection order:
1. ruff format  (preferred — fast, opinionated)
2. black        (fallback)
3. isort        (import-only sort fallback)

Returns list[TextEdit] with a single whole-document replacement edit if the
formatted content differs from the original.  Returns empty list on failure.
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

from loguru import logger
from lsprotocol import types as lsp_types

if TYPE_CHECKING:
    from pygls.lsp.server import LanguageServer


# ---------------------------------------------------------------------------
# Formatter helpers
# ---------------------------------------------------------------------------


def _count_lines(text: str) -> int:
    return text.count("\n") + (1 if text and not text.endswith("\n") else 0)


def _whole_document_edit(original: str, formatted: str) -> list[lsp_types.TextEdit]:
    """Return a single TextEdit replacing the whole document."""
    if original == formatted:
        return []
    line_count = _count_lines(original)
    last_line = original.splitlines()[-1] if original.splitlines() else ""
    return [
        lsp_types.TextEdit(
            range=lsp_types.Range(
                start=lsp_types.Position(line=0, character=0),
                end=lsp_types.Position(line=line_count, character=len(last_line)),
            ),
            new_text=formatted,
        )
    ]


def _run_formatter(cmd: list[str], source: str, suffix: str = ".py") -> str | None:
    """
    Write *source* to a temp file, run *cmd* on it, and return the formatted
    content.  Returns None on any error.
    """
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=suffix,
            encoding="utf-8",
            delete=False,
        ) as f:
            f.write(source)
            tmp_path = f.name

        full_cmd = cmd + [tmp_path]
        result = subprocess.run(
            full_cmd,
            capture_output=True,
            timeout=15,
        )
        if result.returncode != 0:
            logger.debug(
                f"formatting: {cmd[0]} exited {result.returncode}: "
                f"{result.stderr.decode(errors='replace')}"
            )
            return None
        return Path(tmp_path).read_text(encoding="utf-8")
    except Exception as exc:  # noqa: BLE001
        logger.debug(f"formatting: {cmd[0]} error: {exc}")
        return None
    finally:
        try:
            Path(tmp_path).unlink(missing_ok=True)
        except Exception:  # noqa: BLE001
            pass


def _format_source(source: str) -> str:
    """Return formatted source, trying ruff → black → isort in order."""
    # 1. ruff format
    if shutil.which("ruff"):
        formatted = _run_formatter(["ruff", "format", "--quiet"], source)
        if formatted is not None:
            logger.debug("formatting: used ruff")
            return formatted

    # 2. black
    if shutil.which("black"):
        formatted = _run_formatter(["black", "--quiet", "-"], source)
        # black reads from stdin when arg is '-'
        if formatted is None:
            # Try via temp file
            formatted = _run_formatter(["black", "--quiet"], source)
        if formatted is not None:
            logger.debug("formatting: used black")
            return formatted

    # 3. isort (import-only sort)
    if shutil.which("isort"):
        formatted = _run_formatter(["isort", "--quiet"], source)
        if formatted is not None:
            logger.debug("formatting: used isort")
            return formatted

    # No formatter available
    logger.debug("formatting: no formatter available, returning original")
    return source


# ---------------------------------------------------------------------------
# Provider registration
# ---------------------------------------------------------------------------


def register_formatting(server: "LanguageServer") -> None:
    """Register the textDocument/formatting handler on *server*."""

    @server.feature(lsp_types.TEXT_DOCUMENT_FORMATTING)
    def on_formatting(
        params: lsp_types.DocumentFormattingParams,
    ) -> list[lsp_types.TextEdit] | None:
        try:
            uri = params.text_document.uri
            document = server.workspace.get_text_document(uri)
            source = document.source
            formatted = _format_source(source)
            return _whole_document_edit(source, formatted)
        except Exception as exc:  # noqa: BLE001
            logger.exception(f"formatting handler error: {exc}")
            return []
