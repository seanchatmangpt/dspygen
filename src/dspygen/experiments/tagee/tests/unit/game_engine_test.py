"""Unit tests for the TAGEE game engine.

Tests cover: GamePhase, GameConfig, GameResult, and GameEngine —
including lifecycle phase transitions, story choice delegation,
quiz answering, scoring, pass/fail results, and event logging.
"""

from __future__ import annotations

import sys
import os

import pytest

_tagee_root = os.path.join(os.path.dirname(__file__), "..", "..")
_repo_src = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", "..", "src")
sys.path.insert(0, os.path.abspath(_repo_src))
sys.path.insert(0, os.path.abspath(os.path.join(_tagee_root, "src", "core")))

from education_module import (
    Difficulty,
    LearnerProfile,
    Question,
    Topic,
)
from narrative_engine import (
    NarrativeEngine,
    Story,
    StoryGenre,
    StoryNode,
)
from game_engine import (
    GameConfig,
    GameEngine,
    GamePhase,
    GameResult,
)


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------


def make_linear_story(title: str = "Test Quest") -> Story:
    """Build a two-node linear story: start -> ending."""
    engine = NarrativeEngine()
    story = NarrativeEngine.build_linear_story(
        title=title,
        genre=StoryGenre.ADVENTURE,
        passages=["The journey begins.", "You have arrived!"],
    )
    return story


def make_engine_with_story(
    story_title: str = "Test Quest",
    topics: list[Topic] | None = None,
    questions: list[Question] | None = None,
    learner: LearnerProfile | None = None,
) -> GameEngine:
    """Return a configured GameEngine ready to start."""
    if topics is None:
        topics = [Topic(name="Math", content="Numbers and operations.")]
    if questions is None:
        questions = [
            Question(text="1+1=?", options=["1", "2", "3"], correct_answer="2"),
        ]
    story = make_linear_story(story_title)
    narrative_engine = NarrativeEngine()
    narrative_engine.register_story(story)

    config = GameConfig(
        story_title=story_title,
        topics=topics,
        questions=questions,
    )
    return GameEngine(config=config, narrative_engine=narrative_engine, learner=learner)


@pytest.fixture()
def engine() -> GameEngine:
    return make_engine_with_story()


@pytest.fixture()
def started_engine(engine: GameEngine) -> GameEngine:
    engine.start()
    return engine


@pytest.fixture()
def in_education_engine(started_engine: GameEngine) -> GameEngine:
    """Engine that has advanced through the story and is in EDUCATION phase."""
    started_engine.make_story_choice("Continue")  # advance to ending node -> auto enters education
    return started_engine


# ---------------------------------------------------------------------------
# GamePhase enum tests
# ---------------------------------------------------------------------------


class TestGamePhase:
    """Tests for the GamePhase enum."""

    def test_all_phases_present(self) -> None:
        phases = {p.value for p in GamePhase}
        assert phases == {"lobby", "story", "education", "results", "ended"}

    def test_lobby_value(self) -> None:
        assert GamePhase.LOBBY.value == "lobby"

    def test_ended_value(self) -> None:
        assert GamePhase.ENDED.value == "ended"


# ---------------------------------------------------------------------------
# GameConfig tests
# ---------------------------------------------------------------------------


class TestGameConfig:
    """Tests for the GameConfig dataclass."""

    def test_defaults(self) -> None:
        cfg = GameConfig(
            story_title="Quest",
            topics=[Topic("A", "content")],
            questions=[],
        )
        assert cfg.pass_threshold == 70.0
        assert cfg.allow_retry is True

    def test_custom_pass_threshold(self) -> None:
        cfg = GameConfig(
            story_title="Quest",
            topics=[Topic("A", "content")],
            questions=[],
            pass_threshold=90.0,
        )
        assert cfg.pass_threshold == 90.0


# ---------------------------------------------------------------------------
# GameResult tests
# ---------------------------------------------------------------------------


class TestGameResult:
    """Tests for the GameResult dataclass."""

    def test_valid_creation(self) -> None:
        result = GameResult(
            learner_name="Bob",
            score=8,
            total_questions=10,
            percentage=80.0,
            passed=True,
            nodes_visited=5,
        )
        assert result.passed is True
        assert result.percentage == 80.0
        assert result.choices_made == []

    def test_failed_result(self) -> None:
        result = GameResult(
            learner_name="Eve",
            score=3,
            total_questions=10,
            percentage=30.0,
            passed=False,
            nodes_visited=2,
        )
        assert result.passed is False


# ---------------------------------------------------------------------------
# GameEngine initial state tests
# ---------------------------------------------------------------------------


class TestGameEngineInitialState:
    """Tests for GameEngine state before start()."""

    def test_initial_phase_is_lobby(self, engine: GameEngine) -> None:
        assert engine.phase == GamePhase.LOBBY

    def test_no_narrative_session_before_start(self, engine: GameEngine) -> None:
        assert engine.narrative_session is None

    def test_no_education_session_before_start(self, engine: GameEngine) -> None:
        assert engine.education_session is None

    def test_event_log_empty_before_start(self, engine: GameEngine) -> None:
        assert engine.event_log() == []

    def test_anonymous_learner_by_default(self) -> None:
        eng = make_engine_with_story(learner=None)
        assert eng.learner.name == "Anonymous"

    def test_custom_learner_stored(self) -> None:
        lp = LearnerProfile(learner_id="u1", name="Dana")
        eng = make_engine_with_story(learner=lp)
        assert eng.learner.name == "Dana"


# ---------------------------------------------------------------------------
# GameEngine start tests
# ---------------------------------------------------------------------------


class TestGameEngineStart:
    """Tests for start() method."""

    def test_start_transitions_to_story(self, engine: GameEngine) -> None:
        engine.start()
        assert engine.phase == GamePhase.STORY

    def test_start_creates_narrative_session(self, engine: GameEngine) -> None:
        engine.start()
        assert engine.narrative_session is not None

    def test_start_twice_raises(self, started_engine: GameEngine) -> None:
        with pytest.raises(RuntimeError, match="Cannot start"):
            started_engine.start()

    def test_start_logs_event(self, engine: GameEngine) -> None:
        engine.start()
        log = engine.event_log()
        assert len(log) >= 1


# ---------------------------------------------------------------------------
# GameEngine story phase tests
# ---------------------------------------------------------------------------


class TestGameEngineStoryPhase:
    """Tests for make_story_choice while in the STORY phase."""

    def test_make_story_choice_returns_text(self, started_engine: GameEngine) -> None:
        text = started_engine.make_story_choice("Continue")
        assert isinstance(text, str)
        assert len(text) > 0

    def test_make_story_choice_not_in_story_raises(self, engine: GameEngine) -> None:
        # Still in LOBBY
        with pytest.raises(RuntimeError, match="STORY"):
            engine.make_story_choice("Continue")

    def test_reaching_ending_node_enters_education(self, started_engine: GameEngine) -> None:
        # The linear story has exactly one choice from root -> ending node
        started_engine.make_story_choice("Continue")
        assert started_engine.phase == GamePhase.EDUCATION

    def test_invalid_choice_raises(self, started_engine: GameEngine) -> None:
        with pytest.raises(ValueError):
            started_engine.make_story_choice("Fly away")

    def test_education_session_created_after_story_ends(self, in_education_engine: GameEngine) -> None:
        assert in_education_engine.education_session is not None


# ---------------------------------------------------------------------------
# GameEngine enter_education_directly tests
# ---------------------------------------------------------------------------


class TestGameEngineEnterEducationDirectly:
    """Tests for enter_education_directly() shortcut."""

    def test_from_lobby_transitions_to_education(self, engine: GameEngine) -> None:
        engine.enter_education_directly()
        assert engine.phase == GamePhase.EDUCATION

    def test_from_story_transitions_to_education(self, started_engine: GameEngine) -> None:
        started_engine.enter_education_directly()
        assert started_engine.phase == GamePhase.EDUCATION

    def test_from_education_raises(self, in_education_engine: GameEngine) -> None:
        with pytest.raises(RuntimeError):
            in_education_engine.enter_education_directly()


# ---------------------------------------------------------------------------
# GameEngine quiz tests
# ---------------------------------------------------------------------------


class TestGameEngineQuiz:
    """Tests for submit_quiz_answer() and finish_quiz()."""

    def test_correct_answer_returns_true(self, in_education_engine: GameEngine) -> None:
        assert in_education_engine.submit_quiz_answer(0, "2") is True

    def test_wrong_answer_returns_false(self, in_education_engine: GameEngine) -> None:
        assert in_education_engine.submit_quiz_answer(0, "99") is False

    def test_submit_outside_education_raises(self, started_engine: GameEngine) -> None:
        with pytest.raises(RuntimeError, match="EDUCATION"):
            started_engine.submit_quiz_answer(0, "2")

    def test_finish_quiz_returns_game_result(self, in_education_engine: GameEngine) -> None:
        result = in_education_engine.finish_quiz()
        assert isinstance(result, GameResult)

    def test_finish_quiz_correct_answer_passes(self, in_education_engine: GameEngine) -> None:
        in_education_engine.submit_quiz_answer(0, "2")  # correct
        result = in_education_engine.finish_quiz()
        assert result.passed is True

    def test_finish_quiz_wrong_answer_fails(self, in_education_engine: GameEngine) -> None:
        in_education_engine.submit_quiz_answer(0, "99")  # wrong
        result = in_education_engine.finish_quiz()
        assert result.passed is False

    def test_finish_quiz_transitions_to_ended(self, in_education_engine: GameEngine) -> None:
        in_education_engine.finish_quiz()
        assert in_education_engine.phase == GamePhase.ENDED

    def test_finish_quiz_score_reflects_correct_answers(self, in_education_engine: GameEngine) -> None:
        in_education_engine.submit_quiz_answer(0, "2")
        result = in_education_engine.finish_quiz()
        assert result.score == 1

    def test_finish_quiz_percentage_correct(self, in_education_engine: GameEngine) -> None:
        in_education_engine.submit_quiz_answer(0, "2")
        result = in_education_engine.finish_quiz()
        assert result.percentage == 100.0

    def test_finish_quiz_outside_education_raises(self, started_engine: GameEngine) -> None:
        with pytest.raises(RuntimeError, match="EDUCATION"):
            started_engine.finish_quiz()

    def test_finish_quiz_records_nodes_visited(self, in_education_engine: GameEngine) -> None:
        result = in_education_engine.finish_quiz()
        assert result.nodes_visited >= 1

    def test_finish_quiz_records_choices_made(self, engine: GameEngine) -> None:
        engine.start()
        engine.make_story_choice("Continue")
        result = engine.finish_quiz()
        assert "Continue" in result.choices_made

    def test_pass_threshold_honoured(self) -> None:
        """A 100% pass threshold should only pass with a perfect score."""
        topics = [Topic("Math", "content")]
        questions = [
            Question("A?", ["1", "2"], "1"),
            Question("B?", ["1", "2"], "1"),
        ]
        story = NarrativeEngine.build_linear_story("Q", StoryGenre.MYSTERY, ["Go!"])
        ne = NarrativeEngine()
        ne.register_story(story)
        cfg = GameConfig(story_title="Q", topics=topics, questions=questions, pass_threshold=100.0)
        eng = GameEngine(config=cfg, narrative_engine=ne)
        eng.enter_education_directly()
        eng.submit_quiz_answer(0, "1")  # correct
        eng.submit_quiz_answer(1, "2")  # wrong
        result = eng.finish_quiz()
        assert result.passed is False


# ---------------------------------------------------------------------------
# GameEngine event log tests
# ---------------------------------------------------------------------------


class TestGameEngineEventLog:
    """Tests for the event log produced by the engine."""

    def test_event_log_grows_during_session(self, engine: GameEngine) -> None:
        engine.start()
        engine.make_story_choice("Continue")
        engine.finish_quiz()
        assert len(engine.event_log()) > 1

    def test_event_log_returns_copy(self, started_engine: GameEngine) -> None:
        log1 = started_engine.event_log()
        log2 = started_engine.event_log()
        assert log1 is not log2
