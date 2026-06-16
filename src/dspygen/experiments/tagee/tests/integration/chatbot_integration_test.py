"""
Integration tests for the TAGEE chatbot feature.

Tests verify that the ChatbotView, ResponseEngine, and ChatHistory
work together correctly across realistic multi-turn conversation
workflows.
"""

from __future__ import annotations

import pytest

from dspygen.experiments.tagee.src.ui.modules.chatbot_view import (
    ChatbotView,
    ResponseEngine,
)
from dspygen.experiments.tagee.src.ui.utils.ui_helpers import ChatHistory
from dspygen.experiments.tagee.src.ui.utils.formatting_tools import format_chat_message


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def default_view() -> ChatbotView:
    """A ChatbotView with the default ResponseEngine and no context."""
    return ChatbotView()


@pytest.fixture()
def custom_engine() -> ResponseEngine:
    """A ResponseEngine seeded with domain-specific responses."""
    engine = ResponseEngine()
    engine.add_response("photosynthesis", "Photosynthesis is how plants make food using sunlight.")
    engine.add_response("gravity", "Gravity is the force that attracts objects with mass toward each other.")
    engine.add_response("quiz", "Sure! Let's start a quiz on the current topic.")
    return engine


@pytest.fixture()
def science_view(custom_engine: ResponseEngine) -> ChatbotView:
    """A ChatbotView configured for science tutoring."""
    return ChatbotView(engine=custom_engine, context="science tutoring")


# ---------------------------------------------------------------------------
# Integration tests
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestChatbotGreetingWorkflow:
    """A learner opens the chatbot and exchanges a greeting."""

    def test_single_message_produces_reply(self, default_view: ChatbotView) -> None:
        reply = default_view.send_message("hello")
        assert reply, "Bot should always return a non-empty reply."
        assert isinstance(reply, str)

    def test_greeting_reply_is_welcoming(self, default_view: ChatbotView) -> None:
        reply = default_view.send_message("hello")
        # The default engine maps "hello" to a welcoming phrase
        assert "hi" in reply.lower() or "hello" in reply.lower() or "tutor" in reply.lower()

    def test_history_records_both_sides_after_greeting(
        self, default_view: ChatbotView
    ) -> None:
        default_view.send_message("hello")
        history = default_view.get_history()
        # Exactly 2 entries: user + bot
        assert len(history) == 2
        assert "Learner" in history[0]
        assert "TAGEE Tutor" in history[1]

    def test_message_count_reflects_both_sides(self, default_view: ChatbotView) -> None:
        assert default_view.message_count() == 0
        default_view.send_message("hello")
        assert default_view.message_count() == 2


@pytest.mark.integration
class TestMultiTurnConversation:
    """A learner sends several messages in sequence."""

    def test_three_turn_conversation_history_length(
        self, default_view: ChatbotView
    ) -> None:
        for msg in ("hello", "help", "bye"):
            default_view.send_message(msg)
        # 3 user messages + 3 bot replies = 6 total
        assert default_view.message_count() == 6

    def test_conversation_history_preserves_order(
        self, default_view: ChatbotView
    ) -> None:
        messages = ["hello", "who are you", "bye"]
        for msg in messages:
            default_view.send_message(msg)
        history = default_view.get_history()
        # Odd indices (0, 2, 4) are user messages; even indices (1, 3, 5) are bot
        user_entries = [h for h in history if "Learner" in h]
        assert len(user_entries) == 3
        assert "hello" in user_entries[0]
        assert "who are you" in user_entries[1]
        assert "bye" in user_entries[2]

    def test_clear_history_resets_conversation(
        self, default_view: ChatbotView
    ) -> None:
        default_view.send_message("hello")
        default_view.clear_history()
        assert default_view.message_count() == 0
        assert default_view.get_history() == []

    def test_conversation_continues_after_clear(
        self, default_view: ChatbotView
    ) -> None:
        default_view.send_message("hello")
        default_view.clear_history()
        reply = default_view.send_message("help")
        assert reply
        assert default_view.message_count() == 2


@pytest.mark.integration
class TestDomainSpecificChatbot:
    """A science-tutoring chatbot answers curriculum questions."""

    def test_photosynthesis_query_returns_relevant_reply(
        self, science_view: ChatbotView
    ) -> None:
        reply = science_view.send_message("tell me about photosynthesis")
        assert "photosynthesis" in reply.lower() or "plants" in reply.lower()

    def test_gravity_query_returns_relevant_reply(
        self, science_view: ChatbotView
    ) -> None:
        reply = science_view.send_message("what is gravity?")
        assert "gravity" in reply.lower() or "force" in reply.lower()

    def test_unknown_topic_returns_fallback(
        self, science_view: ChatbotView
    ) -> None:
        reply = science_view.send_message("tell me about quantum entanglement")
        # The custom engine has no entry for this; fallback should fire
        assert reply, "Fallback response must be non-empty."
        assert isinstance(reply, str)

    def test_quiz_request_acknowledged(self, science_view: ChatbotView) -> None:
        reply = science_view.send_message("I want a quiz")
        assert "quiz" in reply.lower()


@pytest.mark.integration
class TestChatbotAndHistoryIntegration:
    """ChatbotView and ChatHistory work together correctly."""

    def test_history_format_matches_expected_pattern(
        self, default_view: ChatbotView
    ) -> None:
        default_view.send_message("hello")
        history = default_view.get_history()
        for entry in history:
            # Each entry must be wrapped in [Sender]: text
            assert entry.startswith("["), f"Entry should start with '[': {entry!r}"
            assert "]: " in entry, f"Entry missing ']: ': {entry!r}"

    def test_empty_input_is_ignored(self, default_view: ChatbotView) -> None:
        reply = default_view.send_message("   ")
        assert reply == ""
        assert default_view.message_count() == 0

    def test_multiple_sessions_have_independent_histories(self) -> None:
        view_a = ChatbotView()
        view_b = ChatbotView()
        view_a.send_message("hello")
        view_a.send_message("bye")
        view_b.send_message("who are you")
        assert view_a.message_count() == 4
        assert view_b.message_count() == 2

    def test_last_bot_reply_appears_at_end_of_history(
        self, default_view: ChatbotView
    ) -> None:
        default_view.send_message("hello")
        reply = default_view.send_message("help")
        history = default_view.get_history()
        # The last history entry should contain the last bot reply text
        assert reply in history[-1]


@pytest.mark.integration
class TestResponseEngineExtension:
    """The response engine can be extended and the view reflects additions."""

    def test_dynamically_added_response_is_returned(self) -> None:
        engine = ResponseEngine()
        engine.add_response("ecosystems", "Ecosystems are communities of living organisms.")
        view = ChatbotView(engine=engine)
        reply = view.send_message("tell me about ecosystems")
        assert "ecosystem" in reply.lower() or "living" in reply.lower()

    def test_overwritten_response_replaces_previous(self) -> None:
        engine = ResponseEngine()
        engine.add_response("hello", "First greeting.")
        engine.add_response("hello", "Updated greeting!")
        view = ChatbotView(engine=engine)
        reply = view.send_message("hello")
        assert reply == "Updated greeting!"

    def test_context_attribute_is_stored(self) -> None:
        view = ChatbotView(context="biology class")
        assert view.context == "biology class"
