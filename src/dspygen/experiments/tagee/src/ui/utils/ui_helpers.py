"""
UI helper utilities for the TAGEE system.

Higher-level helpers that compose formatting_tools output and manage
common UI patterns such as chat histories, menu rendering, and
input validation.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from dspygen.experiments.tagee.src.ui.utils.formatting_tools import (
    format_chat_message,
    format_score,
    format_story_node,
    format_topic_header,
)


class ChatHistory:
    """
    In-memory chat history for the chatbot view.

    Stores (sender, message) pairs and exposes them as formatted strings.
    """

    def __init__(self) -> None:
        self._messages: List[Tuple[str, str]] = []

    def add(self, sender: str, text: str) -> None:
        self._messages.append((sender, text))

    def as_formatted_list(self) -> List[str]:
        return [format_chat_message(s, t) for s, t in self._messages]

    def as_plain_text(self) -> str:
        return "\n".join(self.as_formatted_list())

    def clear(self) -> None:
        self._messages.clear()

    def __len__(self) -> int:
        return len(self._messages)

    def last_message(self) -> Optional[Tuple[str, str]]:
        if not self._messages:
            return None
        return self._messages[-1]


def build_topic_menu(topic_names: List[str]) -> str:
    """Return a numbered menu of topic names."""
    lines = ["Available topics:"]
    for i, name in enumerate(topic_names, start=1):
        lines.append(f"  {i}. {name}")
    return "\n".join(lines)


def render_quiz_feedback(correct: bool, explanation: str = "") -> str:
    """Return a one-line feedback string for a quiz answer."""
    result = "Correct!" if correct else "Incorrect."
    if explanation:
        return f"{result} {explanation}"
    return result


def compute_letter_grade(percentage: float) -> str:
    """Map a percentage score to a letter grade.

    Grades: A (90+), B (80+), C (70+), D (60+), F (<60).
    """
    if percentage >= 90:
        return "A"
    if percentage >= 80:
        return "B"
    if percentage >= 70:
        return "C"
    if percentage >= 60:
        return "D"
    return "F"


def summarise_results(score: int, total: int, learner_name: str) -> str:
    """Return a multi-line results summary string."""
    score_str = format_score(score, total)
    pct = (score / total * 100) if total else 0.0
    grade = compute_letter_grade(pct)
    lines = [
        f"Results for {learner_name}",
        "-" * 30,
        score_str,
        f"Grade: {grade}",
    ]
    return "\n".join(lines)
