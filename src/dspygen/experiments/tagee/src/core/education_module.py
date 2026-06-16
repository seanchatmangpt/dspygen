"""
Education module for the TAGEE (Teaching and Adventure Game Educational Engine) system.

Provides core data structures and logic for managing topics, questions,
learner progress, and curriculum sessions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class Difficulty(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


@dataclass
class Topic:
    """A single educational topic with title and content."""

    name: str
    content: str
    difficulty: Difficulty = Difficulty.MEDIUM
    tags: List[str] = field(default_factory=list)

    def summary(self, max_chars: int = 100) -> str:
        """Return a truncated content summary."""
        if len(self.content) <= max_chars:
            return self.content
        return self.content[:max_chars].rstrip() + "..."


@dataclass
class Question:
    """A multiple-choice question linked to a topic."""

    text: str
    options: List[str]
    correct_answer: str
    topic_name: str = ""
    explanation: str = ""

    def is_correct(self, answer: str) -> bool:
        """Return True if the provided answer matches the correct answer."""
        return answer.strip().upper() == self.correct_answer.strip().upper()


@dataclass
class LearnerProfile:
    """Tracks a learner's identity and cumulative progress."""

    learner_id: str
    name: str
    total_score: int = 0
    sessions_completed: int = 0
    topics_mastered: List[str] = field(default_factory=list)

    def record_session_result(self, score: int, topic_names: List[str]) -> None:
        """Update cumulative stats after a session completes."""
        self.total_score += score
        self.sessions_completed += 1
        for topic in topic_names:
            if topic not in self.topics_mastered:
                self.topics_mastered.append(topic)

    @property
    def mastery_count(self) -> int:
        return len(self.topics_mastered)


class SessionState(Enum):
    INTRODUCTION = "introduction"
    TOPIC_EXPLORATION = "topic_exploration"
    QUIZ = "quiz"
    COMPLETED = "completed"


class EducationSession:
    """
    Manages a single tutoring session: topic exploration followed by a quiz.

    This is the central aggregate that coordinates curriculum progression
    and score tracking within one learner session.
    """

    def __init__(
        self,
        topics: List[Topic],
        questions: List[Question],
        learner: Optional[LearnerProfile] = None,
    ) -> None:
        if not topics:
            raise ValueError("A session must have at least one topic.")
        self.topics = topics
        self.questions = questions
        self.learner = learner
        self.current_topic_index: int = 0
        self.score: int = 0
        self.answers_given: List[str] = []
        self.state: SessionState = SessionState.INTRODUCTION

    # ------------------------------------------------------------------
    # State transitions
    # ------------------------------------------------------------------

    def start(self) -> None:
        """Move from introduction to topic exploration."""
        if self.state != SessionState.INTRODUCTION:
            raise RuntimeError(f"Cannot start from state '{self.state.value}'.")
        self.state = SessionState.TOPIC_EXPLORATION

    def advance_topic(self) -> bool:
        """Move to the next topic. Returns True if another topic is available."""
        if self.current_topic_index < len(self.topics) - 1:
            self.current_topic_index += 1
            return True
        return False

    def begin_quiz(self) -> None:
        """Transition to the quiz phase."""
        if self.state != SessionState.TOPIC_EXPLORATION:
            raise RuntimeError(f"Cannot begin quiz from state '{self.state.value}'.")
        self.state = SessionState.QUIZ

    def complete(self) -> None:
        """Mark the session as completed and update the learner profile."""
        if self.state != SessionState.QUIZ:
            raise RuntimeError(f"Cannot complete from state '{self.state.value}'.")
        self.state = SessionState.COMPLETED
        if self.learner is not None:
            self.learner.record_session_result(
                self.score, [t.name for t in self.topics]
            )

    # ------------------------------------------------------------------
    # Content access
    # ------------------------------------------------------------------

    def current_topic(self) -> Topic:
        return self.topics[self.current_topic_index]

    def has_more_topics(self) -> bool:
        return self.current_topic_index < len(self.topics) - 1

    # ------------------------------------------------------------------
    # Quiz logic
    # ------------------------------------------------------------------

    def submit_answer(self, question_index: int, answer: str) -> bool:
        """
        Submit an answer for the question at *question_index*.

        Returns True if correct and updates the running score.
        """
        if question_index >= len(self.questions):
            raise IndexError(f"No question at index {question_index}.")
        question = self.questions[question_index]
        correct = question.is_correct(answer)
        self.answers_given.append(answer)
        if correct:
            self.score += 1
        return correct

    def percentage_score(self) -> float:
        """Return the quiz score as a percentage (0-100)."""
        if not self.questions:
            return 0.0
        return (self.score / len(self.questions)) * 100
