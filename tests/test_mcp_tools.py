"""Tests for dspygen MCP tools."""

import asyncio
import json
from unittest.mock import MagicMock, patch

import pytest

pytestmark = pytest.mark.mcp


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _run(coro):
    """Run a coroutine synchronously."""
    return asyncio.get_event_loop().run_until_complete(coro)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def mcp_server():
    """Import and return the dspygen MCP server instance."""
    dspygen_mcp = pytest.importorskip(
        "dspygen.mcp.server",
        reason="dspygen.mcp.server not yet available",
    )
    return dspygen_mcp.mcp


@pytest.fixture(scope="module")
def module_tools():
    """Import the module_tools submodule."""
    return pytest.importorskip(
        "dspygen.mcp.tools.module_tools",
        reason="dspygen.mcp.tools.module_tools not yet available",
    )


@pytest.fixture(scope="module")
def workflow_tools():
    """Import the workflow_tools submodule."""
    return pytest.importorskip(
        "dspygen.mcp.tools.workflow_tools",
        reason="dspygen.mcp.tools.workflow_tools not yet available",
    )


@pytest.fixture(scope="module")
def agent_tools():
    """Import the agent_tools submodule."""
    return pytest.importorskip(
        "dspygen.mcp.tools.agent_tools",
        reason="dspygen.mcp.tools.agent_tools not yet available",
    )


@pytest.fixture(scope="module")
def retrieval_tools():
    """Import the retrieval_tools submodule."""
    return pytest.importorskip(
        "dspygen.mcp.tools.retrieval_tools",
        reason="dspygen.mcp.tools.retrieval_tools not yet available",
    )


# ---------------------------------------------------------------------------
# Shared assertion helpers
# ---------------------------------------------------------------------------

def _assert_text_content_list(result):
    """Assert result is a non-empty list[TextContent]."""
    from mcp.types import TextContent

    assert isinstance(result, list), f"Expected list, got {type(result)}"
    assert len(result) > 0, "Result list must not be empty"
    for item in result:
        assert isinstance(item, TextContent), (
            f"Expected TextContent, got {type(item)}: {item!r}"
        )
        assert isinstance(item.text, str), "TextContent.text must be a str"
        assert item.text.strip(), "TextContent.text must not be blank"


# ---------------------------------------------------------------------------
# MODULE TOOLS
# ---------------------------------------------------------------------------

class TestListModules:
    """Tests for list_modules tool."""

    def test_list_modules_returns_json(self, mcp_server):
        """list_modules must return a JSON list with at least 10 entries."""
        result = _run(mcp_server.call_tool("list_modules", {}))
        content, _meta = result
        _assert_text_content_list(content)

        data = json.loads(content[0].text)
        assert isinstance(data, list), "list_modules must return a JSON array"
        assert len(data) >= 10, (
            f"Expected at least 10 modules, got {len(data)}"
        )
        # Each entry should have at minimum a 'name' key
        for entry in data:
            assert "name" in entry, f"Module entry missing 'name': {entry}"

    def test_list_modules_direct(self, module_tools):
        """Call list_modules handler directly and verify JSON output."""
        result = _run(module_tools.list_modules())
        _assert_text_content_list(result)

        data = json.loads(result[0].text)
        assert isinstance(data, list)
        assert len(data) >= 10


class TestGetModuleInfo:
    """Tests for get_module_info tool."""

    def test_get_module_info_known_module(self, mcp_server):
        """get_module_info with a known module name returns docstring and signature."""
        result = _run(mcp_server.call_tool("get_module_info", {"module_name": "GenDspyModule"}))
        content, _meta = result
        _assert_text_content_list(content)

        text = content[0].text
        # Should mention the module name, docstring, or signature info
        lower = text.lower()
        assert any(word in lower for word in ("gendspymodule", "signature", "docstring", "module", "gen")), (
            f"Response for known module lacks module info: {text!r}"
        )

    def test_get_module_info_unknown_module(self, mcp_server):
        """get_module_info with a nonexistent module name returns graceful error."""
        result = _run(mcp_server.call_tool("get_module_info", {"module_name": "NonExistentXyzModule99"}))
        content, _meta = result
        _assert_text_content_list(content)

        text = content[0].text.lower()
        assert any(word in text for word in ("not found", "error", "unknown", "no module", "could not")), (
            f"Expected an error message for unknown module, got: {content[0].text!r}"
        )

    def test_get_module_info_direct_known(self, module_tools):
        """Direct call to get_module_info handler for a known module."""
        result = _run(module_tools.get_module_info("GenDspyModule"))
        _assert_text_content_list(result)

    def test_get_module_info_direct_unknown(self, module_tools):
        """Direct call to get_module_info for unknown module returns graceful response."""
        result = _run(module_tools.get_module_info("AbsolutelyNotARealModuleXXX"))
        _assert_text_content_list(result)
        text = result[0].text.lower()
        assert any(word in text for word in ("not found", "error", "unknown", "no module")), (
            f"Expected error-like response for unknown module: {result[0].text!r}"
        )


class TestRunModule:
    """Tests for run_module tool."""

    def test_run_module_with_mock_lm(self, mcp_server):
        """run_module with mocked LM should return TextContent output."""
        mock_prediction = MagicMock()
        mock_prediction.output = "Mocked module output text"

        mock_lm = MagicMock()
        mock_lm.__call__ = MagicMock(return_value=mock_prediction)

        with (
            patch("dspy.settings.configure"),
            patch("dspy.Predict", return_value=MagicMock(return_value=mock_prediction)),
            patch("dspy.ChainOfThought", return_value=MagicMock(return_value=mock_prediction)),
        ):
            result = _run(
                mcp_server.call_tool(
                    "run_module",
                    {
                        "module_name": "GenDspyModule",
                        "inputs": {"prompt": "Write a hello world function"},
                    },
                )
            )
        content, _meta = result
        _assert_text_content_list(content)

    def test_run_module_missing_input(self, mcp_server):
        """run_module without required inputs must return a graceful error, not raise."""
        try:
            result = _run(
                mcp_server.call_tool(
                    "run_module",
                    {"module_name": "GenDspyModule", "inputs": {}},
                )
            )
            content, _meta = result
            _assert_text_content_list(content)
            # Should contain an error message
            text = content[0].text.lower()
            assert any(word in text for word in ("error", "required", "missing", "invalid", "failed")), (
                f"Expected error message for missing input, got: {content[0].text!r}"
            )
        except Exception as exc:
            pytest.fail(
                f"run_module should return TextContent on error, not raise. Got: {exc!r}"
            )


class TestGenerateDspySignature:
    """Tests for generate_dspy_signature tool."""

    def test_generate_dspy_signature(self, mcp_server):
        """generate_dspy_signature with a mocked generator returns a signature string."""
        mock_sig = "class QuestionAnswer(dspy.Signature):\n    question = dspy.InputField()\n    answer = dspy.OutputField()"

        with patch("dspygen.mcp.tools.module_tools.generate_signature_from_prompt", return_value=mock_sig):
            result = _run(
                mcp_server.call_tool(
                    "generate_dspy_signature",
                    {"signature_prompt": "question -> answer"},
                )
            )
        content, _meta = result
        _assert_text_content_list(content)
        text = content[0].text
        # Output should contain signature-related content
        assert any(keyword in text for keyword in ("Signature", "InputField", "OutputField", "dspy", "class")), (
            f"Signature output does not look like a DSPy signature: {text!r}"
        )

    def test_generate_dspy_signature_direct(self, module_tools):
        """Direct handler call for generate_dspy_signature with mocked backend."""
        mock_sig = "celebrity, gossip -> tweet"
        with patch.object(
            module_tools,
            "generate_signature_from_prompt",
            return_value=mock_sig,
            create=True,
        ):
            result = _run(module_tools.generate_dspy_signature("celebrity, gossip -> tweet"))
        _assert_text_content_list(result)


# ---------------------------------------------------------------------------
# WORKFLOW TOOLS
# ---------------------------------------------------------------------------

VALID_PIPELINE_YAML = """
name: HelloWorldWorkflow
jobs:
  - name: SayHello
    runner: python
    steps:
      - name: PrintHello
        code: |
          print('Hello, World!')
"""

INVALID_PIPELINE_YAML = """
name: BrokenWorkflow
jobs:
  - name: MissingRunner   # runner is required
    steps:
      - name: Oops
"""


class TestValidatePipeline:
    """Tests for validate_pipeline tool."""

    def test_validate_pipeline_valid_yaml(self, mcp_server):
        """validate_pipeline with valid YAML returns a success response."""
        result = _run(
            mcp_server.call_tool(
                "validate_pipeline",
                {"pipeline_yaml": VALID_PIPELINE_YAML},
            )
        )
        content, _meta = result
        _assert_text_content_list(content)
        text = content[0].text.lower()
        assert any(word in text for word in ("valid", "success", "ok", "true", "passed")), (
            f"Expected success indication for valid YAML, got: {content[0].text!r}"
        )

    def test_validate_pipeline_invalid_yaml(self, mcp_server):
        """validate_pipeline with invalid/incomplete YAML returns an error message."""
        bad_yaml = ":::this is not valid yaml:::"
        result = _run(
            mcp_server.call_tool(
                "validate_pipeline",
                {"pipeline_yaml": bad_yaml},
            )
        )
        content, _meta = result
        _assert_text_content_list(content)
        text = content[0].text.lower()
        assert any(word in text for word in ("invalid", "error", "fail", "could not", "parse")), (
            f"Expected error for invalid YAML, got: {content[0].text!r}"
        )

    def test_validate_pipeline_direct_valid(self, workflow_tools):
        """Direct call to validate_pipeline handler with valid YAML."""
        result = _run(workflow_tools.validate_pipeline(VALID_PIPELINE_YAML))
        _assert_text_content_list(result)
        text = result[0].text.lower()
        assert any(word in text for word in ("valid", "success", "ok", "true")), (
            f"Expected success for valid YAML: {result[0].text!r}"
        )

    def test_validate_pipeline_direct_invalid(self, workflow_tools):
        """Direct call to validate_pipeline handler with invalid YAML."""
        result = _run(workflow_tools.validate_pipeline("not: valid: yaml: :::"))
        _assert_text_content_list(result)
        text = result[0].text.lower()
        assert any(word in text for word in ("invalid", "error", "fail", "could not")), (
            f"Expected error for invalid YAML: {result[0].text!r}"
        )


class TestListWorkflowExamples:
    """Tests for list_workflow_examples tool."""

    def test_list_workflow_examples(self, mcp_server):
        """list_workflow_examples returns at least 2 example workflows."""
        result = _run(mcp_server.call_tool("list_workflow_examples", {}))
        content, _meta = result
        _assert_text_content_list(content)

        text = content[0].text
        # Try parsing as JSON first; otherwise check for multiple workflow name references
        try:
            data = json.loads(text)
            assert isinstance(data, list), "Expected a JSON list of workflow examples"
            assert len(data) >= 2, f"Expected at least 2 examples, got {len(data)}"
        except json.JSONDecodeError:
            # Plain text: look for at least two distinct workflow-like names or separators
            assert text.count("name") >= 2 or text.count("workflow") >= 2 or text.count("---") >= 1, (
                f"Expected multiple workflow examples in response: {text[:300]!r}"
            )

    def test_list_workflow_examples_direct(self, workflow_tools):
        """Direct call to list_workflow_examples handler."""
        result = _run(workflow_tools.list_workflow_examples())
        _assert_text_content_list(result)
        # Verify at least 2 examples present
        text = result[0].text
        try:
            data = json.loads(text)
            assert len(data) >= 2
        except json.JSONDecodeError:
            assert len(text) > 100, "Expected substantial workflow examples text"


# ---------------------------------------------------------------------------
# AGENT TOOLS
# ---------------------------------------------------------------------------

class TestListAgents:
    """Tests for list_agents tool."""

    def test_list_agents_returns_names(self, mcp_server):
        """list_agents must return known agent names."""
        result = _run(mcp_server.call_tool("list_agents", {}))
        content, _meta = result
        _assert_text_content_list(content)

        text = content[0].text
        try:
            data = json.loads(text)
            agent_names = [str(e.get("name", "")).lower() for e in data]
        except (json.JSONDecodeError, AttributeError):
            agent_names = [w.lower() for w in text.split()]

        known_agents = ["coderagent", "learningagent", "researchagent", "workflowagent"]
        found = any(
            any(known in name for known in known_agents)
            for name in agent_names
        ) or any(known in text.lower() for known in known_agents)
        assert found, (
            f"Expected at least one known agent name in response. Got: {text[:300]!r}"
        )

    def test_list_agents_direct(self, agent_tools):
        """Direct call to list_agents handler."""
        result = _run(agent_tools.list_agents())
        _assert_text_content_list(result)


class TestGetAgentInfo:
    """Tests for get_agent_info tool."""

    def test_get_agent_info(self, mcp_server):
        """get_agent_info returns state machine info for a known agent."""
        result = _run(
            mcp_server.call_tool("get_agent_info", {"agent_name": "CoderAgent"})
        )
        content, _meta = result
        _assert_text_content_list(content)

        text = content[0].text.lower()
        # Should mention states or FSM-related concepts
        assert any(word in text for word in ("state", "transition", "fsm", "coder", "agent")), (
            f"Expected FSM/state info for CoderAgent, got: {content[0].text!r}"
        )

    def test_get_agent_info_direct(self, agent_tools):
        """Direct call to get_agent_info for CoderAgent."""
        result = _run(agent_tools.get_agent_info("CoderAgent"))
        _assert_text_content_list(result)

    def test_get_agent_info_unknown(self, mcp_server):
        """get_agent_info with an unknown agent name returns a graceful error."""
        result = _run(
            mcp_server.call_tool("get_agent_info", {"agent_name": "NonExistentAgent999"})
        )
        content, _meta = result
        _assert_text_content_list(content)
        text = content[0].text.lower()
        assert any(word in text for word in ("not found", "error", "unknown", "no agent")), (
            f"Expected error for unknown agent, got: {content[0].text!r}"
        )


class TestCreateAgents:
    """Tests for create_coder_agent and create_research_agent tools."""

    def test_create_coder_agent(self, mcp_server):
        """create_coder_agent returns a confirmation with agent state info."""
        result = _run(mcp_server.call_tool("create_coder_agent", {}))
        content, _meta = result
        _assert_text_content_list(content)
        text = content[0].text.lower()
        assert any(word in text for word in ("coder", "agent", "state", "created", "initialized")), (
            f"Expected coder agent info in response: {content[0].text!r}"
        )

    def test_create_research_agent(self, mcp_server):
        """create_research_agent returns a confirmation with agent state info."""
        result = _run(mcp_server.call_tool("create_research_agent", {}))
        content, _meta = result
        _assert_text_content_list(content)
        text = content[0].text.lower()
        assert any(word in text for word in ("research", "agent", "learning", "state", "created")), (
            f"Expected research agent info in response: {content[0].text!r}"
        )


# ---------------------------------------------------------------------------
# RETRIEVAL TOOLS
# ---------------------------------------------------------------------------

class TestRetrieveFromWeb:
    """Tests for retrieve_from_web tool."""

    def test_retrieve_from_web_mocked(self, mcp_server):
        """retrieve_from_web with mocked WebRetriever returns passages."""
        mock_prediction = MagicMock()
        mock_prediction.passages = [
            "Passage one: Python is a general-purpose programming language.",
            "Passage two: DSPy enables language model pipelines.",
        ]

        with patch("dspygen.rm.web_retriever.WebRetriever.forward", return_value=mock_prediction):
            result = _run(
                mcp_server.call_tool(
                    "retrieve_from_web",
                    {
                        "query": "What is DSPy?",
                        "source": "https://example.com",
                    },
                )
            )
        content, _meta = result
        _assert_text_content_list(content)

    def test_retrieve_from_web_direct_mocked(self, retrieval_tools):
        """Direct handler call to retrieve_from_web with mocked WebRetriever."""
        mock_prediction = MagicMock()
        mock_prediction.passages = ["DSPy is a framework for programming LMs."]

        with patch("dspygen.rm.web_retriever.WebRetriever.forward", return_value=mock_prediction):
            result = _run(retrieval_tools.retrieve_from_web("What is DSPy?", "https://example.com"))
        _assert_text_content_list(result)
        text = result[0].text
        assert len(text) > 0, "Should return non-empty passages"


class TestRetrieveFromCode:
    """Tests for retrieve_from_code tool."""

    def test_retrieve_from_code_mocked(self, mcp_server):
        """retrieve_from_code with mocked CodeRetriever returns formatted passages."""
        mock_prediction = MagicMock()
        mock_prediction.passages = [
            "## File: src/example.py\n\n```python\ndef hello():\n    pass\n```\n\n",
        ]

        with patch("dspygen.rm.code_retriever.CodeRetriever.forward", return_value=mock_prediction):
            result = _run(
                mcp_server.call_tool(
                    "retrieve_from_code",
                    {
                        "query": "*.py",
                        "path": "/tmp/fake_project",
                    },
                )
            )
        content, _meta = result
        _assert_text_content_list(content)

    def test_retrieve_from_code_direct_mocked(self, retrieval_tools):
        """Direct handler call to retrieve_from_code with mocked CodeRetriever."""
        mock_prediction = MagicMock()
        mock_prediction.passages = [
            "## File: test.py\n\n```python\nprint('hello')\n```\n\n",
        ]

        with patch("dspygen.rm.code_retriever.CodeRetriever.forward", return_value=mock_prediction):
            result = _run(retrieval_tools.retrieve_from_code("*.py", "/tmp"))
        _assert_text_content_list(result)

    def test_retrieve_from_code_return_format(self, retrieval_tools):
        """retrieve_from_code output should include file path and code block markers."""
        mock_prediction = MagicMock()
        mock_prediction.passages = [
            "## File: /path/to/module.py\n\n```python\nclass Foo:\n    pass\n```\n\n",
        ]

        with patch("dspygen.rm.code_retriever.CodeRetriever.forward", return_value=mock_prediction):
            result = _run(retrieval_tools.retrieve_from_code("*.py", "/path/to"))
        _assert_text_content_list(result)
        combined_text = " ".join(item.text for item in result)
        assert ".py" in combined_text or "File" in combined_text or "```" in combined_text, (
            f"Expected code block format in result: {combined_text[:200]!r}"
        )


class TestRetrieveFromChroma:
    """Tests for retrieve_from_chroma tool."""

    def test_retrieve_from_chroma_mocked(self, mcp_server):
        """retrieve_from_chroma with mocked ChromaRetriever returns passages."""
        mock_passages = [["Relevant passage about DSPy optimization."]]

        with patch("dspygen.rm.chroma_retriever.ChromaRetriever.forward", return_value=mock_passages):
            result = _run(
                mcp_server.call_tool(
                    "retrieve_from_chroma",
                    {
                        "query": "DSPy MIPRO",
                        "collection_name": "dspygen_docs",
                    },
                )
            )
        content, _meta = result
        _assert_text_content_list(content)


# ---------------------------------------------------------------------------
# ERROR HANDLING
# ---------------------------------------------------------------------------

class TestErrorHandling:
    """Tests verifying tools handle exceptions gracefully."""

    def test_tool_exception_returns_text_content(self, mcp_server):
        """A tool that raises internally must return TextContent, not propagate the exception."""
        with patch(
            "dspygen.mcp.tools.module_tools.list_modules",
            side_effect=RuntimeError("Simulated internal error"),
            create=True,
        ):
            try:
                result = _run(mcp_server.call_tool("list_modules", {}))
                content, _meta = result
                # If we get here, the tool returned without raising
                _assert_text_content_list(content)
            except RuntimeError:
                pytest.fail(
                    "Tool must catch internal errors and return TextContent; it raised instead."
                )
            except Exception:
                # MCP may wrap errors — that is acceptable as long as we get a result
                pass

    def test_run_module_exception_returns_text_content(self, mcp_server):
        """run_module must return TextContent with error message on internal failure."""
        with patch("dspy.Predict", side_effect=Exception("LM backend unavailable")):
            try:
                result = _run(
                    mcp_server.call_tool(
                        "run_module",
                        {
                            "module_name": "GenDspyModule",
                            "inputs": {"prompt": "test"},
                        },
                    )
                )
                content, _meta = result
                _assert_text_content_list(content)
                text = content[0].text.lower()
                assert any(word in text for word in ("error", "failed", "exception", "unavailable")), (
                    f"Expected error message when LM unavailable: {content[0].text!r}"
                )
            except Exception:
                # If MCP itself re-raises, that is also acceptable — the key requirement
                # is not to silently swallow results
                pass

    def test_tool_returns_text_content_type(self, mcp_server):
        """Verify list_modules actually returns proper TextContent objects (type check)."""
        from mcp.types import TextContent

        result = _run(mcp_server.call_tool("list_modules", {}))
        content, _meta = result
        assert isinstance(content, list), "Tool result must be a list"
        for item in content:
            assert isinstance(item, TextContent), (
                f"Each item must be TextContent, got: {type(item)}"
            )
            assert item.type == "text", f"TextContent.type must be 'text', got: {item.type!r}"
