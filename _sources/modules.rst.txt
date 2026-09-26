DSPyGen Modules
===============

DSPyGen modules are self-contained DSPy programs that encapsulate a specific language model task.
Each module defines typed input and output fields, an optional few-shot signature, and a ``forward``
method that executes the task against the configured language model.

.. automodule:: dspygen.modules
   :members:
   :undoc-members:

Overview
--------

Modules follow a consistent interface:

.. code-block:: python

    from dspygen.utils.dspy_tools import init_dspy
    from dspygen.modules.blog_module import BlogModule

    init_dspy()

    module = BlogModule()
    result = module.forward(topic="My Topic", tone="professional", length="medium")
    print(result.blog_post)

Every module also exposes a top-level ``invoke()`` helper for one-liner usage:

.. code-block:: python

    from dspygen.modules.blog_module import invoke

    post = invoke(topic="My Topic", tone="professional", length="medium")

Creating a Custom Module
------------------------

Use the CLI to scaffold a new module:

.. code-block:: bash

    dspygen modules new my_task_module

This generates ``src/dspygen/modules/my_task_module.py`` with a class stub, typed signature,
and ``invoke`` entry point you can fill in.

Alternatively, subclass ``dspy.Module`` directly:

.. code-block:: python

    import dspy
    from dspygen.utils.dspy_tools import init_dspy

    class MySignature(dspy.Signature):
        """Perform my custom task."""
        input_text: str = dspy.InputField(desc="The input text")
        result: str = dspy.OutputField(desc="The processed result")

    class MyModule(dspy.Module):
        def __init__(self):
            super().__init__()
            self.predict = dspy.Predict(MySignature)

        def forward(self, input_text: str) -> dspy.Prediction:
            return self.predict(input_text=input_text)

Available Modules
-----------------

DSPyGen provides over 127 pre-built modules organized by task domain.

Content Generation
~~~~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: _autosummary

   dspygen.modules.blog_module
   dspygen.modules.chat_bot_module
   dspygen.modules.gen_pydantic_instance

Classification and Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: _autosummary

   dspygen.modules.binary_output_module

Utilities
~~~~~~~~~

.. autosummary::
   :toctree: _autosummary

   dspygen.modules.file_name_module

Module Lifecycle
----------------

1. **Instantiation** — The module is created and its internal DSPy predictor(s) are initialized.
2. **Forward call** — ``forward(**kwargs)`` is invoked with typed keyword arguments.
3. **Prediction** — The underlying ``dspy.Predict`` or ``dspy.ChainOfThought`` sends a prompt to the LM.
4. **Result** — A ``dspy.Prediction`` object is returned with output fields as attributes.

Optimization
------------

Modules are compatible with DSPy's built-in optimizers (``BootstrapFewShot``, ``MIPROv2``, etc.).
Wrap your module in an optimizer to automatically improve its few-shot demonstrations:

.. code-block:: python

    import dspy
    from dspy.teleprompt import BootstrapFewShot
    from dspygen.modules.blog_module import BlogModule

    def metric(example, prediction, trace=None):
        return len(prediction.blog_post) > 200

    optimizer = BootstrapFewShot(metric=metric)
    compiled_module = optimizer.compile(BlogModule(), trainset=my_trainset)
