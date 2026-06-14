"""
Narrative engine for the TAGEE system.

Responsible for generating, sequencing, and managing the text-based story
content that wraps educational material in an engaging adventure context.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class StoryGenre(Enum):
    FANTASY = "fantasy"
    SCIENCE_FICTION = "science_fiction"
    MYSTERY = "mystery"
    HISTORICAL = "historical"
    ADVENTURE = "adventure"


@dataclass
class StoryNode:
    """
    A single node in a branching narrative tree.

    Each node has display text and up to two child keys that represent
    choices the learner can make to advance the story.
    """

    node_id: str
    text: str
    choices: Dict[str, str] = field(default_factory=dict)  # label -> next node_id
    educational_note: str = ""
    is_ending: bool = False

    def add_choice(self, label: str, next_node_id: str) -> None:
        """Register a named choice that leads to *next_node_id*."""
        self.choices[label] = next_node_id


@dataclass
class Story:
    """
    A complete branching story composed of interconnected StoryNodes.

    Stories are authored by creating nodes and wiring them together.
    The narrative engine traverses them in response to learner choices.
    """

    title: str
    genre: StoryGenre
    root_node_id: str
    nodes: Dict[str, StoryNode] = field(default_factory=dict)
    author: str = ""
    description: str = ""

    def add_node(self, node: StoryNode) -> None:
        self.nodes[node.node_id] = node

    def get_node(self, node_id: str) -> StoryNode:
        if node_id not in self.nodes:
            raise KeyError(f"Story node '{node_id}' not found.")
        return self.nodes[node_id]

    @property
    def node_count(self) -> int:
        return len(self.nodes)


class NarrativeSession:
    """
    Tracks a learner's traversal through a Story.

    Records each visited node and chosen path so the full narrative
    history is available for replay or review.
    """

    def __init__(self, story: Story) -> None:
        self.story = story
        self.current_node_id: str = story.root_node_id
        self.visited_nodes: List[str] = [story.root_node_id]
        self.choices_made: List[str] = []
        self.is_finished: bool = False

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def current_node(self) -> StoryNode:
        return self.story.get_node(self.current_node_id)

    def available_choices(self) -> List[str]:
        """Return the labels of choices available at the current node."""
        return list(self.current_node().choices.keys())

    def choose(self, choice_label: str) -> StoryNode:
        """
        Advance the story by selecting *choice_label*.

        Returns the newly entered StoryNode.
        Raises ValueError if the choice is not valid at the current node.
        """
        node = self.current_node()
        if choice_label not in node.choices:
            raise ValueError(
                f"Choice '{choice_label}' is not available. "
                f"Valid choices: {list(node.choices.keys())}"
            )
        next_id = node.choices[choice_label]
        self.current_node_id = next_id
        self.visited_nodes.append(next_id)
        self.choices_made.append(choice_label)
        next_node = self.story.get_node(next_id)
        if next_node.is_ending:
            self.is_finished = True
        return next_node

    # ------------------------------------------------------------------
    # History / introspection
    # ------------------------------------------------------------------

    def path_length(self) -> int:
        """Number of nodes visited so far (including the starting node)."""
        return len(self.visited_nodes)

    def narrative_so_far(self) -> List[str]:
        """Return the text of every visited node in order."""
        return [
            self.story.get_node(nid).text for nid in self.visited_nodes
        ]


class NarrativeEngine:
    """
    Factory and registry for Story objects.

    Builds stories from structured data and serves them to NarrativeSessions.
    Also provides helpers for generating simple linear or branching stories
    from topic lists (used by the story_view).
    """

    def __init__(self) -> None:
        self._stories: Dict[str, Story] = {}

    def register_story(self, story: Story) -> None:
        self._stories[story.title] = story

    def get_story(self, title: str) -> Story:
        if title not in self._stories:
            raise KeyError(f"Story '{title}' is not registered.")
        return self._stories[title]

    def list_stories(self) -> List[str]:
        return list(self._stories.keys())

    def start_session(self, story_title: str) -> NarrativeSession:
        """Return a fresh NarrativeSession for the named story."""
        story = self.get_story(story_title)
        return NarrativeSession(story)

    # ------------------------------------------------------------------
    # Story builder helpers
    # ------------------------------------------------------------------

    @staticmethod
    def build_linear_story(
        title: str,
        genre: StoryGenre,
        passages: List[str],
        author: str = "",
    ) -> Story:
        """
        Build a simple story where each passage is a node and there is
        exactly one 'Continue' choice that leads to the next passage.

        The final passage is marked as an ending.
        """
        if not passages:
            raise ValueError("At least one passage is required.")

        story = Story(
            title=title,
            genre=genre,
            root_node_id="node_0",
            author=author,
        )

        for idx, text in enumerate(passages):
            node_id = f"node_{idx}"
            is_last = idx == len(passages) - 1
            node = StoryNode(
                node_id=node_id,
                text=text,
                is_ending=is_last,
            )
            if not is_last:
                node.add_choice("Continue", f"node_{idx + 1}")
            story.add_node(node)

        return story
