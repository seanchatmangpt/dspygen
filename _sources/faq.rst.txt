Frequently Asked Questions
==========================

.. contents::
   :local:
   :depth: 2


Installation
------------

**Q: Which Python versions are supported?**

Python 3.10, 3.11, and 3.12. Python 3.13+ is not yet supported due to upstream dependencies.

**Q: Do I need an OpenAI API key?**

For most features, yes. Set ``OPENAI_API_KEY`` in your environment or ``.env`` file.
You can also use Ollama for local inference — see :doc:`quickstart`.

**Q: How do I install only the MCP server?**

.. code-block:: bash

    pip install "dspygen[mcp]"
    dspygen-mcp  # runs stdio server


Modules
-------

**Q: What's the difference between a DSPy Signature and a Module?**

A *Signature* declares what a module does (inputs → outputs). A *Module* implements how it does it, wrapping one or more Signatures with ``dspy.Predict``, ``dspy.ChainOfThought``, etc.

**Q: How do I add a new module?**

.. code-block:: bash

    dspygen gen module my_module_name

This scaffolds ``src/dspygen/modules/my_module_name.py``.

**Q: My module's forward() raises a TypeError**

Ensure your Signature fields are declared as class-level annotations with ``dspy.InputField()`` / ``dspy.OutputField()``, not as ``__init__`` arguments.


MCP Server
----------

**Q: The MCP server isn't showing up in Claude Desktop**

1. Confirm ``dspygen-mcp`` is on your PATH: ``which dspygen-mcp``
2. Check your ``mcp_config.json`` is saved to ``~/Library/Application Support/Claude/claude_desktop_config.json`` (macOS)
3. Restart Claude Desktop after config changes
4. Run ``dspygen doctor`` to verify all dependencies are installed

**Q: How do I see MCP server logs?**

.. code-block:: bash

    # MCP logs go to stderr; capture with:
    dspygen-mcp 2>~/dspygen-mcp.log


LSP Server
----------

**Q: How do I enable the LSP in VS Code?**

Install the dspygen VS Code extension, which auto-starts ``dspygen-lsp``.
Or add to ``settings.json``::

    "dspygen.lsp.enabled": true

**Q: Completions aren't appearing**

Ensure the file is recognized as Python and ``dspy`` is imported at the top.
Completions trigger after ``dspy.Predict(``, ``dspy.ChainOfThought(``, etc.

**Q: Where are LSP logs?**

.. code-block:: bash

    cat ~/.cache/dspygen/lsp.log


Testing
-------

**Q: How do I run only the fast tests?**

.. code-block:: bash

    pytest  # uses default addopts: excludes slow/benchmark/requires_openai

**Q: How do I run the full test suite?**

.. code-block:: bash

    pytest -m ""  # remove mark filters
    # or:
    pytest --co -q  # see what would run

**Q: Tests fail with "No module named 'dspygen'"**

Ensure the package is installed: ``pip install -e .``
Or run via ``poetry run pytest``.


RDDDY
-----

**Q: What is RDDDY?**

Reactive Domain-Driven Design with Inhabitants — a framework for building event-driven systems with explicit domain models (Commands, Events, Queries, Aggregates, Sagas, Policies).

**Q: How does RDDDY relate to DSPy?**

RDDDY provides the *structural* layer (domain objects, message passing). DSPy provides the *intelligence* layer (LLM predictions). They compose naturally — a RDDDY Command handler can call a DSPy Module.


Performance
-----------

**Q: Module imports are slow**

Use lazy imports. The dspygen modules are designed to import quickly; the LLM call happens only when ``forward()`` is invoked.

**Q: How do I profile a pipeline?**

.. code-block:: bash

    python -m cProfile -s cumulative -m dspygen pipeline run pipeline.yaml
