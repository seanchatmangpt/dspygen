"""
Game engine for the TAGEE system.

Coordinates the interplay between the education module (quizzes, topics)
and the narrative engine (story progression), providing a unified runtime
that drives the full game loop.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Dict, List, Optional

from dspygen.experiments.tagee.src.core.education_module import (
    EducationSession,
    LearnerProfile,
    Question,
    SessionState,
    Topic,
)
from dspygen.experiments.tagee.src.core.narrative_engine import (
    NarrativeEngine,
    NarrativeSession,
    Story,
    StoryGenre,
)


class GamePhase(Enum):
    """Top-level lifecycle phases of a TAGEE game session."""

    LOBBY = "lobby"
    STORY = "story"
    EDUCATION = "education"
    RESULTS = "results"
    ENDED = "ended"


@dataclass
class GameConfig:
    """Immutable configuration supplied when a game is created."""

    story_title: str
    topics: List[Topic]
    questions: List[Question]
    pass_threshold: float = 70.0  # minimum % score to "win"
    allow_retry: bool = True


@dataclass
class GameResult:
    """Outcome produced when a game session ends."""

    learner_name: str
    score: int
    total_questions: int
    percentage: float
    passed: bool
    nodes_visited: int
    choices_made: List[str] = field(default_factory=list)


class GameEngine:
    """
    Central coordinator for a TAGEE game session.

    Sequences the learner through: lobby -> story -> education (quiz) -> results.

    The engine wires together a NarrativeSession and an EducationSession so
    that story choices can unlock quiz questions and quiz performance can
    influence narrative branches.
    """

    def __init__(
        self,
        config: GameConfig,
        narrative_engine: NarrativeEngine,
        learner: Optional[LearnerProfile] = None,
    ) -> None:
        self.config = config
        self.narrative_engine = narrative_engine
        self.learner = learner or LearnerProfile(
            learner_id="anonymous", name="Anonymous"
        )
        self._phase: GamePhase = GamePhase.LOBBY
        self._narrative_session: Optional[NarrativeSession] = None
        self._education_session: Optional[EducationSession] = None
        self._event_log: List[str] = []

    # ------------------------------------------------------------------
    # Phase accessors
    # ------------------------------------------------------------------

    @property
    def phase(self) -> GamePhase:
        return self._phase

    @property
    def narrative_session(self) -> Optional[NarrativeSession]:
        return self._narrative_session

    @property
    def education_session(self) -> Optional[EducationSession]:
        return self._education_session

    # ------------------------------------------------------------------
    # Game flow
    # ------------------------------------------------------------------

    def start(self) -> None:
        """Transition from LOBBY to STORY, starting the narrative."""
        if self._phase != GamePhase.LOBBY:
            raise RuntimeError(f"Cannot start from phase '{self._phase.value}'.")
        self._narrative_session = self.narrative_engine.start_session(
            self.config.story_title
        )
        self._phase = GamePhase.STORY
        self._log(f"Game started for '{self.learner.name}'.")

    def make_story_choice(self, choice_label: str) -> str:
        """
        Advance the story by *choice_label*.

        If the resulting node is an ending, the engine automatically
        transitions to the EDUCATION phase.

        Returns the text of the next story node.
        """
        if self._phase != GamePhase.STORY:
            raise RuntimeError("Not in the STORY phase.")
        assert self._narrative_session is not None
        next_node = self._narrative_session.choose(choice_label)
        self._log(f"Story choice '{choice_label}' -> node '{next_node.node_id}'.")
        if self._narrative_session.is_finished:
            self._enter_education()
        return next_node.text

    def _enter_education(self) -> None:
        """Internal: switch to the education (quiz) phase."""
        self._education_session = EducationSession(
            topics=self.config.topics,
            questions=self.config.questions,
            learner=self.learner,
        )
        self._education_session.start()
        self._phase = GamePhase.EDUCATION
        self._log("Entered EDUCATION phase.")

    def enter_education_directly(self) -> None:
        """Skip or finish the story and jump straight to education."""
        if self._phase not in (GamePhase.LOBBY, GamePhase.STORY):
            raise RuntimeError(f"Cannot enter education from phase '{self._phase.value}'.")
        if self._phase == GamePhase.LOBBY:
            self.start()
        self._enter_education()

    def submit_quiz_answer(self, question_index: int, answer: str) -> bool:
        """
        Submit an answer for the quiz. Returns True if correct.
        """
        if self._phase != GamePhase.EDUCATION:
            raise RuntimeError("Not in the EDUCATION phase.")
        assert self._education_session is not None
        if self._education_session.state != SessionState.TOPIC_EXPLORATION:
            # Auto-advance to quiz if still in topic exploration
            self._education_session.begin_quiz()
        correct = self._education_session.submit_answer(question_index, answer)
        self._log(
            f"Q{question_index} answered '{answer}': {'correct' if correct else 'wrong'}."
        )
        return correct

    def finish_quiz(self) -> GameResult:
        """
        Complete the quiz and return a GameResult.

        Transitions the engine to RESULTS and then ENDED.
        """
        if self._phase != GamePhase.EDUCATION:
            raise RuntimeError("Not in the EDUCATION phase.")
        assert self._education_session is not None
        edu = self._education_session
        if edu.state == SessionState.TOPIC_EXPLORATION:
            edu.begin_quiz()
        edu.complete()
        self._phase = GamePhase.RESULTS

        pct = edu.percentage_score()
        result = GameResult(
            learner_name=self.learner.name,
            score=edu.score,
            total_questions=len(edu.questions),
            percentage=pct,
            passed=pct >= self.config.pass_threshold,
            nodes_visited=(
                self._narrative_session.path_length()
                if self._narrative_session
                else 0
            ),
            choices_made=(
                list(self._narrative_session.choices_made)
                if self._narrative_session
                else []
            ),
        )
        self._phase = GamePhase.ENDED
        self._log(f"Game ended. Score={edu.score}, passed={result.passed}.")
        return result

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _log(self, message: str) -> None:
        self._event_log.append(message)

    def event_log(self) -> List[str]:
        return list(self._event_log)
