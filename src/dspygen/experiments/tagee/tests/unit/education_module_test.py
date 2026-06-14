"""Unit tests for the TAGEE education module.

Tests cover: Difficulty, Topic, Question, LearnerProfile, SessionState,
and EducationSession — including validation, state transitions,
quiz scoring, and learner profile updates.
"""

from __future__ import annotations

import sys
import os

import pytest

# Allow direct import of the core modules without a package install.
# Insert the dspygen src root so that package-qualified imports resolve.
_tagee_root = os.path.join(os.path.dirname(__file__), "..", "..")
_repo_src = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", "..", "src")
sys.path.insert(0, os.path.abspath(_repo_src))
sys.path.insert(0, os.path.abspath(os.path.join(_tagee_root, "src", "core")))

from education_module import (
    Difficulty,
    EducationSession,
    LearnerProfile,
    Question,
    SessionState,
    Topic,
)


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------


def make_topic(name: str = "Photosynthesis", content: str = "Plants convert sunlight into food.") -> Topic:
    return Topic(name=name, content=content)


def make_question(
    text: str = "What gas do plants absorb?",
    correct: str = "CO2",
) -> Question:
    return Question(
        text=text,
        options=["O2", "N2", "CO2", "H2"],
        correct_answer=correct,
    )


def make_learner(lid: str = "l1", name: str = "Alice") -> LearnerProfile:
    return LearnerProfile(learner_id=lid, name=name)


@pytest.fixture()
def topics() -> list[Topic]:
    return [make_topic("Biology", "Study of living things."), make_topic("Chemistry", "Study of matter.")]


@pytest.fixture()
def questions() -> list[Question]:
    return [make_question("What is H2O?", "water"), make_question("What is NaCl?", "salt")]


@pytest.fixture()
def session(topics: list[Topic], questions: list[Question]) -> EducationSession:
    return EducationSession(topics=topics, questions=questions)


@pytest.fixture()
def started_session(session: EducationSession) -> EducationSession:
    session.start()
    return session


# ---------------------------------------------------------------------------
# Difficulty enum tests
# ---------------------------------------------------------------------------


class TestDifficulty:
    """Tests for the Difficulty enum."""

    def test_easy_value(self) -> None:
        assert Difficulty.EASY.value == "easy"

    def test_medium_value(self) -> None:
        assert Difficulty.MEDIUM.value == "medium"

    def test_hard_value(self) -> None:
        assert Difficulty.HARD.value == "hard"

    def test_all_difficulties_enumerable(self) -> None:
        values = {d.value for d in Difficulty}
        assert values == {"easy", "medium", "hard"}


# ---------------------------------------------------------------------------
# Topic tests
# ---------------------------------------------------------------------------


class TestTopic:
    """Tests for the Topic dataclass."""

    def test_valid_creation(self) -> None:
        t = make_topic()
        assert t.name == "Photosynthesis"
        assert t.difficulty == Difficulty.MEDIUM  # default

    def test_custom_difficulty(self) -> None:
        t = Topic(name="Calc", content="Derivatives.", difficulty=Difficulty.HARD)
        assert t.difficulty == Difficulty.HARD

    def test_default_tags_empty(self) -> None:
        t = make_topic()
        assert t.tags == []

    def test_tags_set(self) -> None:
        t = Topic(name="Calc", content="...", tags=["math", "advanced"])
        assert "math" in t.tags

    def test_summary_short_content(self) -> None:
        t = make_topic(content="Short text.")
        assert t.summary() == "Short text."

    def test_summary_truncates_at_max_chars(self) -> None:
        long_content = "A" * 200
        t = make_topic(content=long_content)
        result = t.summary(max_chars=50)
        assert len(result) <= 53  # 50 + "..."
        assert result.endswith("...")

    def test_summary_custom_max_chars(self) -> None:
        t = make_topic(content="Hello World, this is a longer piece of text.")
        result = t.summary(max_chars=10)
        assert result.endswith("...")

    def test_summary_exact_boundary(self) -> None:
        content = "A" * 100
        t = make_topic(content=content)
        # Exactly 100 chars should NOT be truncated
        assert not t.summary(max_chars=100).endswith("...")


# ---------------------------------------------------------------------------
# Question tests
# ---------------------------------------------------------------------------


class TestQuestion:
    """Tests for the Question dataclass."""

    def test_valid_creation(self) -> None:
        q = make_question()
        assert q.text == "What gas do plants absorb?"
        assert len(q.options) == 4

    def test_is_correct_case_insensitive(self) -> None:
        q = make_question(correct="CO2")
        assert q.is_correct("co2") is True
        assert q.is_correct("CO2") is True

    def test_is_correct_strips_whitespace(self) -> None:
        q = make_question(correct="water")
        assert q.is_correct("  water  ") is True

    def test_is_correct_wrong_answer(self) -> None:
        q = make_question(correct="CO2")
        assert q.is_correct("O2") is False

    def test_default_topic_name_empty(self) -> None:
        q = make_question()
        assert q.topic_name == ""

    def test_default_explanation_empty(self) -> None:
        q = make_question()
        assert q.explanation == ""

    def test_with_topic_and_explanation(self) -> None:
        q = Question(
            text="Q?",
            options=["A", "B"],
            correct_answer="A",
            topic_name="Biology",
            explanation="Because A.",
        )
        assert q.topic_name == "Biology"
        assert q.explanation == "Because A."


# ---------------------------------------------------------------------------
# LearnerProfile tests
# ---------------------------------------------------------------------------


class TestLearnerProfile:
    """Tests for the LearnerProfile dataclass."""

    def test_initial_state(self) -> None:
        lp = make_learner()
        assert lp.total_score == 0
        assert lp.sessions_completed == 0
        assert lp.topics_mastered == []
        assert lp.mastery_count == 0

    def test_record_session_result_increments_score(self) -> None:
        lp = make_learner()
        lp.record_session_result(10, ["Biology"])
        assert lp.total_score == 10

    def test_record_session_result_cumulates_score(self) -> None:
        lp = make_learner()
        lp.record_session_result(10, ["A"])
        lp.record_session_result(5, ["B"])
        assert lp.total_score == 15

    def test_record_session_result_increments_session_count(self) -> None:
        lp = make_learner()
        lp.record_session_result(10, ["X"])
        assert lp.sessions_completed == 1

    def test_record_session_result_adds_topics(self) -> None:
        lp = make_learner()
        lp.record_session_result(10, ["Biology", "Chemistry"])
        assert "Biology" in lp.topics_mastered
        assert "Chemistry" in lp.topics_mastered

    def test_duplicate_topics_not_added_twice(self) -> None:
        lp = make_learner()
        lp.record_session_result(10, ["Math"])
        lp.record_session_result(5, ["Math"])
        assert lp.topics_mastered.count("Math") == 1

    def test_mastery_count_property(self) -> None:
        lp = make_learner()
        lp.record_session_result(0, ["A", "B", "C"])
        assert lp.mastery_count == 3

    def test_zero_score_session(self) -> None:
        lp = make_learner()
        lp.record_session_result(0, ["EmptyTopic"])
        assert lp.total_score == 0
        assert lp.sessions_completed == 1


# ---------------------------------------------------------------------------
# SessionState enum tests
# ---------------------------------------------------------------------------


class TestSessionState:
    """Tests for SessionState enum values."""

    def test_introduction_value(self) -> None:
        assert SessionState.INTRODUCTION.value == "introduction"

    def test_topic_exploration_value(self) -> None:
        assert SessionState.TOPIC_EXPLORATION.value == "topic_exploration"

    def test_quiz_value(self) -> None:
        assert SessionState.QUIZ.value == "quiz"

    def test_completed_value(self) -> None:
        assert SessionState.COMPLETED.value == "completed"


# ---------------------------------------------------------------------------
# EducationSession construction tests
# ---------------------------------------------------------------------------


class TestEducationSessionConstruction:
    """Tests for EducationSession creation and invariants."""

    def test_empty_topics_raises(self, questions: list[Question]) -> None:
        with pytest.raises(ValueError, match="at least one topic"):
            EducationSession(topics=[], questions=questions)

    def test_initial_state_is_introduction(self, session: EducationSession) -> None:
        assert session.state == SessionState.INTRODUCTION

    def test_initial_score_is_zero(self, session: EducationSession) -> None:
        assert session.score == 0

    def test_initial_topic_index_is_zero(self, session: EducationSession) -> None:
        assert session.current_topic_index == 0

    def test_no_learner_by_default(self, topics: list[Topic], questions: list[Question]) -> None:
        s = EducationSession(topics=topics, questions=questions)
        assert s.learner is None

    def test_with_learner_set(self, topics: list[Topic], questions: list[Question]) -> None:
        lp = make_learner()
        s = EducationSession(topics=topics, questions=questions, learner=lp)
        assert s.learner is lp


# ---------------------------------------------------------------------------
# EducationSession lifecycle tests
# ---------------------------------------------------------------------------


class TestEducationSessionLifecycle:
    """Tests for state machine transitions: start -> topic -> quiz -> complete."""

    def test_start_transitions_to_topic_exploration(self, session: EducationSession) -> None:
        session.start()
        assert session.state == SessionState.TOPIC_EXPLORATION

    def test_start_twice_raises(self, started_session: EducationSession) -> None:
        with pytest.raises(RuntimeError):
            started_session.start()

    def test_begin_quiz_from_topic_exploration(self, started_session: EducationSession) -> None:
        started_session.begin_quiz()
        assert started_session.state == SessionState.QUIZ

    def test_begin_quiz_from_wrong_state_raises(self, session: EducationSession) -> None:
        with pytest.raises(RuntimeError):
            session.begin_quiz()  # must be in TOPIC_EXPLORATION

    def test_complete_from_quiz_state(self, started_session: EducationSession) -> None:
        started_session.begin_quiz()
        started_session.complete()
        assert started_session.state == SessionState.COMPLETED

    def test_complete_from_wrong_state_raises(self, started_session: EducationSession) -> None:
        # In TOPIC_EXPLORATION, not QUIZ
        with pytest.raises(RuntimeError):
            started_session.complete()

    def test_complete_updates_learner_profile(
        self, topics: list[Topic], questions: list[Question]
    ) -> None:
        lp = make_learner()
        s = EducationSession(topics=topics, questions=questions, learner=lp)
        s.start()
        s.begin_quiz()
        s.complete()
        assert lp.sessions_completed == 1


# ---------------------------------------------------------------------------
# EducationSession topic navigation tests
# ---------------------------------------------------------------------------


class TestEducationSessionTopicNavigation:
    """Tests for topic traversal within a session."""

    def test_current_topic_initial(self, started_session: EducationSession) -> None:
        topic = started_session.current_topic()
        assert topic.name == "Biology"

    def test_advance_topic_returns_true(self, started_session: EducationSession) -> None:
        assert started_session.advance_topic() is True

    def test_advance_topic_changes_current_topic(self, started_session: EducationSession) -> None:
        started_session.advance_topic()
        assert started_session.current_topic().name == "Chemistry"

    def test_advance_topic_at_last_returns_false(self, started_session: EducationSession) -> None:
        started_session.advance_topic()  # move to last topic
        assert started_session.advance_topic() is False  # already at end

    def test_has_more_topics_true(self, started_session: EducationSession) -> None:
        assert started_session.has_more_topics() is True

    def test_has_more_topics_false_at_end(self, started_session: EducationSession) -> None:
        started_session.advance_topic()
        assert started_session.has_more_topics() is False


# ---------------------------------------------------------------------------
# EducationSession quiz tests
# ---------------------------------------------------------------------------


class TestEducationSessionQuiz:
    """Tests for quiz answer submission and scoring."""

    def test_correct_answer_returns_true(self, started_session: EducationSession) -> None:
        started_session.begin_quiz()
        assert started_session.submit_answer(0, "water") is True

    def test_wrong_answer_returns_false(self, started_session: EducationSession) -> None:
        started_session.begin_quiz()
        assert started_session.submit_answer(0, "milk") is False

    def test_correct_answer_increments_score(self, started_session: EducationSession) -> None:
        started_session.begin_quiz()
        started_session.submit_answer(0, "water")
        assert started_session.score == 1

    def test_wrong_answer_does_not_increment_score(self, started_session: EducationSession) -> None:
        started_session.begin_quiz()
        started_session.submit_answer(0, "wrong")
        assert started_session.score == 0

    def test_multiple_correct_answers_accumulate(self, started_session: EducationSession) -> None:
        started_session.begin_quiz()
        started_session.submit_answer(0, "water")
        started_session.submit_answer(1, "salt")
        assert started_session.score == 2

    def test_answers_given_recorded(self, started_session: EducationSession) -> None:
        started_session.begin_quiz()
        started_session.submit_answer(0, "water")
        assert "water" in started_session.answers_given

    def test_out_of_range_index_raises(self, started_session: EducationSession) -> None:
        started_session.begin_quiz()
        with pytest.raises(IndexError):
            started_session.submit_answer(999, "anything")

    def test_percentage_score_all_correct(self, started_session: EducationSession) -> None:
        started_session.begin_quiz()
        started_session.submit_answer(0, "water")
        started_session.submit_answer(1, "salt")
        assert started_session.percentage_score() == 100.0

    def test_percentage_score_none_correct(self, started_session: EducationSession) -> None:
        started_session.begin_quiz()
        started_session.submit_answer(0, "wrong1")
        started_session.submit_answer(1, "wrong2")
        assert started_session.percentage_score() == 0.0

    def test_percentage_score_partial(self, started_session: EducationSession) -> None:
        started_session.begin_quiz()
        started_session.submit_answer(0, "water")  # correct
        started_session.submit_answer(1, "wrong")  # wrong
        assert started_session.percentage_score() == 50.0

    def test_percentage_score_no_questions(self, topics: list[Topic]) -> None:
        s = EducationSession(topics=topics, questions=[])
        s.start()
        s.begin_quiz()
        assert s.percentage_score() == 0.0

    def test_complete_updates_learner_total_score(
        self, topics: list[Topic], questions: list[Question]
    ) -> None:
        lp = make_learner()
        s = EducationSession(topics=topics, questions=questions, learner=lp)
        s.start()
        s.begin_quiz()
        s.submit_answer(0, "water")  # correct
        s.complete()
        assert lp.total_score == 1
