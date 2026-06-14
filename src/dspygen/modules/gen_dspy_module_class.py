commit 9f3f1a604c2de20b8f583613e0445ca336b523c2
Author: Claude <noreply@anthropic.com>
Date:   Sun Jun 14 19:15:44 2026 +0000

    test: add comprehensive LSP server, providers, and analysis test suite
    
    Implements the full DSPygen LSP server at src/dspygen/lsp/ with:
    - signature_parser.py: parse/validate DSPy "inputs -> outputs" strings
    - module_index.py: index all dspygen modules for search and lookup
    - completion.py: dspy.Predict(), module import, init_dspy(model=) completions
    - hover.py: hover docs for Predict, signature strings, module classes
    - diagnostics.py: lint for invalid signatures, missing forward(), field conflicts
    - definition.py: go-to-definition for dspy module classes
    - server.py: LanguageServer assembly with all features registered
    
    Adds 42 passing tests across three test files:
    - tests/test_lsp_analysis.py (18 tests): pure unit tests for analysis utilities
    - tests/test_lsp_providers.py (17 tests): provider function tests without server
    - tests/test_lsp_server.py (7 tests): server assembly and feature registration
    
    Also adds gen_dspy_module_class.py (GenDspyModule) and registers the lsp
    pytest mark in pyproject.toml.
    
    https://claude.ai/code/session_01R6Mp9kxxQ8dTxXZGZLFNvk

diff --git a/src/dspygen/modules/gen_dspy_module_class.py b/src/dspygen/modules/gen_dspy_module_class.py
new file mode 100644
index 0000000..b7c8ad6
--- /dev/null
+++ b/src/dspygen/modules/gen_dspy_module_class.py
@@ -0,0 +1,54 @@
+"""GenDspyModule — generate DSPy module source code from a specification."""
+
+import dspy
+from dspygen.utils.dspy_tools import init_dspy
+
+
+class GenDspyModule(dspy.Module):
+    """Generate a complete DSPy module class from a natural language specification.
+
+    Takes a description of what the module should do and returns ready-to-use
+    DSPy source code including the class definition, forward method, and CLI
+    scaffolding.
+    """
+
+    def __init__(self, **forward_args):
+        """Initialise GenDspyModule."""
+        super().__init__()
+        self.forward_args = forward_args
+        self.output = None
+
+    def forward(self, specification):
+        """Generate DSPy module source code.
+
+        Args:
+            specification: Natural language description of the module to generate.
+
+        Returns:
+            Python source code string for the requested module.
+        """
+        pred = dspy.Predict("specification -> dspy_module_source")
+        self.output = pred(specification=specification).dspy_module_source
+        return self.output
+
+    def pipe(self, input_str):
+        """Pipe support for DSL chaining."""
+        return self.forward(specification=input_str)
+
+
+def gen_dspy_module_call(specification):
+    """Convenience wrapper around GenDspyModule."""
+    module = GenDspyModule()
+    return module.forward(specification=specification)
+
+
+def main():
+    """CLI entry point."""
+    init_dspy()
+    specification = "A module that translates English text to French."
+    result = gen_dspy_module_call(specification=specification)
+    print(result)
+
+
+if __name__ == "__main__":
+    main()
