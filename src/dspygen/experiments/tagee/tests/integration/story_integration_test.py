"""
Integration tests for the TAGEE story feature.

Tests verify that StoryView, NarrativeEngine, NarrativeSession, Story,
and StoryNode all work together across end-to-end storytelling workflows.
"""

from __future__ import annotations

import pytest

from dspygen.experiments.tagee.src.core.narrative_engine import (
    NarrativeEngine,
    NarrativeSession,
    Story,
    StoryGenre,
    StoryNode,
)
from dspygen.experiments.tagee.src.ui.modules.story_view import StoryView


# ---------------------------------------------------------------------------
# Story builders / fixtures
# ---------------------------------------------------------------------------


def make_branching_story() -> Story:
    """
    Build a small branching story with two possible endings:

        ROOT --> "Explore cave" --> CAVE (ending)
             --> "Follow river" --> RIVER --> "Cross bridge" --> BRIDGE_END (ending)
                                          --> "Wait by bank"  --> WAIT_END (ending)
    """
    story = Story(
        title="The Lost Explorer",
        genre=StoryGenre.ADVENTURE,
        root_node_id="root",
        author="TAGEE Test Suite",
        description="A short adventure with branching paths.",
    )

    root = StoryNode(
        node_id="root",
        text="You find yourself at a fork in the path. A cave entrance yawns to the left; a river glitters to the right.",
    )
    root.add_choice("Explore cave", "cave")
    root.add_choice("Follow river", "river")

    cave = StoryNode(
        node_id="cave",
        text="You enter the cave and discover ancient paintings. The path ends here.",
        is_ending=True,
        educational_note="Cave paintings are an early form of human communication.",
    )

    river = StoryNode(
        node_id="river",
        text="You follow the river downstream and reach a bridge. What do you do?",
    )
    river.add_choice("Cross bridge", "bridge_end")
    river.add_choice("Wait by bank", "wait_end")

    bridge_end = StoryNode(
        node_id="bridge_end",
        text="You cross the bridge and find a friendly village on the other side. Your adventure ends happily.",
        is_ending=True,
    )

    wait_end = StoryNode(
        node_id="wait_end",
        text="You wait patiently. A raft floats by and carries you safely downstream. Journey complete.",
        is_ending=True,
    )

    for node in (root, cave, river, bridge_end, wait_end):
        story.add_node(node)

    return story


def make_linear_passages() -> list[str]:
    return [
        "Once upon a time, a young scientist discovered a hidden laboratory.",
        "Inside, she found equations that could change the world.",
        "She spent years decoding them, and eventually unlocked the secret of clean energy.",
        "Her discovery brought light and warmth to millions of people. The End.",
    ]


@pytest.fixture()
def branching_story() -> Story:
    return make_branching_story()


@pytest.fixture()
def branching_view(branching_story: Story) -> StoryView:
    return StoryView.from_story(branching_story)


@pytest.fixture()
def linear_view() -> StoryView:
    return StoryView.build_linear(
        title="The Young Scientist",
        passages=make_linear_passages(),
        genre=StoryGenre.SCIENCE_FICTION,
        author="TAGEE Test Suite",
    )


@pytest.fixture()
def narrative_engine(branching_story: Story) -> NarrativeEngine:
    engine = NarrativeEngine()
    engine.register_story(branching_story)
    return engine


# ---------------------------------------------------------------------------
# Integration tests
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestLinearStoryWorkflow:
    """A linear story progresses node-by-node until it ends."""

    def test_initial_render_shows_first_passage(
        self, linear_view: StoryView
    ) -> None:
        display = linear_view.render_current()
        assert "young scientist" in display.lower()

    def test_initial_render_shows_continue_choice(
        self, linear_view: StoryView
    ) -> None:
        display = linear_view.render_current()
        assert "Continue" in display

    def test_story_is_not_finished_at_start(
        self, linear_view: StoryView
    ) -> None:
        assert linear_view.is_finished() is False

    def test_advancing_through_all_passages(
        self, linear_view: StoryView
    ) -> None:
        for _ in range(3):  # 4 passages -> 3 choices to advance
            assert linear_view.is_finished() is False
            linear_view.choose("Continue")
        assert linear_view.is_finished() is True

    def test_final_passage_contains_the_end(
        self, linear_view: StoryView
    ) -> None:
        for _ in range(3):
            linear_view.choose("Continue")
        display = linear_view.render_current()
        assert "end" in display.lower() or "millions" in display.lower()

    def test_nodes_visited_increments_with_each_choice(
        self, linear_view: StoryView
    ) -> None:
        assert linear_view.nodes_visited() == 1
        linear_view.choose("Continue")
        assert linear_view.nodes_visited() == 2

    def test_choices_made_records_each_choice(
        self, linear_view: StoryView
    ) -> None:
        linear_view.choose("Continue")
        linear_view.choose("Continue")
        assert linear_view.choices_made() == ["Continue", "Continue"]

    def test_full_narrative_joins_visited_nodes(
        self, linear_view: StoryView
    ) -> None:
        linear_view.choose("Continue")
        narrative = linear_view.full_narrative()
        # Should contain text from both visited nodes
        assert "scientist" in narrative.lower()
        assert "equations" in narrative.lower()

    def test_story_title_is_accessible(self, linear_view: StoryView) -> None:
        assert linear_view.story_title() == "The Young Scientist"


@pytest.mark.integration
class TestBranchingStoryWorkflow:
    """Choices in a branching story lead to different endings."""

    def test_root_node_shows_two_choices(
        self, branching_view: StoryView
    ) -> None:
        choices = branching_view.available_choices()
        assert len(choices) == 2
        assert "Explore cave" in choices
        assert "Follow river" in choices

    def test_cave_path_leads_to_ending(
        self, branching_view: StoryView
    ) -> None:
        branching_view.choose("Explore cave")
        assert branching_view.is_finished() is True

    def test_cave_ending_text_is_correct(
        self, branching_view: StoryView
    ) -> None:
        display = branching_view.choose("Explore cave")
        assert "cave" in display.lower() or "paintings" in display.lower()

    def test_river_path_opens_further_choices(
        self, branching_view: StoryView
    ) -> None:
        branching_view.choose("Follow river")
        assert branching_view.is_finished() is False
        choices = branching_view.available_choices()
        assert "Cross bridge" in choices
        assert "Wait by bank" in choices

    def test_river_then_bridge_reaches_happy_ending(
        self, branching_view: StoryView
    ) -> None:
        branching_view.choose("Follow river")
        display = branching_view.choose("Cross bridge")
        assert branching_view.is_finished() is True
        assert "village" in display.lower() or "happily" in display.lower()

    def test_river_then_wait_reaches_raft_ending(
        self, branching_view: StoryView
    ) -> None:
        branching_view.choose("Follow river")
        display = branching_view.choose("Wait by bank")
        assert branching_view.is_finished() is True
        assert "raft" in display.lower() or "downstream" in display.lower()

    def test_invalid_choice_raises_value_error(
        self, branching_view: StoryView
    ) -> None:
        with pytest.raises(ValueError, match="not available"):
            branching_view.choose("Fly away")

    def test_choices_made_list_records_path(
        self, branching_view: StoryView
    ) -> None:
        branching_view.choose("Follow river")
        branching_view.choose("Cross bridge")
        assert branching_view.choices_made() == ["Follow river", "Cross bridge"]

    def test_different_paths_have_different_node_counts(self) -> None:
        # Cave path: root + cave = 2 nodes
        story = make_branching_story()
        cave_view = StoryView.from_story(story)
        cave_view.choose("Explore cave")

        # River+bridge path: root + river + bridge_end = 3 nodes
        story2 = make_branching_story()
        bridge_view = StoryView.from_story(story2)
        bridge_view.choose("Follow river")
        bridge_view.choose("Cross bridge")

        assert cave_view.nodes_visited() == 2
        assert bridge_view.nodes_visited() == 3


@pytest.mark.integration
class TestNarrativeEngineIntegration:
    """NarrativeEngine registers, retrieves, and starts sessions for stories."""

    def test_registered_story_is_retrievable(
        self, narrative_engine: NarrativeEngine, branching_story: Story
    ) -> None:
        retrieved = narrative_engine.get_story(branching_story.title)
        assert retrieved.title == branching_story.title

    def test_list_stories_returns_registered_title(
        self, narrative_engine: NarrativeEngine, branching_story: Story
    ) -> None:
        titles = narrative_engine.list_stories()
        assert branching_story.title in titles

    def test_start_session_returns_narrative_session(
        self, narrative_engine: NarrativeEngine, branching_story: Story
    ) -> None:
        session = narrative_engine.start_session(branching_story.title)
        assert isinstance(session, NarrativeSession)

    def test_multiple_sessions_are_independent(
        self, narrative_engine: NarrativeEngine, branching_story: Story
    ) -> None:
        session_a = narrative_engine.start_session(branching_story.title)
        session_b = narrative_engine.start_session(branching_story.title)

        view_a = StoryView(session_a)
        view_b = StoryView(session_b)

        view_a.choose("Explore cave")
        view_b.choose("Follow river")

        assert view_a.is_finished() is True
        assert view_b.is_finished() is False

    def test_unknown_story_raises_key_error(
        self, narrative_engine: NarrativeEngine
    ) -> None:
        with pytest.raises(KeyError):
            narrative_engine.get_story("Nonexistent Story")

    def test_engine_can_register_multiple_stories(
        self, narrative_engine: NarrativeEngine
    ) -> None:
        linear = NarrativeEngine.build_linear_story(
            title="Short Tale",
            genre=StoryGenre.MYSTERY,
            passages=["A mystery begins.", "It ends here."],
        )
        narrative_engine.register_story(linear)
        assert "Short Tale" in narrative_engine.list_stories()
        assert len(narrative_engine.list_stories()) == 2


@pytest.mark.integration
class TestStoryViewAndEngineEndToEnd:
    """End-to-end: build story via engine, navigate via StoryView."""

    def test_engine_builds_and_plays_linear_story(self) -> None:
        engine = NarrativeEngine()
        story = NarrativeEngine.build_linear_story(
            title="The River Journey",
            genre=StoryGenre.ADVENTURE,
            passages=[
                "You stand at the river's edge.",
                "You build a raft and set off downstream.",
                "You reach the sea. Your journey is complete.",
            ],
        )
        engine.register_story("The River Journey")

        # Re-fetch and play through
        view = StoryView.from_story(story)
        assert "river's edge" in view.render_current().lower()
        view.choose("Continue")
        assert "raft" in view.render_current().lower()
        view.choose("Continue")
        assert view.is_finished() is True

    def test_story_node_count_matches_passages(self) -> None:
        passages = ["Passage one.", "Passage two.", "Passage three."]
        story = NarrativeEngine.build_linear_story(
            title="Three Passages",
            genre=StoryGenre.FANTASY,
            passages=passages,
        )
        assert story.node_count == 3

    def test_educational_note_accessible_on_node(
        self, branching_story: Story
    ) -> None:
        cave_node = branching_story.get_node("cave")
        assert "cave paintings" in cave_node.educational_note.lower()

    def test_full_narrative_after_complete_linear_playthrough(self) -> None:
        passages = [
            "The adventure begins.",
            "The hero faces a challenge.",
            "Victory is achieved.",
        ]
        view = StoryView.build_linear(title="Hero's Journey", passages=passages)
        view.choose("Continue")
        view.choose("Continue")
        narrative = view.full_narrative()
        assert "adventure begins" in narrative.lower()
        assert "hero faces" in narrative.lower()
        assert "victory" in narrative.lower()
