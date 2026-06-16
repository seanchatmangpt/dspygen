"""
Quiz view module for the TAGEE system.

Wraps an EducationSession and exposes a clean controller API that the
UI layer (CLI, web, test harness) can drive without knowing the
internals of the education module.
"""

from __future__ import annotations

from typing import List, Optional, Tuple

from dspygen.experiments.tagee.src.core.education_module import (
    EducationSession,
    LearnerProfile,
    Question,
    SessionState,
    Topic,
)
from dspygen.experiments.tagee.src.ui.utils.formatting_tools import (
    format_question,
    format_score,
    format_topic_header,
)
from dspygen.experiments.tagee.src.ui.utils.ui_helpers import (
    render_quiz_feedback,
    summarise_results,
)


class QuizView:
    """
    Controller for the quiz UI module.

    Drives an EducationSession through its full lifecycle:
    introduction -> topic exploration -> quiz -> completed.

    All methods return strings so callers can render them however they
    like (terminal print, web response, test assertion).
    """

    def __init__(
        self,
        topics: List[Topic],
        questions: List[Question],
        learner: Optional[LearnerProfile] = None,
    ) -> None:
        self.session = EducationSession(
            topics=topics,
            questions=questions,
            learner=learner,
        )
        self._current_question_index: int = 0
        self._feedback_history: List[Tuple[int, bool, str]] = []

    # ------------------------------------------------------------------
    # Session lifecycle
    # ------------------------------------------------------------------

    def start(self) -> str:
        """Start the session and return the first topic header + content."""
        self.session.start()
        return self._render_current_topic()

    def next_topic(self) -> str:
        """
        Advance to the next topic if available.

        Returns the topic content, or a message indicating the quiz
        should begin.
        """
        if self.session.state != SessionState.TOPIC_EXPLORATION:
            return "Session is not in topic exploration mode."
        advanced = self.session.advance_topic()
        if advanced:
            return self._render_current_topic()
        return "All topics covered. Ready for the quiz!"

    def begin_quiz(self) -> str:
        """Transition to the quiz phase and return the first question."""
        self.session.begin_quiz()
        return self._render_question(self._current_question_index)

    def submit_answer(self, answer: str) -> Tuple[bool, str]:
        """
        Submit an answer for the current question.

        Returns (is_correct, feedback_string).
        Automatically advances the question pointer.
        """
        idx = self._current_question_index
        correct = self.session.submit_answer(idx, answer)
        explanation = self.session.questions[idx].explanation
        feedback = render_quiz_feedback(correct, explanation)
        self._feedback_history.append((idx, correct, feedback))
        self._current_question_index += 1
        return correct, feedback

    def has_more_questions(self) -> bool:
        return self._current_question_index < len(self.session.questions)

    def current_question_display(self) -> str:
        """Return the formatted string for the current question."""
        return self._render_question(self._current_question_index)

    def finish(self) -> str:
        """Complete the session and return a results summary."""
        self.session.complete()
        learner_name = (
            self.session.learner.name if self.session.learner else "Learner"
        )
        return summarise_results(
            self.session.score,
            len(self.session.questions),
            learner_name,
        )

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _render_current_topic(self) -> str:
        topic = self.session.current_topic()
        idx = self.session.current_topic_index + 1
        total = len(self.session.topics)
        header = format_topic_header(topic.name, idx, total)
        return f"{header}\n\n{topic.content}"

    def _render_question(self, index: int) -> str:
        if index >= len(self.session.questions):
            return "No more questions."
        q = self.session.questions[index]
        return format_question(q.text, q.options, index + 1)

    def score_display(self) -> str:
        return format_score(self.session.score, len(self.session.questions))
