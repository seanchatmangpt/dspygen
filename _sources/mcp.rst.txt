MCP Server
==========

DSPyGen ships with a built-in `Model Context Protocol (MCP) <https://modelcontextprotocol.io/>`_
server that exposes DSPyGen's capabilities as callable tools to any MCP-compatible client
(Claude Desktop, Cursor, Continue, etc.).

What is MCP?
------------

The Model Context Protocol is an open standard that defines how AI applications discover and
call external tools, read resources (files, databases, APIs), and inject structured prompts.
By running DSPyGen's MCP server, language model clients can:

- Invoke DSPyGen modules as tools.
- Read project resources (pipelines, module definitions).
- Use pre-built prompt templates for common AI tasks.

Starting the MCP Server
------------------------

Start the server with the CLI:

.. code-block:: bash

    dspygen mcp serve

By default the server listens on ``stdio`` (standard input/output), which is the transport used
by Claude Desktop and most MCP clients. To use a TCP socket instead:

.. code-block:: bash

    dspygen mcp serve --transport sse --port 8000

You can also start the server programmatically:

.. code-block:: python

    from dspygen.mcp.server import create_server
    import asyncio

    server = create_server()
    asyncio.run(server.run_stdio())

Tools Exposed
-------------

The MCP server exposes the following tool categories:

Module Execution
~~~~~~~~~~~~~~~~

``run_module``
    Execute any registered DSPyGen module by name.

    **Parameters:**

    - ``module_name`` (string) — Fully qualified module class name, e.g.
      ``"dspygen.modules.blog_module.BlogModule"``.
    - ``kwargs`` (object) — Keyword arguments passed to the module's ``forward`` method.

    **Returns:** The module's prediction as a JSON object.

``list_modules``
    List all available DSPyGen modules with their signatures and descriptions.

    **Returns:** Array of module descriptors.

Pipeline Execution
~~~~~~~~~~~~~~~~~~

``run_pipeline``
    Execute a DSPyGen YAML pipeline.

    **Parameters:**

    - ``pipeline_yaml`` (string) — Pipeline definition as a YAML string.
    - ``inputs`` (object) — Template variables for the pipeline.

    **Returns:** Final pipeline outputs as a JSON object.

``load_pipeline``
    Load a pipeline from a file path on the server's filesystem.

    **Parameters:**

    - ``path`` (string) — Absolute path to a ``.yaml`` pipeline file.

DSPy Configuration
~~~~~~~~~~~~~~~~~~

``init_lm``
    Initialize the language model backend.

    **Parameters:**

    - ``model`` (string) — Model identifier, e.g. ``"openai/gpt-4o"``.
    - ``api_key`` (string, optional) — Override the API key from environment.
    - ``max_tokens`` (integer, optional) — Maximum tokens per response.

Resources
---------

The MCP server exposes the following resource URIs:

``dspygen://modules``
    A JSON list of all available modules, their input/output signatures, and docstrings.

``dspygen://pipelines/{name}``
    The YAML source of a named pipeline stored in the server's pipeline registry.

``dspygen://config``
    The current DSPyGen and DSPy configuration as JSON.

Prompts
-------

The server provides these reusable prompt templates:

``blog_post``
    Generate a structured blog post on any topic.

    **Arguments:** ``topic``, ``tone``, ``length``

``summarize``
    Summarize a long piece of text.

    **Arguments:** ``text``, ``max_sentences``

``code_review``
    Review a code snippet and suggest improvements.

    **Arguments:** ``code``, ``language``, ``focus``

Configuration
-------------

Claude Desktop
~~~~~~~~~~~~~~

Add the following to your ``claude_desktop_config.json``:

.. code-block:: json

    {
      "mcpServers": {
        "dspygen": {
          "command": "dspygen",
          "args": ["mcp", "serve"],
          "env": {
            "OPENAI_API_KEY": "sk-..."
          }
        }
      }
    }

Cursor
~~~~~~

Add to ``.cursor/mcp.json`` in your project root:

.. code-block:: json

    {
      "mcpServers": {
        "dspygen": {
          "command": "dspygen",
          "args": ["mcp", "serve"],
          "env": {
            "OPENAI_API_KEY": "sk-..."
          }
        }
      }
    }

Continue (VS Code)
~~~~~~~~~~~~~~~~~~

Add to ``~/.continue/config.json``:

.. code-block:: json

    {
      "experimental": {
        "modelContextProtocolServers": [
          {
            "transport": {
              "type": "stdio",
              "command": "dspygen",
              "args": ["mcp", "serve"]
            }
          }
        ]
      }
    }

Security Considerations
-----------------------

- The MCP server inherits the permissions of the process running it. Run it with a
  least-privilege user in production.
- Avoid exposing the TCP transport (``--transport sse``) on a public interface without
  authentication.
- API keys are read from environment variables; never pass them as tool arguments in
  multi-user environments.

API Reference
-------------

See :doc:`api/mcp` for full API documentation.
