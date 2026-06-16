"""
Story view module for the TAGEE system.

Wraps a NarrativeSession and exposes a clean controller API for
presenting and navigating branching stories.
"""

from __future__ import annotations

from typing import List, Optional

from dspygen.experiments.tagee.src.core.narrative_engine import (
    NarrativeEngine,
    NarrativeSession,
    Story,
    StoryGenre,
)
from dspygen.experiments.tagee.src.ui.utils.formatting_tools import (
    format_story_node,
    truncate_text,
)


class StoryView:
    """
    Controller for the story UI module.

    Drives a NarrativeSession, renders each node with its available
    choices, and reports when the story has concluded.
    """

    def __init__(self, session: NarrativeSession) -> None:
        self.session = session

    # ------------------------------------------------------------------
    # Factory helpers
    # ------------------------------------------------------------------

    @classmethod
    def from_story(cls, story: Story) -> "StoryView":
        """Convenience constructor — create a view directly from a Story."""
        return cls(NarrativeSession(story))

    @classmethod
    def build_linear(
        cls,
        title: str,
        passages: List[str],
        genre: StoryGenre = StoryGenre.ADVENTURE,
        author: str = "",
    ) -> "StoryView":
        """
        Build and wrap a simple linear story.

        Each passage is a node with a single 'Continue' choice, except
        the last which is an ending.
        """
        story = NarrativeEngine.build_linear_story(
            title=title, genre=genre, passages=passages, author=author
        )
        return cls.from_story(story)

    # ------------------------------------------------------------------
    # Navigation API
    # ------------------------------------------------------------------

    def render_current(self) -> str:
        """Return the formatted text and choices for the current node."""
        node = self.session.current_node()
        choices = self.session.available_choices()
        return format_story_node(node.text, choices)

    def choose(self, choice_label: str) -> str:
        """
        Advance the story by *choice_label* and return the next node's display.

        Raises ValueError if the choice is not valid.
        """
        self.session.choose(choice_label)
        return self.render_current()

    def is_finished(self) -> bool:
        return self.session.is_finished

    def available_choices(self) -> List[str]:
        return self.session.available_choices()

    # ------------------------------------------------------------------
    # History / summary
    # ------------------------------------------------------------------

    def full_narrative(self, max_chars_per_node: int = 300) -> str:
        """
        Return the story so far as a single string.

        Each visited node's text is separated by a blank line and
        optionally truncated.
        """
        parts = []
        for text in self.session.narrative_so_far():
            parts.append(truncate_text(text, max_chars_per_node))
        return "\n\n---\n\n".join(parts)

    def nodes_visited(self) -> int:
        return self.session.path_length()

    def choices_made(self) -> List[str]:
        return list(self.session.choices_made)

    def story_title(self) -> str:
        return self.session.story.title
