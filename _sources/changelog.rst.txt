Changelog
=========

All notable changes to DSPyGen are documented in this file.  The format follows
`Keep a Changelog <https://keepachangelog.com/en/1.1.0/>`_ and the project
adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

.. contents:: Releases
   :local:
   :depth: 1

----

v1.0.0 — 2024-06-14
---------------------

The first stable release of DSPyGen.  This milestone delivers a production-ready
framework for building, composing, and deploying DSPy programs at scale.

Added
~~~~~

MCP Server (66 tools)
^^^^^^^^^^^^^^^^^^^^^

A fully-featured `Model Context Protocol <https://modelcontextprotocol.io/>`_
server that exposes DSPyGen capabilities as callable tools to any MCP-compatible
client (Claude Desktop, Cursor, Continue, Zed, etc.).

- **Module execution** — ``run_module``, ``list_modules``, ``get_module_schema``
- **Pipeline execution** — ``run_pipeline``, ``load_pipeline``, ``validate_pipeline``
- **DSPy configuration** — ``init_lm``, ``set_model``, ``get_config``
- **Code generation** — ``gen_module``, ``gen_agent``, ``gen_signature``,
  ``gen_pipeline``, ``gen_test``
- **File I/O** — ``read_file``, ``write_file``, ``list_directory``,
  ``create_directory``, ``delete_file``, ``move_file``
- **Shell execution** — ``run_command``, ``run_script``, ``run_python``
- **Git integration** — ``git_status``, ``git_diff``, ``git_commit``,
  ``git_push``, ``git_log``
- **Search** — ``grep_codebase``, ``find_files``, ``search_symbols``
- **Testing** — ``run_tests``, ``run_test_file``, ``run_test_case``
- **Documentation** — ``build_docs``, ``serve_docs``
- **Data tools** — ``query_csv``, ``query_json``, ``convert_format``
- **HTTP client** — ``http_get``, ``http_post``, ``http_put``, ``http_delete``
- **Environment** — ``get_env``, ``set_env``, ``list_env``
- **Prompt templates** — ``blog_post``, ``summarize``, ``code_review``
- **Resources** — ``dspygen://modules``, ``dspygen://pipelines/{name}``,
  ``dspygen://config``

Start the server with ``dspygen mcp serve``.  See :doc:`mcp` for full details.

LSP Server (14 capabilities)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A Language Server Protocol server that brings AI-aware IDE intelligence to
DSPy and DSPyGen projects.

1. ``textDocument/completion`` — module class names, ``forward()`` parameters,
   pipeline YAML keys, and DSPy signature field types
2. ``textDocument/hover`` — class/field docstrings, types, default values, and
   links to online API documentation
3. ``textDocument/definition`` — jump to module source or pipeline step class
4. ``textDocument/references`` — find every usage of a module or signature
5. ``textDocument/diagnostics`` — missing required fields (errors), deprecated
   names (warnings), type mismatches (errors)
6. ``textDocument/codeAction`` — *Generate module stub*, *Optimize module*
7. ``textDocument/rename`` — rename a module across the project
8. ``textDocument/formatting`` — auto-format pipeline YAML
9. ``textDocument/rangeFormatting`` — format a selected range
10. ``textDocument/signatureHelp`` — show ``forward()`` signature while typing
11. ``textDocument/documentSymbol`` — outline of all module classes in the file
12. ``workspace/symbol`` — project-wide symbol search
13. ``workspace/didChangeConfiguration`` — live reload of ``[tool.dspygen.lsp]``
    settings
14. ``$/cancelRequest`` — graceful cancellation of long-running operations

Start the server with ``dspygen lsp serve``.  See :doc:`lsp` for full details.

Jupyter Magic Extension (7 commands)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Load with ``%load_ext dspygen.jupyter.magic``.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Magic
     - Purpose
   * - ``%dspygen_init [model]``
     - Configure a DSPy LM backend (OpenAI, Ollama, Groq, Cerebras).
   * - ``%dspygen_modules``
     - List all available DSPyGen modules in a formatted table.
   * - ``%dspygen_agents``
     - List all available DSPyGen agents.
   * - ``%%dspygen_signature Name``
     - Compile a DSPy Signature class body and inject it into the namespace.
   * - ``%dspygen <module> [args]``
     - Invoke any DSPyGen module with positional or keyword arguments.
   * - ``%%dspygen_pipeline``
     - Execute a YAML-defined multi-step pipeline.
   * - ``%dspygen_history [N]``
     - Display the last N LM prompt/completion pairs.

VS Code Extension
^^^^^^^^^^^^^^^^^

Published to the `VS Code Marketplace
<https://marketplace.visualstudio.com/items?itemName=seanchatmangpt.dspygen>`_
as ``seanchatmangpt.dspygen``.

- Bundles the LSP server with zero-configuration setup.
- Syntax highlighting for ``.dspygen.yaml`` pipeline files.
- Run-module code lens above every ``dspy.Module`` subclass.
- Integrated output panel for MCP server logs.
- Configurable via VS Code ``settings.json`` under the ``dspygen.*`` namespace.

pytest Plugin
^^^^^^^^^^^^^

``pytest-dspygen`` integrates DSPyGen into the pytest test suite and is
auto-discovered via the ``pytest11`` entry-point — no ``conftest.py``
changes required.

Fixtures provided:

- ``dspy_lm`` — session-scoped configured DSPy LM.
- ``dspy_module`` — factory fixture that instantiates any module by name.
- ``mcp_server`` — spins up an in-process MCP server for tool-call tests.
- ``lsp_client`` — connects an LSP client to the server for protocol tests.
- ``pipeline_runner`` — runs YAML pipelines inside test functions.
- ``mock_lm`` — deterministic LM stub for fast unit tests.

Sphinx Documentation
^^^^^^^^^^^^^^^^^^^^^

Full Sphinx documentation site built with the ``furo`` theme and hosted at
https://dspygen.readthedocs.io.

- ``autodoc`` API reference for all public subpackages.
- Narrative guides: :doc:`quickstart`, :doc:`mcp`, :doc:`lsp`, :doc:`rdddy`.
- ``sphinx-copybutton`` on every code block.
- ``sphinx.ext.intersphinx`` cross-links to DSPy, Pydantic, and Typer docs.

Type Stubs
^^^^^^^^^^

PEP 561 ``py.typed`` marker and hand-maintained ``.pyi`` stub files:

- ``dspygen/modules/*.pyi`` — ``forward()`` signatures with full type annotations.
- ``dspygen/mcp/server.pyi`` — ``create_server()`` and transport types.
- ``dspygen/lsp/server.pyi`` — ``create_lsp_server()`` and capability types.
- ``dspygen/utils/dspy_tools.pyi`` — ``init_dspy()`` / ``init_ol()`` overloads.

Enables accurate type checking with ``mypy``, ``pyright``, and ``pytype``
without importing the full package at type-check time.

CI/CD (7 workflows)
^^^^^^^^^^^^^^^^^^^^

Seven GitHub Actions workflows under ``.github/workflows/``:

.. list-table::
   :header-rows: 1
   :widths: 28 72

   * - Workflow
     - Trigger & purpose
   * - ``ci.yml``
     - Push / PR — lint (ruff), type-check (mypy), unit tests (pytest).
   * - ``test-mcp.yml``
     - Push / PR — integration tests for all 66 MCP tools.
   * - ``test-lsp.yml``
     - Push / PR — integration tests for all 14 LSP capabilities.
   * - ``docs.yml``
     - Push to ``main`` — build Sphinx docs and deploy to Read the Docs.
   * - ``publish.yml``
     - Tag ``v*`` — build and publish wheel to PyPI via Trusted Publisher.
   * - ``nightly.yml``
     - Daily cron — full test matrix across Python 3.10 / 3.11 / 3.12.
   * - ``security.yml``
     - Weekly cron — ``pip-audit`` dependency audit and secret scanning.

Changed
~~~~~~~

- ``init_dspy()`` now accepts a ``provider`` keyword argument (``"openai"``,
  ``"ollama"``, ``"groq"``, ``"cerebras"``) for explicit backend selection.
- Pipeline YAML schema updated to version 2; version 1 files are automatically
  migrated on load with a deprecation warning.
- CLI commands reorganised under ``dspygen mcp ...`` and ``dspygen lsp ...``
  subgroups; old flat commands emit a deprecation notice and are forwarded.
- Minimum Python version raised to **3.10**.

Fixed
~~~~~

- ``GenDspyModule`` no longer raises ``AttributeError`` when the LM returns
  an empty prediction.
- MCP server no longer drops the last byte of large payloads over stdio transport.
- LSP ``textDocument/completion`` no longer crashes on files with Windows line
  endings (CRLF).
- ``init_ol()`` now correctly passes ``num_ctx`` as ``max_tokens`` for Ollama
  models that use the non-standard parameter name.

Deprecated
~~~~~~~~~~

- ``dspygen.utils.dspy_tools.init_lm`` — use ``init_dspy(provider=...)`` instead.
- Pipeline YAML ``version: 1`` schema — upgrade to ``version: 2``.

Security
~~~~~~~~

- Removed debug endpoint ``/debug/env`` from the MCP SSE transport that could
  leak environment variables to unauthenticated clients.

----

Earlier Development
--------------------

DSPyGen was developed iteratively as a research project.  Pre-1.0 releases are
not listed here; consult the ``git log`` for the full history.
