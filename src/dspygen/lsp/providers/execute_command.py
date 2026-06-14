"""
Execute command provider for the dspygen LSP server.

Handles workspace/executeCommand.

Registered commands:
- dspygen.runModule         — run the module under cursor via CLI subprocess
- dspygen.generateModule    — produce a new file with a module template
- dspygen.validateSignature — validate the signature string under cursor
- dspygen.initDspy          — insert init_dspy() at top of current file
- dspygen.formatSignature   — normalise the signature string under cursor
- dspygen.showModuleInfo    — show module info as a log-level notification
"""

from __future__ import annotations

import re
import subprocess
import sys
from typing import TYPE_CHECKING, Any

from loguru import logger
from lsprotocol import types as lsp_types

if TYPE_CHECKING:
    from pygls.lsp.server import LanguageServer


# ---------------------------------------------------------------------------
# Command constants
# ---------------------------------------------------------------------------

CMD_RUN_MODULE = "dspygen.runModule"
CMD_GENERATE_MODULE = "dspygen.generateModule"
CMD_VALIDATE_SIGNATURE = "dspygen.validateSignature"
CMD_INIT_DSPY = "dspygen.initDspy"
CMD_FORMAT_SIGNATURE = "dspygen.formatSignature"
CMD_SHOW_MODULE_INFO = "dspygen.showModuleInfo"

ALL_COMMANDS: list[str] = [
    CMD_RUN_MODULE,
    CMD_GENERATE_MODULE,
    CMD_VALIDATE_SIGNATURE,
    CMD_INIT_DSPY,
    CMD_FORMAT_SIGNATURE,
    CMD_SHOW_MODULE_INFO,
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_SIG_LITERAL_RE = re.compile(r"""(["'])([\w\s,]+->\s*[\w\s,]+)\1""")
_IDENT_RE = re.compile(r"\b([A-Za-z_]\w*)\b")


def _get_source_and_position(
    server: "LanguageServer",
    args: list[Any] | None,
) -> tuple[str | None, str | None, lsp_types.Position | None]:
    """Extract (uri, source, position) from command arguments."""
    if not args or len(args) < 1:
        return None, None, None
    uri = args[0] if isinstance(args[0], str) else None
    if not uri:
        return None, None, None
    try:
        document = server.workspace.get_text_document(uri)
        source = document.source
    except Exception:  # noqa: BLE001
        source = None
    position: lsp_types.Position | None = None
    if len(args) >= 3 and isinstance(args[1], int) and isinstance(args[2], int):
        position = lsp_types.Position(line=args[1], character=args[2])
    return uri, source, position


def _word_at(source: str, position: lsp_types.Position) -> str:
    lines = source.splitlines()
    if position.line >= len(lines):
        return ""
    line = lines[position.line]
    col = position.character
    for m in _IDENT_RE.finditer(line):
        if m.start() <= col <= m.end():
            return m.group(1)
    return ""


def _sig_at(source: str, position: lsp_types.Position) -> str | None:
    lines = source.splitlines()
    if position.line >= len(lines):
        return None
    line = lines[position.line]
    for m in _SIG_LITERAL_RE.finditer(line):
        if m.start() <= position.character <= m.end():
            return m.group(2).strip()
    return None


def _format_sig(sig: str) -> str:
    """Normalise a DSPy signature string: trim spaces, single space around ->."""
    if "->" not in sig:
        return sig.strip()
    parts = sig.split("->", 1)
    inputs = ", ".join(f.strip() for f in parts[0].split(",") if f.strip())
    outputs = ", ".join(f.strip() for f in parts[1].split(",") if f.strip())
    return f"{inputs} -> {outputs}"


_MODULE_TEMPLATE = '''\
"""
{name} — dspygen module.
"""
from dspygen.utils.dspy_tools import init_dspy
import dspy


class {name}(dspy.Module):
    """TODO: describe what this module does."""

    def __init__(self):
        super().__init__()
        self.predict = dspy.Predict("input -> output")

    def forward(self, input: str) -> dspy.Prediction:
        return self.predict(input=input)


if __name__ == "__main__":
    init_dspy()
    mod = {name}()
    result = mod.forward(input="hello world")
    print(result)
'''


# ---------------------------------------------------------------------------
# Command handlers
# ---------------------------------------------------------------------------


def _handle_run_module(server: "LanguageServer", args: list[Any] | None) -> str:
    """Run module via dspygen CLI.  Args: [uri, line, col]."""
    uri, source, position = _get_source_and_position(server, args)
    if not source or not position:
        return "No document or position provided."
    word = _word_at(source, position)
    if not word:
        return "No identifier under cursor."
    try:
        result = subprocess.run(
            [sys.executable, "-m", "dspygen", "run", word],
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = result.stdout or result.stderr or "No output."
        logger.info(f"runModule({word}): {output[:200]}")
        return output
    except Exception as exc:  # noqa: BLE001
        logger.exception(f"runModule error: {exc}")
        return f"Error: {exc}"


def _handle_generate_module(server: "LanguageServer", args: list[Any] | None) -> str:
    """Generate a new module template.  Args: [name_or_uri]."""
    name = (args[0] if args else None) or "NewModule"
    if name.startswith("file://"):
        name = "NewModule"
    code = _MODULE_TEMPLATE.format(name=name)
    logger.info(f"generateModule: produced template for {name}")
    return code


def _handle_validate_signature(server: "LanguageServer", args: list[Any] | None) -> str:
    """Validate signature under cursor.  Args: [uri, line, col]."""
    uri, source, position = _get_source_and_position(server, args)
    if not source or not position:
        # Try direct signature string as first arg
        if args and isinstance(args[0], str) and "->" in args[0]:
            sig = args[0]
        else:
            return "Provide a URI+position or a signature string."
    else:
        sig = _sig_at(source, position)
        if not sig:
            return "No signature string found under cursor."

    from ..analysis.signature_parser import validate_signature  # noqa: PLC0415

    errors = validate_signature(sig)
    if errors:
        return "Signature errors:\n" + "\n".join(f"  - {e}" for e in errors)
    return f"Signature '{sig}' is valid."


def _handle_init_dspy(server: "LanguageServer", args: list[Any] | None) -> dict[str, Any] | str:
    """Insert init_dspy() into the current file.  Args: [uri]."""
    uri = args[0] if args else None
    if not uri:
        return "No URI provided."
    try:
        document = server.workspace.get_text_document(uri)
        source = document.source
    except Exception as exc:  # noqa: BLE001
        return f"Could not open document: {exc}"

    lines = source.splitlines()
    last_import = -1
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("import ") or stripped.startswith("from "):
            last_import = i

    insert_line = last_import + 1
    insert_pos = lsp_types.Position(line=insert_line, character=0)
    edit = lsp_types.TextEdit(
        range=lsp_types.Range(start=insert_pos, end=insert_pos),
        new_text="\ninit_dspy()\n",
    )
    workspace_edit = lsp_types.WorkspaceEdit(changes={uri: [edit]})
    # Return as dict so pygls can serialise it back to the client
    return {
        "applied": True,
        "message": "init_dspy() inserted.",
        "workspaceEdit": workspace_edit,
    }


def _handle_format_signature(server: "LanguageServer", args: list[Any] | None) -> dict[str, Any] | str:
    """Normalise the signature string under cursor.  Args: [uri, line, col]."""
    uri, source, position = _get_source_and_position(server, args)
    if not source or not position:
        if args and isinstance(args[0], str) and "->" in args[0]:
            return _format_sig(args[0])
        return "No document/position or signature string provided."

    lines = source.splitlines()
    if position.line >= len(lines):
        return "Position out of range."
    line_text = lines[position.line]

    for m in _SIG_LITERAL_RE.finditer(line_text):
        if m.start() <= position.character <= m.end():
            old_sig = m.group(2)
            new_sig = _format_sig(old_sig)
            edit = lsp_types.TextEdit(
                range=lsp_types.Range(
                    start=lsp_types.Position(line=position.line, character=m.start(2)),
                    end=lsp_types.Position(line=position.line, character=m.end(2)),
                ),
                new_text=new_sig,
            )
            return {
                "applied": True,
                "old": old_sig,
                "new": new_sig,
                "workspaceEdit": lsp_types.WorkspaceEdit(changes={uri: [edit]}),
            }

    return "No signature literal under cursor."


def _handle_show_module_info(server: "LanguageServer", args: list[Any] | None) -> str:
    """Show hover-style module info as a string.  Args: [uri, line, col]."""
    from .._state import module_index  # noqa: PLC0415

    uri, source, position = _get_source_and_position(server, args)
    if not source or not position:
        return "No document or position provided."
    word = _word_at(source, position)
    if not word:
        return "No identifier under cursor."
    info = module_index.get_by_name(word)
    if not info:
        return f"No dspygen module info found for '{word}'."

    parts = [f"Module: {info.name}", f"File: {info.file_path}"]
    if info.docstring:
        parts.append(f"Docstring: {info.docstring}")
    if info.signature_string:
        parts.append(f"Signature: {info.signature_string}")
    if info.input_fields:
        parts.append(f"Inputs: {', '.join(info.input_fields)}")
    if info.output_fields:
        parts.append(f"Outputs: {', '.join(info.output_fields)}")
    result = "\n".join(parts)
    logger.info(f"showModuleInfo: {result}")
    return result


# ---------------------------------------------------------------------------
# Provider registration
# ---------------------------------------------------------------------------


def register_execute_command(server: "LanguageServer") -> None:
    """Register the workspace/executeCommand handler on *server*."""

    @server.feature(
        lsp_types.WORKSPACE_EXECUTE_COMMAND,
        lsp_types.ExecuteCommandOptions(commands=ALL_COMMANDS),
    )
    def on_execute_command(
        params: lsp_types.ExecuteCommandParams,
    ) -> Any:
        command = params.command
        args: list[Any] = list(params.arguments or [])
        logger.info(f"executeCommand: {command} args={args}")
        try:
            if command == CMD_RUN_MODULE:
                return _handle_run_module(server, args)
            elif command == CMD_GENERATE_MODULE:
                return _handle_generate_module(server, args)
            elif command == CMD_VALIDATE_SIGNATURE:
                return _handle_validate_signature(server, args)
            elif command == CMD_INIT_DSPY:
                return _handle_init_dspy(server, args)
            elif command == CMD_FORMAT_SIGNATURE:
                return _handle_format_signature(server, args)
            elif command == CMD_SHOW_MODULE_INFO:
                return _handle_show_module_info(server, args)
            else:
                logger.warning(f"executeCommand: unknown command '{command}'")
                return f"Unknown command: {command}"
        except Exception as exc:  # noqa: BLE001
            logger.exception(f"executeCommand({command}) error: {exc}")
            return f"Error executing {command}: {exc}"
