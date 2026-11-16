Cookbook
========

Practical recipes for common dspygen tasks.

.. contents::
   :local:
   :depth: 2


Basic Module Generation
-----------------------

Generate a DSPy signature and module from a natural language description::

    from dspygen.convenience import quick_predict, init_dspy

    init_dspy(model="gpt-4o", max_tokens=1000)
    result = quick_predict("question -> answer", question="What is DSPy?")
    print(result.answer)


SQL from Natural Language
-------------------------

Convert plain English to SQL using the built-in module::

    from dspygen.utils.dspy_tools import init_dspy
    import dspy

    init_dspy()

    class NLToSQL(dspy.Signature):
        """Convert a natural language query to SQL."""
        query: str = dspy.InputField()
        schema: str = dspy.InputField(desc="Database schema DDL")
        sql: str = dspy.OutputField()

    predict = dspy.Predict(NLToSQL)
    result = predict(query="Show all users created this week", schema="CREATE TABLE users (id INT, name TEXT, created_at TIMESTAMP)")
    print(result.sql)


Chain of Thought Reasoning
--------------------------

Use ChainOfThought for complex reasoning tasks::

    import dspy

    class Reasoning(dspy.Signature):
        """Solve a multi-step problem."""
        problem: str = dspy.InputField()
        solution: str = dspy.OutputField()

    cot = dspy.ChainOfThought(Reasoning)
    result = cot(problem="If a train travels 60 mph for 2.5 hours, how far does it go?")
    print(result.solution)


MCP Tool Integration
--------------------

Use dspygen tools from Claude Desktop::

    # mcp_config.json
    {
      "mcpServers": {
        "dspygen": {
          "command": "dspygen-mcp",
          "env": {
            "OPENAI_API_KEY": "sk-..."
          }
        }
      }
    }

Then in Claude, ask: *"List all dspygen modules"* or *"Generate a DSPy module for sentiment analysis"*.


Batch Processing with Pipelines
--------------------------------

Run multiple modules in sequence using YAML pipelines::

    # pipeline.yaml
    steps:
      - module: natural_language_to_sql_module
        inputs: {query: "Find active users"}
      - module: document_summarizer_module
        inputs: {text: "{{previous.sql}}"}

Run with::

    dspygen pipeline run pipeline.yaml


RDDDY Domain Modeling
---------------------

Model a domain using Reactive Domain-Driven Design::

    from dspygen.rdddy.base_command import BaseCommand
    from dspygen.rdddy.base_event import BaseEvent

    class CreateUser(BaseCommand):
        username: str
        email: str

    class UserCreated(BaseEvent):
        user_id: str
        username: str

    # Use the MCP tool to scaffold a full domain:
    # dspygen-mcp → scaffold_domain(domain_name="user_management")


LSP in VS Code
--------------

1. Install the VS Code extension::

       code --install-extension dspygen.vscode-dspygen

2. Open a Python file with DSPy code.
3. Hover over a ``dspy.Signature`` string to see field documentation.
4. Use ``Ctrl+Space`` inside ``dspy.Predict(...)`` to get signature completions.


Health Check
------------

Verify your installation::

    dspygen doctor

Expected output::

    ✓ Python 3.11.9
    ✓ dspygen 2024.9.14
    ✓ dspy-ai installed
    ✓ OPENAI_API_KEY set
    ✓ MCP server importable
    ✓ LSP server importable
