"""
Formatting utilities for the TAGEE UI layer.

Pure functions that transform raw data into display-ready strings.
No side effects; safe to call from tests without any setup.
"""

from __future__ import annotations

from typing import List


def format_topic_header(topic_name: str, index: int, total: int) -> str:
    """Return a header string for a topic display.

    Example:
        >>> format_topic_header("The Water Cycle", 1, 3)
        'Topic 1/3: The Water Cycle'
    """
    return f"Topic {index}/{total}: {topic_name}"


def format_question(
    question_text: str,
    options: List[str],
    question_number: int,
) -> str:
    """Return a formatted multiple-choice question block.

    Example output::

        Q1: What is H2O?
          A. Water
          B. Oxygen
    """
    lines = [f"Q{question_number}: {question_text}"]
    for option in options:
        lines.append(f"  {option}")
    return "\n".join(lines)


def format_score(score: int, total: int) -> str:
    """Return a human-readable score string.

    Example:
        >>> format_score(3, 5)
        'Score: 3/5 (60.0%)'
    """
    if total == 0:
        return "Score: 0/0 (0.0%)"
    pct = (score / total) * 100
    return f"Score: {score}/{total} ({pct:.1f}%)"


def format_chat_message(sender: str, text: str) -> str:
    """Return a chat-style message string.

    Example:
        >>> format_chat_message("Tutor", "Hello!")
        '[Tutor]: Hello!'
    """
    return f"[{sender}]: {text}"


def truncate_text(text: str, max_length: int = 200, ellipsis: str = "...") -> str:
    """Shorten *text* to at most *max_length* characters.

    Example:
        >>> truncate_text("Hello world", max_length=5)
        'Hello...'
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + ellipsis


def format_story_node(node_text: str, choices: List[str]) -> str:
    """Render a story node with available choices.

    Example output::

        Once upon a time...

        What do you do?
          [1] Go left
          [2] Go right
    """
    if not choices:
        return node_text
    choice_lines = "\n".join(
        f"  [{i + 1}] {choice}" for i, choice in enumerate(choices)
    )
    return f"{node_text}\n\nWhat do you do?\n{choice_lines}"
