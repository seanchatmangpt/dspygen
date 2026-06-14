"""Tests for the DSPygen LSP server assembly.

Verifies that the server is correctly wired up: the right name, version,
features registered, and the entry points available.
"""
from __future__ import annotations

import pytest

pygls = pytest.importorskip("pygls")
lsprotocol = pytest.importorskip("lsprotocol")

from lsprotocol import types as lsp_types

pytestmark = pytest.mark.lsp


@pytest.fixture(scope="module")
def lsp_server():
    """Import and return the assembled LanguageServer instance."""
    from dspygen.lsp.server import server
    return server


@pytest.mark.lsp
def test_server_creates_successfully(lsp_server):
    """The server module imports and the LanguageServer object is created."""
    from pygls.lsp.server import LanguageServer
    assert isinstance(lsp_server, LanguageServer)


@pytest.mark.lsp
def test_server_name_and_version(lsp_server):
    """The server name is ``"dspygen-lsp"`` and version is set."""
    assert lsp_server.name == "dspygen-lsp"
    assert lsp_server.version  # non-empty string
    assert isinstance(lsp_server.version, str)


@pytest.mark.lsp
def test_completion_feature_registered(lsp_server):
    """The server has the completion feature (``textDocument/completion``) registered."""
    protocol = lsp_server.protocol
    method_name = lsp_types.TEXT_DOCUMENT_COMPLETION  # "textDocument/completion"
    bf = getattr(protocol, "fm", None) or getattr(protocol, "_feature_manager", None)
    if bf is not None:
        feature_keys = list(bf._features.keys()) if hasattr(bf, "_features") else []
        assert method_name in feature_keys, (
            f"Expected '{method_name}' in registered features, got: {feature_keys}"
        )
    else:
        pytest.skip("Cannot introspect feature manager on this pygls version")


@pytest.mark.lsp
def test_hover_feature_registered(lsp_server):
    """The server has the hover feature (``textDocument/hover``) registered."""
    protocol = lsp_server.protocol
    method_name = lsp_types.TEXT_DOCUMENT_HOVER
    bf = getattr(protocol, "fm", None) or getattr(protocol, "_feature_manager", None)
    if bf is not None:
        feature_keys = list(bf._features.keys()) if hasattr(bf, "_features") else []
        assert method_name in feature_keys, (
            f"Expected '{method_name}' in registered features, got: {feature_keys}"
        )
    else:
        pytest.skip("Cannot introspect feature manager on this pygls version")


@pytest.mark.lsp
def test_diagnostics_registered(lsp_server):
    """The server has didOpen and didChange handlers registered."""
    protocol = lsp_server.protocol
    bf = getattr(protocol, "fm", None) or getattr(protocol, "_feature_manager", None)
    if bf is not None:
        feature_keys = list(bf._features.keys()) if hasattr(bf, "_features") else []
        assert lsp_types.TEXT_DOCUMENT_DID_OPEN in feature_keys, (
            f"Expected 'textDocument/didOpen' registered, got: {feature_keys}"
        )
        assert lsp_types.TEXT_DOCUMENT_DID_CHANGE in feature_keys, (
            f"Expected 'textDocument/didChange' registered, got: {feature_keys}"
        )
    else:
        pytest.skip("Cannot introspect feature manager on this pygls version")


@pytest.mark.lsp
def test_definition_feature_registered(lsp_server):
    """The server has the definition feature (``textDocument/definition``) registered."""
    protocol = lsp_server.protocol
    method_name = lsp_types.TEXT_DOCUMENT_DEFINITION
    bf = getattr(protocol, "fm", None) or getattr(protocol, "_feature_manager", None)
    if bf is not None:
        feature_keys = list(bf._features.keys()) if hasattr(bf, "_features") else []
        assert method_name in feature_keys, (
            f"Expected '{method_name}' in registered features, got: {feature_keys}"
        )
    else:
        pytest.skip("Cannot introspect feature manager on this pygls version")


@pytest.mark.lsp
def test_run_stdio_callable():
    """``run_stdio`` is exported from the server module and is callable."""
    from dspygen.lsp.server import run_stdio
    assert callable(run_stdio)
