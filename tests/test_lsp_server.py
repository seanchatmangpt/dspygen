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

diff --git a/tests/test_lsp_server.py b/tests/test_lsp_server.py
new file mode 100644
index 0000000..2f7cd3e
--- /dev/null
+++ b/tests/test_lsp_server.py
@@ -0,0 +1,120 @@
+"""Tests for the DSPygen LSP server assembly.
+
+Verifies that the server is correctly wired up: the right name, version,
+features registered, and the ``run_stdio`` entry point available.
+"""
+from __future__ import annotations
+
+import pytest
+
+pygls = pytest.importorskip("pygls")
+lsprotocol = pytest.importorskip("lsprotocol")
+
+from lsprotocol import types as lsp_types
+
+pytestmark = pytest.mark.lsp
+
+
+@pytest.fixture(scope="module")
+def lsp_server():
+    """Import and return the assembled LanguageServer instance."""
+    from dspygen.lsp.server import server
+    return server
+
+
+@pytest.mark.lsp
+def test_server_creates_successfully(lsp_server):
+    """The server module imports and the LanguageServer object is created."""
+    from pygls.lsp.server import LanguageServer
+    assert isinstance(lsp_server, LanguageServer)
+
+
+@pytest.mark.lsp
+def test_server_name_and_version(lsp_server):
+    """The server name is ``"dspygen-lsp"`` and version is set."""
+    assert lsp_server.name == "dspygen-lsp"
+    assert lsp_server.version  # non-empty string
+    assert isinstance(lsp_server.version, str)
+
+
+@pytest.mark.lsp
+def test_completion_feature_registered(lsp_server):
+    """The server has the completion feature (``textDocument/completion``) registered."""
+    protocol = lsp_server.protocol
+    method_name = lsp_types.TEXT_DOCUMENT_COMPLETION  # "textDocument/completion"
+    # pygls stores registered features under the protocol's feature manager
+    features = protocol.fm._features if hasattr(protocol, "fm") else {}
+    # Also check via BF (built-in feature manager variant)
+    registered = (
+        method_name in features
+        or hasattr(protocol, "_features") and method_name in getattr(protocol, "_features", {})
+        or any(
+            method_name in str(attr)
+            for attr in dir(protocol)
+        )
+    )
+    # The most reliable check: ensure the handler was registered via @server.feature(...)
+    # by verifying the feature map in the protocol's feature manager
+    bf = getattr(protocol, "fm", None) or getattr(protocol, "_feature_manager", None)
+    if bf is not None:
+        feature_keys = list(bf._features.keys()) if hasattr(bf, "_features") else []
+        assert method_name in feature_keys, (
+            f"Expected '{method_name}' in registered features, got: {feature_keys}"
+        )
+    else:
+        # Fallback: at minimum the server module exports the feature
+        pytest.skip("Cannot introspect feature manager on this pygls version")
+
+
+@pytest.mark.lsp
+def test_hover_feature_registered(lsp_server):
+    """The server has the hover feature (``textDocument/hover``) registered."""
+    protocol = lsp_server.protocol
+    method_name = lsp_types.TEXT_DOCUMENT_HOVER
+    bf = getattr(protocol, "fm", None) or getattr(protocol, "_feature_manager", None)
+    if bf is not None:
+        feature_keys = list(bf._features.keys()) if hasattr(bf, "_features") else []
+        assert method_name in feature_keys, (
+            f"Expected '{method_name}' in registered features, got: {feature_keys}"
+        )
+    else:
+        pytest.skip("Cannot introspect feature manager on this pygls version")
+
+
+@pytest.mark.lsp
+def test_diagnostics_registered(lsp_server):
+    """The server has didOpen and didChange handlers registered."""
+    protocol = lsp_server.protocol
+    bf = getattr(protocol, "fm", None) or getattr(protocol, "_feature_manager", None)
+    if bf is not None:
+        feature_keys = list(bf._features.keys()) if hasattr(bf, "_features") else []
+        assert lsp_types.TEXT_DOCUMENT_DID_OPEN in feature_keys, (
+            f"Expected 'textDocument/didOpen' registered, got: {feature_keys}"
+        )
+        assert lsp_types.TEXT_DOCUMENT_DID_CHANGE in feature_keys, (
+            f"Expected 'textDocument/didChange' registered, got: {feature_keys}"
+        )
+    else:
+        pytest.skip("Cannot introspect feature manager on this pygls version")
+
+
+@pytest.mark.lsp
+def test_definition_feature_registered(lsp_server):
+    """The server has the definition feature (``textDocument/definition``) registered."""
+    protocol = lsp_server.protocol
+    method_name = lsp_types.TEXT_DOCUMENT_DEFINITION
+    bf = getattr(protocol, "fm", None) or getattr(protocol, "_feature_manager", None)
+    if bf is not None:
+        feature_keys = list(bf._features.keys()) if hasattr(bf, "_features") else []
+        assert method_name in feature_keys, (
+            f"Expected '{method_name}' in registered features, got: {feature_keys}"
+        )
+    else:
+        pytest.skip("Cannot introspect feature manager on this pygls version")
+
+
+@pytest.mark.lsp
+def test_run_stdio_callable():
+    """``run_stdio`` is exported from the server module and is callable."""
+    from dspygen.lsp.server import run_stdio
+    assert callable(run_stdio)
