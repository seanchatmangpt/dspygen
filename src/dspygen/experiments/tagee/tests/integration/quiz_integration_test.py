"""
Integration tests for the TAGEE quiz feature.

Tests verify that QuizView, EducationSession, Topic, Question, and
LearnerProfile all work together across end-to-end quiz workflows.
"""

from __future__ import annotations

import pytest

from dspygen.experiments.tagee.src.core.education_module import (
    Difficulty,
    EducationSession,
    LearnerProfile,
    Question,
    SessionState,
    Topic,
)
from dspygen.experiments.tagee.src.ui.modules.quiz_view import QuizView
from dspygen.experiments.tagee.src.ui.utils.ui_helpers import compute_letter_grade


# ---------------------------------------------------------------------------
# Shared test data builders
# ---------------------------------------------------------------------------


def make_topics() -> list[Topic]:
    return [
        Topic(
            name="The Water Cycle",
            content=(
                "Water moves continuously through the environment in a cycle: "
                "evaporation, condensation, precipitation, and collection."
            ),
            difficulty=Difficulty.EASY,
            tags=["science", "geography"],
        ),
        Topic(
            name="Photosynthesis",
            content=(
                "Photosynthesis is the process by which green plants convert "
                "sunlight, water, and CO2 into glucose and oxygen."
            ),
            difficulty=Difficulty.MEDIUM,
            tags=["biology"],
        ),
    ]


def make_questions() -> list[Question]:
    return [
        Question(
            text="What drives evaporation in the water cycle?",
            options=["A. Gravity", "B. Solar energy", "C. Wind", "D. Pressure"],
            correct_answer="B",
            topic_name="The Water Cycle",
            explanation="Solar energy heats surface water, causing it to evaporate.",
        ),
        Question(
            text="Which gas do plants absorb during photosynthesis?",
            options=["A. Oxygen", "B. Nitrogen", "C. Carbon dioxide", "D. Hydrogen"],
            correct_answer="C",
            topic_name="Photosynthesis",
            explanation="Plants absorb CO2 and release O2 as a byproduct.",
        ),
        Question(
            text="What is the primary product of photosynthesis?",
            options=["A. Starch", "B. Glucose", "C. Cellulose", "D. Fructose"],
            correct_answer="B",
            topic_name="Photosynthesis",
            explanation="Glucose is the main sugar produced during photosynthesis.",
        ),
    ]


@pytest.fixture()
def learner() -> LearnerProfile:
    return LearnerProfile(learner_id="student_001", name="Alex")


@pytest.fixture()
def quiz_view(learner: LearnerProfile) -> QuizView:
    return QuizView(topics=make_topics(), questions=make_questions(), learner=learner)


# ---------------------------------------------------------------------------
# Integration tests
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestQuizViewStartupAndTopicDisplay:
    """QuizView starts correctly and displays topic content."""

    def test_start_returns_first_topic_header(self, quiz_view: QuizView) -> None:
        display = quiz_view.start()
        assert "The Water Cycle" in display
        assert "Topic 1/2" in display

    def test_start_includes_topic_content(self, quiz_view: QuizView) -> None:
        display = quiz_view.start()
        assert "evaporation" in display.lower() or "water" in display.lower()

    def test_advance_to_second_topic(self, quiz_view: QuizView) -> None:
        quiz_view.start()
        display = quiz_view.next_topic()
        assert "Photosynthesis" in display
        assert "Topic 2/2" in display

    def test_advance_past_last_topic_signals_quiz_ready(
        self, quiz_view: QuizView
    ) -> None:
        quiz_view.start()
        quiz_view.next_topic()  # move to topic 2
        message = quiz_view.next_topic()  # no more topics
        assert "quiz" in message.lower() or "ready" in message.lower()

    def test_session_state_is_topic_exploration_after_start(
        self, quiz_view: QuizView
    ) -> None:
        quiz_view.start()
        assert quiz_view.session.state == SessionState.TOPIC_EXPLORATION


@pytest.mark.integration
class TestQuizAnswerWorkflow:
    """Full quiz workflow: start -> topics -> quiz -> answers -> finish."""

    def _run_to_quiz(self, quiz_view: QuizView) -> None:
        """Helper: advance to the quiz phase."""
        quiz_view.start()
        quiz_view.next_topic()  # advance to topic 2
        quiz_view.begin_quiz()

    def test_begin_quiz_returns_first_question(self, quiz_view: QuizView) -> None:
        quiz_view.start()
        question_display = quiz_view.begin_quiz()
        assert "Q1:" in question_display
        assert "evaporation" in question_display.lower() or "water" in question_display.lower()

    def test_correct_answer_returns_true_and_positive_feedback(
        self, quiz_view: QuizView
    ) -> None:
        self._run_to_quiz(quiz_view)
        correct, feedback = quiz_view.submit_answer("B")  # correct answer to Q1
        assert correct is True
        assert "correct" in feedback.lower()

    def test_wrong_answer_returns_false(self, quiz_view: QuizView) -> None:
        self._run_to_quiz(quiz_view)
        correct, _ = quiz_view.submit_answer("A")  # wrong answer
        assert correct is False

    def test_wrong_answer_feedback_says_incorrect(self, quiz_view: QuizView) -> None:
        self._run_to_quiz(quiz_view)
        _, feedback = quiz_view.submit_answer("A")
        assert "incorrect" in feedback.lower()

    def test_explanation_is_included_in_feedback(self, quiz_view: QuizView) -> None:
        self._run_to_quiz(quiz_view)
        _, feedback = quiz_view.submit_answer("B")  # correct
        # Q1 has an explanation about solar energy
        assert "solar" in feedback.lower() or "correct" in feedback.lower()

    def test_has_more_questions_reflects_progress(
        self, quiz_view: QuizView
    ) -> None:
        self._run_to_quiz(quiz_view)
        assert quiz_view.has_more_questions() is True
        quiz_view.submit_answer("B")  # Q1
        assert quiz_view.has_more_questions() is True
        quiz_view.submit_answer("C")  # Q2
        assert quiz_view.has_more_questions() is True
        quiz_view.submit_answer("B")  # Q3
        assert quiz_view.has_more_questions() is False

    def test_perfect_score_after_all_correct_answers(
        self, quiz_view: QuizView
    ) -> None:
        self._run_to_quiz(quiz_view)
        quiz_view.submit_answer("B")  # Q1 correct
        quiz_view.submit_answer("C")  # Q2 correct
        quiz_view.submit_answer("B")  # Q3 correct
        assert quiz_view.session.score == 3

    def test_zero_score_after_all_wrong_answers(
        self, quiz_view: QuizView
    ) -> None:
        self._run_to_quiz(quiz_view)
        quiz_view.submit_answer("A")  # wrong
        quiz_view.submit_answer("A")  # wrong
        quiz_view.submit_answer("A")  # wrong
        assert quiz_view.session.score == 0


@pytest.mark.integration
class TestQuizCompletionAndLearnerUpdate:
    """Finishing a quiz updates the learner profile."""

    def _run_full_quiz(
        self, quiz_view: QuizView, answers: list[str]
    ) -> str:
        quiz_view.start()
        quiz_view.next_topic()
        quiz_view.begin_quiz()
        for answer in answers:
            quiz_view.submit_answer(answer)
        return quiz_view.finish()

    def test_finish_returns_results_string_with_learner_name(
        self, quiz_view: QuizView, learner: LearnerProfile
    ) -> None:
        summary = self._run_full_quiz(quiz_view, ["B", "C", "B"])
        assert learner.name in summary

    def test_finish_results_include_score(
        self, quiz_view: QuizView
    ) -> None:
        summary = self._run_full_quiz(quiz_view, ["B", "C", "B"])
        assert "3/3" in summary or "Score" in summary

    def test_session_state_is_completed_after_finish(
        self, quiz_view: QuizView
    ) -> None:
        self._run_full_quiz(quiz_view, ["B", "C", "B"])
        assert quiz_view.session.state == SessionState.COMPLETED

    def test_learner_profile_total_score_updated(
        self, quiz_view: QuizView, learner: LearnerProfile
    ) -> None:
        self._run_full_quiz(quiz_view, ["B", "C", "B"])
        # All 3 correct
        assert learner.total_score == 3

    def test_learner_sessions_completed_incremented(
        self, quiz_view: QuizView, learner: LearnerProfile
    ) -> None:
        self._run_full_quiz(quiz_view, ["B", "C", "B"])
        assert learner.sessions_completed == 1

    def test_learner_topics_mastered_populated(
        self, quiz_view: QuizView, learner: LearnerProfile
    ) -> None:
        self._run_full_quiz(quiz_view, ["B", "C", "B"])
        mastered = learner.topics_mastered
        assert "The Water Cycle" in mastered
        assert "Photosynthesis" in mastered

    def test_multiple_sessions_accumulate_scores(self, learner: LearnerProfile) -> None:
        for _ in range(2):
            view = QuizView(
                topics=make_topics(), questions=make_questions(), learner=learner
            )
            view.start()
            view.next_topic()
            view.begin_quiz()
            view.submit_answer("B")
            view.submit_answer("C")
            view.submit_answer("B")
            view.finish()
        assert learner.sessions_completed == 2
        assert learner.total_score == 6


@pytest.mark.integration
class TestQuizScoreDisplay:
    """The score display string integrates correctly with quiz state."""

    def test_score_display_after_some_correct_answers(
        self, quiz_view: QuizView
    ) -> None:
        quiz_view.start()
        quiz_view.next_topic()
        quiz_view.begin_quiz()
        quiz_view.submit_answer("B")  # correct
        quiz_view.submit_answer("A")  # wrong
        display = quiz_view.score_display()
        assert "1/3" in display

    def test_percentage_is_correct_for_mixed_results(
        self, quiz_view: QuizView
    ) -> None:
        quiz_view.start()
        quiz_view.next_topic()
        quiz_view.begin_quiz()
        quiz_view.submit_answer("B")  # correct Q1
        quiz_view.submit_answer("C")  # correct Q2
        quiz_view.submit_answer("A")  # wrong Q3
        pct = quiz_view.session.percentage_score()
        assert abs(pct - 66.67) < 0.1


@pytest.mark.integration
class TestQuizEdgeCases:
    """Edge cases and guard conditions for the quiz workflow."""

    def test_single_topic_single_question_full_workflow(self) -> None:
        topic = Topic(name="Colors", content="Colors are perceptions of light wavelengths.")
        question = Question(
            text="What color is the sky?",
            options=["A. Red", "B. Blue", "C. Green", "D. Yellow"],
            correct_answer="B",
        )
        view = QuizView(topics=[topic], questions=[question])
        view.start()
        view.begin_quiz()
        correct, _ = view.submit_answer("B")
        assert correct is True
        summary = view.finish()
        assert "1/1" in summary or "Score" in summary

    def test_grade_a_on_perfect_score(self, quiz_view: QuizView) -> None:
        quiz_view.start()
        quiz_view.next_topic()
        quiz_view.begin_quiz()
        quiz_view.submit_answer("B")
        quiz_view.submit_answer("C")
        quiz_view.submit_answer("B")
        pct = quiz_view.session.percentage_score()
        assert compute_letter_grade(pct) == "A"

    def test_grade_f_on_zero_score(self, quiz_view: QuizView) -> None:
        quiz_view.start()
        quiz_view.next_topic()
        quiz_view.begin_quiz()
        quiz_view.submit_answer("A")
        quiz_view.submit_answer("A")
        quiz_view.submit_answer("A")
        pct = quiz_view.session.percentage_score()
        assert compute_letter_grade(pct) == "F"
