Quick Start
===========

This guide walks you through the most common DSPyGen workflows so you can be productive in minutes.

Prerequisites
-------------

Make sure DSPyGen is installed and your API key is set:

.. code-block:: bash

    pip install dspygen
    export OPENAI_API_KEY="sk-..."

1. Initialize DSPy
------------------

DSPyGen wraps DSPy's language model configuration with sensible defaults. The ``init_dspy()`` helper
configures a language model and makes it globally available:

.. code-block:: python

    from dspygen.utils.dspy_tools import init_dspy

    # Use the default model (gpt-4o-mini)
    lm = init_dspy()

    # Specify a model explicitly
    lm = init_dspy(model="gpt-4o", max_tokens=4096)

To use a local Ollama model instead:

.. code-block:: python

    from dspygen.utils.dspy_tools import init_ol

    # Connect to a locally running Ollama instance
    lm = init_ol(model="llama3", max_tokens=2048)

2. Run a Module
---------------

DSPyGen modules are self-contained DSPy programs that perform a specific task. Here is an example
using the built-in ``BlogModule`` to generate a blog post:

.. code-block:: python

    from dspygen.utils.dspy_tools import init_dspy
    from dspygen.modules.blog_module import BlogModule

    # Initialize the language model
    init_dspy()

    # Instantiate and call the module
    blog = BlogModule()
    result = blog.forward(topic="Introduction to DSPy", tone="informative", length="short")

    print(result.blog_post)

You can also use the ``invoke`` helper for a one-liner:

.. code-block:: python

    from dspygen.modules.blog_module import invoke

    post = invoke(topic="Introduction to DSPy", tone="informative", length="short")
    print(post)

3. End-to-End Example
---------------------

The following example shows a complete, self-contained workflow — from initialising
the language model to running a module and composing modules with the pipe operator.

.. code-block:: python

    from dspygen.utils.dspy_tools import init_dspy
    init_dspy()

    from dspygen.modules.gen_dspy_module import GenDspyModule

    # Run the module end-to-end
    module = GenDspyModule()
    result = module.forward(
        signature="text -> summary",
        instructions="Summarize the input text in one sentence.",
    )
    print(result)

Modules support the **pipe operator** (``|``) for left-to-right composition.
The output of the left module is forwarded as the input to the right module:

.. code-block:: python

    from dspygen.utils.dspy_tools import init_dspy
    init_dspy()

    from dspygen.modules.blog_module import BlogModule
    from dspygen.modules.summarize_module import SummarizeModule

    # Compose two modules with the | operator
    pipeline = BlogModule() | SummarizeModule()

    result = pipeline.forward(
        topic="The future of AI-assisted software development",
        tone="professional",
        length="medium",
    )
    print(result)

Each module's ``forward()`` return value is passed directly to the next module's
first positional argument.  The final result is the output of the rightmost module.

4. Run a Pipeline with YAML
---------------------------

DSPyGen supports declarative pipelines defined in YAML. Create a file called ``my_pipeline.yaml``:

.. code-block:: yaml

    pipeline:
      name: blog_pipeline
      steps:
        - module: dspygen.modules.blog_module.BlogModule
          args:
            topic: "{{ topic }}"
            tone: "informative"
            length: "medium"
          output: blog_post

        - module: dspygen.modules.summarize_module.SummarizeModule
          args:
            text: "{{ blog_post }}"
          output: summary

Then run it from Python:

.. code-block:: python

    from dspygen.pipeline import Pipeline

    pipeline = Pipeline.from_yaml("my_pipeline.yaml")
    result = pipeline.run(topic="Reactive Domain-Driven Design")

    print(result["summary"])

Or from the CLI:

.. code-block:: bash

    dspygen pipeline run my_pipeline.yaml --topic "Reactive Domain-Driven Design"

5. Use DSPyGen in Jupyter
--------------------------

DSPyGen provides a Jupyter magic extension for interactive exploration. Load it in a notebook:

.. code-block:: python

    %load_ext dspygen.jupyter_extension

Then use the ``%%dspygen`` cell magic to run a module inline:

.. code-block:: python

    %%dspygen BlogModule
    topic: "Getting started with AI frameworks"
    tone: "friendly"
    length: "short"

The output is automatically displayed in the notebook and stored in the ``_dspygen_result`` variable.

6. Use the CLI
--------------

DSPyGen ships with a Typer-based CLI. Explore available commands:

.. code-block:: bash

    dspygen --help

List all available modules:

.. code-block:: bash

    dspygen modules list

Generate a new module scaffold:

.. code-block:: bash

    dspygen modules new my_custom_module

Run a specific module from the command line:

.. code-block:: bash

    dspygen modules run blog_module --topic "AI trends" --tone "professional"

Start the MCP server:

.. code-block:: bash

    dspygen mcp serve

Start the LSP server:

.. code-block:: bash

    dspygen lsp serve

Next Steps
----------

- Read the :doc:`modules` page to explore the full library of 127+ pre-built modules.
- Read the :doc:`rdddy` page to learn about the Reactive Domain-Driven Design framework.
- Read the :doc:`mcp` page to integrate DSPyGen with AI tool-calling clients.
- Read the :doc:`lsp` page to set up IDE support.
- Browse the :doc:`api/modules` reference for full API documentation.
