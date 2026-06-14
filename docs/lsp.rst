LSP Server
==========

DSPyGen includes a `Language Server Protocol (LSP) <https://microsoft.github.io/language-server-protocol/>`_
server that provides AI-powered code intelligence for DSPy and DSPyGen projects directly inside
your editor.

What is LSP?
------------

The Language Server Protocol is an open standard that defines how editors and IDEs communicate
with language servers to provide features such as auto-completion, hover documentation, go-to
definition, and inline diagnostics — all without editor-specific plugins.

DSPyGen's LSP server understands DSPy module signatures, pipeline YAML schemas, and dspygen
configuration files, offering intelligent assistance as you write AI-powered code.

Installation
------------

The LSP server is an optional extra. Install it with:

.. code-block:: bash

    pip install "dspygen[lsp]"

Or with Poetry:

.. code-block:: bash

    poetry add "dspygen[lsp]"

Starting the Server
-------------------

Start the LSP server from the command line:

.. code-block:: bash

    dspygen lsp serve

By default the server communicates over ``stdio``. For TCP mode:

.. code-block:: bash

    dspygen lsp serve --tcp --host 127.0.0.1 --port 2087

You can also start it programmatically:

.. code-block:: python

    from dspygen.lsp.server import create_lsp_server
    import asyncio

    server = create_lsp_server()
    asyncio.run(server.start_io())

IDE Configuration
-----------------

VS Code
~~~~~~~

1. Install the `DSPyGen VS Code extension <https://marketplace.visualstudio.com/items?itemName=seanchatmangpt.dspygen>`_
   from the marketplace, **or** configure the generic ``vscode-lsp-client`` manually.

2. Add to your VS Code ``settings.json``:

   .. code-block:: json

       {
         "dspygen.lsp.enabled": true,
         "dspygen.lsp.command": "dspygen",
         "dspygen.lsp.args": ["lsp", "serve"],
         "dspygen.lsp.filetypes": ["python", "yaml"]
       }

3. Reload the window. The status bar should show **DSPyGen LSP: running**.

Neovim
~~~~~~

Using ``nvim-lspconfig``:

.. code-block:: lua

    local lspconfig = require("lspconfig")
    local configs = require("lspconfig.configs")

    if not configs.dspygen then
      configs.dspygen = {
        default_config = {
          cmd = { "dspygen", "lsp", "serve" },
          filetypes = { "python", "yaml" },
          root_dir = lspconfig.util.root_pattern("pyproject.toml", ".git"),
          settings = {},
        },
      }
    end

    lspconfig.dspygen.setup({
      on_attach = function(client, bufnr)
        -- your on_attach keybindings here
      end,
    })

Using ``mason.nvim``:

.. code-block:: lua

    require("mason-lspconfig").setup({
      ensure_installed = { "dspygen" },
    })

Emacs
~~~~~

Using ``eglot`` (built-in since Emacs 29):

.. code-block:: emacs-lisp

    (with-eval-after-load 'eglot
      (add-to-list 'eglot-server-programs
                   '((python-mode python-ts-mode yaml-mode)
                     . ("dspygen" "lsp" "serve"))))

    (add-hook 'python-mode-hook 'eglot-ensure)
    (add-hook 'yaml-mode-hook 'eglot-ensure)

Using ``lsp-mode``:

.. code-block:: emacs-lisp

    (use-package lsp-mode
      :hook ((python-mode . lsp-deferred)
             (yaml-mode   . lsp-deferred))
      :config
      (lsp-register-client
       (make-lsp-client
        :new-connection (lsp-stdio-connection '("dspygen" "lsp" "serve"))
        :major-modes '(python-mode yaml-mode)
        :server-id 'dspygen)))

Sublime Text
~~~~~~~~~~~~

Install the ``LSP`` package via Package Control, then add to ``LSP.sublime-settings``:

.. code-block:: json

    {
      "clients": {
        "dspygen": {
          "command": ["dspygen", "lsp", "serve"],
          "enabled": true,
          "selector": "source.python, source.yaml"
        }
      }
    }

Features
--------

Auto-Completion
~~~~~~~~~~~~~~~

- Module class names and their ``forward()`` parameter names.
- Pipeline YAML keys and allowed values.
- DSPy signature field types (``dspy.InputField``, ``dspy.OutputField``).
- ``init_dspy()`` / ``init_ol()`` keyword arguments.

Hover Documentation
~~~~~~~~~~~~~~~~~~~

Hovering over a module class, signature field, or pipeline key shows:

- The class or field docstring.
- Accepted types and default values.
- Links to the online API documentation.

Go-to Definition
~~~~~~~~~~~~~~~~

- Jump from a module import to its source file.
- Jump from a pipeline step name to the corresponding module class.

Inline Diagnostics
~~~~~~~~~~~~~~~~~~

- Missing required pipeline fields highlighted as errors.
- Deprecated module names shown as warnings.
- Type mismatches between pipeline outputs and module inputs.

Code Actions
~~~~~~~~~~~~

- **Generate module stub** — right-click a ``# TODO`` comment inside a module file to scaffold
  the missing ``forward()`` implementation.
- **Optimize module** — trigger a DSPy optimizer run directly from the editor.

Configuration Options
---------------------

All LSP settings can be placed in ``pyproject.toml`` under ``[tool.dspygen.lsp]``:

.. code-block:: toml

    [tool.dspygen.lsp]
    # Log level: "debug" | "info" | "warning" | "error"
    log_level = "info"

    # Additional paths to search for modules
    module_search_paths = ["src/my_custom_modules"]

    # Disable specific diagnostics
    disabled_diagnostics = ["deprecated-module"]

    # Maximum number of completions to return
    max_completions = 50

API Reference
-------------

See :doc:`api/lsp` for full API documentation.
