"""Unit tests for the TAGEE narrative engine.

Tests cover: StoryGenre, StoryNode, Story, NarrativeSession, and
NarrativeEngine — including node/choice management, session traversal,
history tracking, and static story builders.
"""

from __future__ import annotations

import sys
import os

import pytest

_tagee_root = os.path.join(os.path.dirname(__file__), "..", "..")
_repo_src = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", "..", "src")
sys.path.insert(0, os.path.abspath(_repo_src))
sys.path.insert(0, os.path.abspath(os.path.join(_tagee_root, "src", "core")))

from narrative_engine import (
    NarrativeEngine,
    NarrativeSession,
    Story,
    StoryGenre,
    StoryNode,
)


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------


def make_node(
    node_id: str = "n1",
    text: str = "You stand at the crossroads.",
    is_ending: bool = False,
) -> StoryNode:
    return StoryNode(node_id=node_id, text=text, is_ending=is_ending)


def make_two_node_story(title: str = "Quick Tale") -> Story:
    """Build start -> ending story."""
    start = make_node("start", "The beginning.")
    end = make_node("end", "The end.", is_ending=True)
    start.add_choice("Go on", "end")

    story = Story(title=title, genre=StoryGenre.ADVENTURE, root_node_id="start")
    story.add_node(start)
    story.add_node(end)
    return story


@pytest.fixture()
def two_node_story() -> Story:
    return make_two_node_story()


@pytest.fixture()
def narrative_engine() -> NarrativeEngine:
    """NarrativeEngine with one registered story."""
    ne = NarrativeEngine()
    ne.register_story(make_two_node_story())
    return ne


@pytest.fixture()
def session(two_node_story: Story) -> NarrativeSession:
    return NarrativeSession(story=two_node_story)


# ---------------------------------------------------------------------------
# StoryGenre tests
# ---------------------------------------------------------------------------


class TestStoryGenre:
    """Tests for the StoryGenre enum."""

    def test_all_genres_present(self) -> None:
        values = {g.value for g in StoryGenre}
        expected = {"fantasy", "science_fiction", "mystery", "historical", "adventure"}
        assert values == expected

    def test_fantasy_value(self) -> None:
        assert StoryGenre.FANTASY.value == "fantasy"

    def test_mystery_value(self) -> None:
        assert StoryGenre.MYSTERY.value == "mystery"


# ---------------------------------------------------------------------------
# StoryNode tests
# ---------------------------------------------------------------------------


class TestStoryNode:
    """Tests for the StoryNode dataclass."""

    def test_valid_creation(self) -> None:
        node = make_node()
        assert node.node_id == "n1"
        assert node.is_ending is False
        assert node.choices == {}

    def test_ending_flag(self) -> None:
        node = make_node(is_ending=True)
        assert node.is_ending is True

    def test_add_choice(self) -> None:
        node = make_node()
        node.add_choice("Go north", "cave")
        assert "Go north" in node.choices
        assert node.choices["Go north"] == "cave"

    def test_add_multiple_choices(self) -> None:
        node = make_node()
        node.add_choice("North", "cave")
        node.add_choice("South", "meadow")
        assert len(node.choices) == 2

    def test_educational_note_default_empty(self) -> None:
        node = make_node()
        assert node.educational_note == ""

    def test_educational_note_set(self) -> None:
        node = StoryNode(node_id="n1", text="...", educational_note="Plants are green.")
        assert node.educational_note == "Plants are green."

    def test_overwrite_choice(self) -> None:
        node = make_node()
        node.add_choice("Go", "dest_1")
        node.add_choice("Go", "dest_2")  # overwrite
        assert node.choices["Go"] == "dest_2"


# ---------------------------------------------------------------------------
# Story tests
# ---------------------------------------------------------------------------


class TestStory:
    """Tests for the Story dataclass."""

    def test_valid_creation(self) -> None:
        s = Story(title="Epic", genre=StoryGenre.FANTASY, root_node_id="n1")
        assert s.title == "Epic"
        assert s.node_count == 0

    def test_add_node(self) -> None:
        s = Story(title="T", genre=StoryGenre.MYSTERY, root_node_id="start")
        s.add_node(make_node("start"))
        assert s.node_count == 1

    def test_get_node_found(self) -> None:
        s = Story(title="T", genre=StoryGenre.MYSTERY, root_node_id="start")
        node = make_node("start")
        s.add_node(node)
        assert s.get_node("start") is node

    def test_get_node_missing_raises(self) -> None:
        s = Story(title="T", genre=StoryGenre.MYSTERY, root_node_id="start")
        with pytest.raises(KeyError, match="ghost"):
            s.get_node("ghost")

    def test_node_count_increases(self) -> None:
        s = Story(title="T", genre=StoryGenre.ADVENTURE, root_node_id="n1")
        for i in range(5):
            s.add_node(make_node(f"n{i}"))
        assert s.node_count == 5

    def test_default_author_empty(self) -> None:
        s = Story(title="T", genre=StoryGenre.FANTASY, root_node_id="n1")
        assert s.author == ""

    def test_custom_author(self) -> None:
        s = Story(title="T", genre=StoryGenre.FANTASY, root_node_id="n1", author="Tolkien")
        assert s.author == "Tolkien"


# ---------------------------------------------------------------------------
# NarrativeSession tests
# ---------------------------------------------------------------------------


class TestNarrativeSession:
    """Tests for NarrativeSession traversal and history."""

    def test_initial_current_node(self, session: NarrativeSession, two_node_story: Story) -> None:
        assert session.current_node().node_id == two_node_story.root_node_id

    def test_initial_visited_nodes(self, session: NarrativeSession) -> None:
        assert session.visited_nodes == ["start"]

    def test_initial_choices_made_empty(self, session: NarrativeSession) -> None:
        assert session.choices_made == []

    def test_initial_is_not_finished(self, session: NarrativeSession) -> None:
        assert session.is_finished is False

    def test_initial_path_length(self, session: NarrativeSession) -> None:
        assert session.path_length() == 1

    def test_available_choices_lists_labels(self, session: NarrativeSession) -> None:
        choices = session.available_choices()
        assert "Go on" in choices

    def test_choose_valid_choice(self, session: NarrativeSession) -> None:
        next_node = session.choose("Go on")
        assert next_node.node_id == "end"

    def test_choose_updates_current_node(self, session: NarrativeSession) -> None:
        session.choose("Go on")
        assert session.current_node().node_id == "end"

    def test_choose_records_choice(self, session: NarrativeSession) -> None:
        session.choose("Go on")
        assert "Go on" in session.choices_made

    def test_choose_updates_visited_nodes(self, session: NarrativeSession) -> None:
        session.choose("Go on")
        assert "end" in session.visited_nodes

    def test_choose_path_length_increases(self, session: NarrativeSession) -> None:
        session.choose("Go on")
        assert session.path_length() == 2

    def test_choose_sets_is_finished_on_ending(self, session: NarrativeSession) -> None:
        session.choose("Go on")
        assert session.is_finished is True

    def test_choose_invalid_label_raises(self, session: NarrativeSession) -> None:
        with pytest.raises(ValueError, match="not available"):
            session.choose("Fly away")

    def test_narrative_so_far_initial(self, session: NarrativeSession) -> None:
        texts = session.narrative_so_far()
        assert len(texts) == 1
        assert texts[0] == "The beginning."

    def test_narrative_so_far_after_choice(self, session: NarrativeSession) -> None:
        session.choose("Go on")
        texts = session.narrative_so_far()
        assert len(texts) == 2
        assert "The end." in texts

    def test_available_choices_at_ending_empty(self, session: NarrativeSession) -> None:
        session.choose("Go on")
        # Ending node has no choices registered
        assert session.available_choices() == []


# ---------------------------------------------------------------------------
# NarrativeEngine tests
# ---------------------------------------------------------------------------


class TestNarrativeEngine:
    """Tests for the NarrativeEngine registry and session factory."""

    def test_register_and_list_stories(self, narrative_engine: NarrativeEngine) -> None:
        titles = narrative_engine.list_stories()
        assert "Quick Tale" in titles

    def test_get_story_found(self, narrative_engine: NarrativeEngine) -> None:
        story = narrative_engine.get_story("Quick Tale")
        assert story.title == "Quick Tale"

    def test_get_story_missing_raises(self, narrative_engine: NarrativeEngine) -> None:
        with pytest.raises(KeyError, match="Ghost"):
            narrative_engine.get_story("Ghost")

    def test_register_multiple_stories(self) -> None:
        ne = NarrativeEngine()
        ne.register_story(make_two_node_story("A"))
        ne.register_story(make_two_node_story("B"))
        assert len(ne.list_stories()) == 2

    def test_start_session_returns_narrative_session(self, narrative_engine: NarrativeEngine) -> None:
        session = narrative_engine.start_session("Quick Tale")
        assert isinstance(session, NarrativeSession)

    def test_start_session_at_root_node(self, narrative_engine: NarrativeEngine) -> None:
        session = narrative_engine.start_session("Quick Tale")
        assert session.current_node().node_id == "start"

    def test_start_session_unknown_title_raises(self, narrative_engine: NarrativeEngine) -> None:
        with pytest.raises(KeyError):
            narrative_engine.start_session("Unknown")

    def test_overwrite_story_registration(self) -> None:
        """Registering the same title twice overwrites the earlier story."""
        ne = NarrativeEngine()
        story_v1 = make_two_node_story("My Story")
        story_v2 = make_two_node_story("My Story")
        ne.register_story(story_v1)
        ne.register_story(story_v2)
        # Only one story under this title
        assert len(ne.list_stories()) == 1


# ---------------------------------------------------------------------------
# NarrativeEngine.build_linear_story tests
# ---------------------------------------------------------------------------


class TestBuildLinearStory:
    """Tests for the static build_linear_story helper."""

    def test_creates_story_with_correct_title(self) -> None:
        story = NarrativeEngine.build_linear_story("Epic", StoryGenre.FANTASY, ["Start", "End"])
        assert story.title == "Epic"

    def test_creates_correct_number_of_nodes(self) -> None:
        story = NarrativeEngine.build_linear_story("T", StoryGenre.FANTASY, ["A", "B", "C"])
        assert story.node_count == 3

    def test_root_node_id_is_node_0(self) -> None:
        story = NarrativeEngine.build_linear_story("T", StoryGenre.ADVENTURE, ["Intro"])
        assert story.root_node_id == "node_0"

    def test_last_node_is_ending(self) -> None:
        story = NarrativeEngine.build_linear_story("T", StoryGenre.FANTASY, ["A", "B"])
        assert story.get_node("node_1").is_ending is True

    def test_non_last_node_not_ending(self) -> None:
        story = NarrativeEngine.build_linear_story("T", StoryGenre.FANTASY, ["A", "B"])
        assert story.get_node("node_0").is_ending is False

    def test_continue_choice_on_non_last_nodes(self) -> None:
        story = NarrativeEngine.build_linear_story("T", StoryGenre.FANTASY, ["A", "B"])
        node_0 = story.get_node("node_0")
        assert "Continue" in node_0.choices

    def test_no_choice_on_last_node(self) -> None:
        story = NarrativeEngine.build_linear_story("T", StoryGenre.FANTASY, ["A", "B"])
        node_1 = story.get_node("node_1")
        assert node_1.choices == {}

    def test_single_passage_story(self) -> None:
        story = NarrativeEngine.build_linear_story("T", StoryGenre.MYSTERY, ["Only passage."])
        assert story.node_count == 1
        root = story.get_node("node_0")
        assert root.is_ending is True
        assert root.choices == {}

    def test_empty_passages_raises(self) -> None:
        with pytest.raises(ValueError, match="[Aa]t least one passage"):
            NarrativeEngine.build_linear_story("T", StoryGenre.MYSTERY, [])

    def test_author_stored(self) -> None:
        story = NarrativeEngine.build_linear_story(
            "T", StoryGenre.HISTORICAL, ["Intro"], author="Herodotus"
        )
        assert story.author == "Herodotus"

    def test_traversal_reaches_end(self) -> None:
        """Walk through a 3-passage linear story via NarrativeSession."""
        story = NarrativeEngine.build_linear_story(
            "Walk", StoryGenre.ADVENTURE, ["Step 1", "Step 2", "Step 3"]
        )
        session = NarrativeSession(story=story)
        assert not session.is_finished
        session.choose("Continue")
        assert not session.is_finished
        session.choose("Continue")
        assert session.is_finished

    def test_genre_preserved(self) -> None:
        story = NarrativeEngine.build_linear_story("T", StoryGenre.SCIENCE_FICTION, ["Warp!"])
        assert story.genre == StoryGenre.SCIENCE_FICTION
