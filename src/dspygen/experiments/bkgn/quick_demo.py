```python
# conversations.py
from abc import ABC, abstractmethod


class QuestionHandler(ABC):
    @abstractmethod
    def parse_question(self, question: str) -> dict:
        pass


class SocraticQuestionHandler(QuestionHandler):
    def parse_question(self, question: str) -> dict:


# Implement Socratic question parsing here

class ProjectBasedLearningHandler(QuestionHandler):
    def parse_question(self, question: str) -> dict:


# Implement project-based learning question parsing here

class ResponseGenerator(ABC):
    @abstractmethod
    def generate_response(self, interpreted_data: dict, user_data: dict) -> str:
        pass


class ContextualResponseGenerator(ResponseGenerator):
    def generate_response(self, interpreted_data: dict, user_data: dict) -> str:


# Implement contextual response generation here

class LearningSession:
    def __init__(self, question_handler: QuestionHandler, response_generator: ResponseGenerator):
        self.question_handler = question_handler
        self.response_generator = response_generator

    def start(self, question: str):
        interpreted_data = self.question_handler.parse_question(question)
        response = self.response_generator.generate_response(interpreted_data, user_data)
        # Add interactivity by returning or presenting the response


# app.py
import conversations
import project_dependencies


def start_conversation() -> None:
    question_handler = project_dependencies.create_question_handler()
    response_generator = project_dependencies.create_response_generator()

    learning_session = conversations.LearningSession(question_handler, response_generator)
    while True:
        user_question = input("Ask a question: ")
        learning_session.start(user_question)


if __name__ == "__main__":
    start_conversation()