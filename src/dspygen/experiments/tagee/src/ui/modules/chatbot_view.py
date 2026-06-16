"""
Chatbot view module for the TAGEE system.

Provides a pure-Python (no I/O) chatbot controller that wraps a
rule-based response engine and a ChatHistory.  The view is intentionally
kept free of any network or LLM calls so it can be tested deterministically.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from dspygen.experiments.tagee.src.ui.utils.ui_helpers import ChatHistory
from dspygen.experiments.tagee.src.ui.utils.formatting_tools import format_chat_message


# ---------------------------------------------------------------------------
# Simple rule-based response engine
# ---------------------------------------------------------------------------

_DEFAULT_RESPONSES: Dict[str, str] = {
    "hello": "Hi there! I'm your TAGEE tutor. How can I help you today?",
    "help": (
        "I can explain topics, quiz you, or guide you through stories. "
        "Just ask!"
    ),
    "bye": "Goodbye! Keep learning!",
    "who are you": "I'm TAGEE, your Teaching and Adventure Game Educational Engine.",
}

_FALLBACK_RESPONSE = (
    "That's an interesting question. Let me think about that... "
    "Could you rephrase or give me more context?"
)


class ResponseEngine:
    """
    Minimal keyword-based response engine.

    Matches the lowercased user input against a dictionary of known
    prompts and returns the associated reply.  Unknown inputs receive
    the fallback response.

    Can be extended or replaced with an LLM-backed engine without
    changing the ChatbotView interface.
    """

    def __init__(
        self,
        responses: Optional[Dict[str, str]] = None,
        fallback: str = _FALLBACK_RESPONSE,
    ) -> None:
        self._responses: Dict[str, str] = responses or dict(_DEFAULT_RESPONSES)
        self._fallback = fallback

    def add_response(self, trigger: str, reply: str) -> None:
        self._responses[trigger.lower()] = reply

    def respond(self, user_input: str) -> str:
        normalized = user_input.strip().lower()
        # Exact match first
        if normalized in self._responses:
            return self._responses[normalized]
        # Keyword scan
        for keyword, reply in self._responses.items():
            if keyword in normalized:
                return reply
        return self._fallback


# ---------------------------------------------------------------------------
# Chatbot view
# ---------------------------------------------------------------------------

class ChatbotView:
    """
    Controller for the chatbot UI module.

    Accepts user messages, routes them through a ResponseEngine,
    appends both sides of the conversation to a ChatHistory, and
    returns the bot's reply.
    """

    BOT_NAME = "TAGEE Tutor"
    USER_NAME = "Learner"

    def __init__(
        self,
        engine: Optional[ResponseEngine] = None,
        context: str = "",
    ) -> None:
        self.engine = engine or ResponseEngine()
        self.context = context
        self.history = ChatHistory()

    def send_message(self, user_input: str) -> str:
        """
        Process *user_input*, record both sides, and return the bot reply.

        Args:
            user_input: Raw text typed by the learner.

        Returns:
            The bot's response string.
        """
        if not user_input or not user_input.strip():
            return ""
        self.history.add(self.USER_NAME, user_input.strip())
        reply = self.engine.respond(user_input)
        self.history.add(self.BOT_NAME, reply)
        return reply

    def clear_history(self) -> None:
        """Wipe the conversation history."""
        self.history.clear()

    def get_history(self) -> List[str]:
        """Return the formatted conversation history."""
        return self.history.as_formatted_list()

    def message_count(self) -> int:
        """Total messages exchanged (user + bot combined)."""
        return len(self.history)
