Installation
============

This guide covers how to install DSPyGen and configure your environment.

Requirements
------------

- Python 3.10 or higher
- pip or Poetry package manager
- An OpenAI API key (or a compatible local model via Ollama)

Installing with pip
-------------------

The simplest way to install DSPyGen is via pip::

    pip install dspygen

To install with all optional extras::

    pip install "dspygen[jupyter,lsp,mcp]"

Installing with Poetry
----------------------

If you use Poetry for dependency management, add DSPyGen to your project::

    poetry add dspygen

To add with optional extras::

    poetry add "dspygen[jupyter,lsp,mcp]"

Installing from Source
----------------------

To install the latest development version directly from GitHub::

    git clone https://github.com/seanchatmangpt/dspygen.git
    cd dspygen
    pip install -e .

Or with Poetry::

    git clone https://github.com/seanchatmangpt/dspygen.git
    cd dspygen
    poetry install

Environment Setup
-----------------

DSPyGen requires API credentials for the language model backend you plan to use.

OpenAI
~~~~~~

Set your OpenAI API key as an environment variable::

    export OPENAI_API_KEY="sk-..."

You can also add this to your shell profile (``~/.bashrc``, ``~/.zshrc``, etc.) to make it persistent.

Ollama (Local Models)
~~~~~~~~~~~~~~~~~~~~~

If you want to use local models via Ollama, install Ollama from https://ollama.com and then set the host::

    export OLLAMA_HOST="http://localhost:11434"

Start the Ollama service and pull a model::

    ollama serve
    ollama pull llama3

Anthropic Claude
~~~~~~~~~~~~~~~~

To use Anthropic's Claude models::

    export ANTHROPIC_API_KEY="sk-ant-..."

Verifying the Installation
--------------------------

After installation, verify that DSPyGen is correctly installed by running::

    dspygen --version

You should see output similar to::

    DSPyGen version 2024.9.14

You can also run a quick sanity check in Python::

    python -c "import dspygen; print('DSPyGen installed successfully')"

Optional Extras
---------------

DSPyGen ships with several optional dependency groups:

Jupyter Support
~~~~~~~~~~~~~~~

Install the Jupyter integration to use DSPyGen magic commands inside notebooks::

    pip install "dspygen[jupyter]"

Then load the extension inside a notebook cell::

    %load_ext dspygen.jupyter_extension

LSP Server
~~~~~~~~~~

Install the Language Server Protocol server for IDE integration::

    pip install "dspygen[lsp]"

See the :doc:`lsp` page for configuration instructions.

MCP Server
~~~~~~~~~~

Install the Model Context Protocol server for tool-calling integrations::

    pip install "dspygen[mcp]"

See the :doc:`mcp` page for configuration instructions.

Upgrading
---------

To upgrade an existing installation::

    pip install --upgrade dspygen

Or with Poetry::

    poetry update dspygen

Uninstalling
------------

To remove DSPyGen::

    pip uninstall dspygen
