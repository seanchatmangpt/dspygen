ADR-0003: Use pygls for the Language Server
============================================

:Status: Accepted
:Date: 2024-09-14
:Deciders: Sean Chatman

Context
-------

Providing IDE support (completions, diagnostics, hover) requires implementing the Language Server Protocol (LSP). Options: pygls, custom asyncio server, or no LSP.

Decision
--------

Use **pygls** (Python Generic Language Server) with **lsprotocol** for type-safe LSP message handling.

Rationale
---------

- pygls handles all LSP transport/protocol boilerplate
- lsprotocol provides dataclasses for every LSP type — no manual JSON serialization
- Supports all 14+ capabilities needed (completion, hover, diagnostics, etc.)
- Used by production language servers (pylsp, ruff-lsp)

Consequences
------------

- ``dspygen-lsp`` script entry point runs the LSP server via stdio
- All analysis is AST-based (no LLM calls) for sub-50ms response times
- LSP logs go to ``~/.cache/dspygen/lsp.log`` (stdout is the protocol channel)
- VS Code extension manages the LSP client lifecycle
