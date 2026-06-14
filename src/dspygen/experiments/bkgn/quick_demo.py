# conversations.py
from abc import ABC, abstractmethod


class QuestionHandler(ABC):
    @abstractmethod
    def parse_question(self, question: str) -> dict:
        pass


class SocraticQuestionHandler(QuestionHandler):
    def parse_question(self, question: str) -> dict:
        """Parse a question and return the interpreted data.

        Uses the Socratic method: identify the core concept being questioned,
        strip surface-level phrasing, and extract key terms for follow-up probing.
        """
        question = question.strip()
        words = question.lower().split()

        # Identify interrogative word to categorise the question type
        interrogatives = {"what", "why", "how", "when", "where", "who", "which",
                          "is", "are", "can", "do", "does"}
        question_type = "open"
        for word in words:
            if word in interrogatives:
                question_type = word
                break

        # Extract key terms (non-stopwords, non-interrogatives)
        stopwords = {"a", "an", "the", "is", "are", "was", "were", "of", "in", "to",
                     "and", "or", "but", "for", "on", "at", "by", "with"} | interrogatives
        key_terms = [w.rstrip("?.!,") for w in words if w.rstrip("?.!,") and w not in stopwords]

        return {
            "original": question,
            "question_type": question_type,
            "key_terms": key_terms,
            "method": "socratic",
            "follow_up_prompts": [
                f"What do you mean by '{term}'?" for term in key_terms[:2]
            ],
        }


class ProjectBasedLearningHandler(QuestionHandler):
    def parse_question(self, question: str) -> dict:
        """Parse a question and return the interpreted data.

        Maps the question onto a project-based learning context: identify the
        learning objective, suggest a hands-on project or task, and note any
        prerequisite knowledge implied by the question.
        """
        question = question.strip()
        words = question.lower().split()

        stopwords = {"a", "an", "the", "is", "are", "was", "were", "of", "in", "to",
                     "and", "or", "but", "for", "on", "at", "by", "with", "what",
                     "why", "how", "when", "where", "who", "which", "can", "do", "does"}
        key_terms = [w.rstrip("?.!,") for w in words if w.rstrip("?.!,") and w not in stopwords]

        # Build a simple project suggestion from the key terms
        topic = " ".join(key_terms[:3]) if key_terms else "the topic"
        project_suggestion = f"Build a small project that demonstrates {topic}."

        return {
            "original": question,
            "key_terms": key_terms,
            "method": "project_based_learning",
            "learning_objective": f"Understand {topic} through hands-on practice.",
            "project_suggestion": project_suggestion,
            "prerequisites": key_terms[3:] if len(key_terms) > 3 else [],
        }


class ResponseGenerator(ABC):
    @abstractmethod
    def generate_response(self, interpreted_data: dict, user_data: dict) -> str:
        pass


class ContextualResponseGenerator(ResponseGenerator):
    def generate_response(self, interpreted_data: dict, user_data: dict) -> str:
        """Generate a response based on the interpreted data and user data.

        Combines the parsed question context with user-specific data to produce
        a targeted, method-aware response string.
        """
        method = interpreted_data.get("method", "unknown")
        original = interpreted_data.get("original", "")
        key_terms = interpreted_data.get("key_terms", [])
        user_name = user_data.get("name", "learner")

        if method == "socratic":
            follow_ups = interpreted_data.get("follow_up_prompts", [])
            follow_up_text = "  ".join(follow_ups) if follow_ups else ""
            response = (
                f"Hello {user_name}, let's explore your question: \"{original}\"\n"
                f"Key concepts identified: {', '.join(key_terms)}.\n"
            )
            if follow_up_text:
                response += f"To dig deeper, consider: {follow_up_text}"
        elif method == "project_based_learning":
            objective = interpreted_data.get("learning_objective", "")
            project = interpreted_data.get("project_suggestion", "")
            response = (
                f"Great question, {user_name}! Your question: \"{original}\"\n"
                f"Learning objective: {objective}\n"
                f"Suggested project: {project}"
            )
        else:
            response = (
                f"Hello {user_name}, you asked: \"{original}\"\n"
                f"Key terms: {', '.join(key_terms)}."
            )

        return response

class LearningSession:
    def __init__(self, question_handler: QuestionHandler, response_generator: ResponseGenerator):
        self.question_handler = question_handler
        self.response_generator = response_generator

    def start(self, question: str):
        interpreted_data = self.question_handler.parse_question(question)
        # response = self.response_generator.generate_response(interpreted_data, user_data)
        # Add interactivity by returning or presenting the response


# app.py


def start_conversation(project_dependencies=None, conversations=None) -> None:
    question_handler = project_dependencies.create_question_handler()
    response_generator = project_dependencies.create_response_generator()

    learning_session = conversations.LearningSession(question_handler, response_generator)
    while True:
        user_question = input("Ask a question: ")
        learning_session.start(user_question)


if __name__ == "__main__":
    start_conversation()