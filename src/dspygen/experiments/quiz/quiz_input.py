import typer
from transitions import Machine
from typing import List
import json

app = typer.Typer()

# Value Objects
class Topic:
    def __init__(self, name: str, content: str):
        self.name = name
        self.content = content

class Question:
    def __init__(self, question: str, options: List[str], answer: str):
        self.question = question
        self.options = options
        self.answer = answer

# Domain Entities
class TutoringSession:
    def __init__(self, topics: List[Topic], questions: List[Question], current_topic_index: int = 0, score: int = 0):
        self.topics = topics
        self.questions = questions
        self.current_topic_index = current_topic_index
        self.score = score
        self.machine = Machine(model=self, states=['introduction', 'topic_exploration', 'quiz', 'completed'], initial='introduction')
        self.machine.add_transition('start_topic', 'introduction', 'topic_exploration')
        self.machine.add_transition('next_topic', '*', None, after='move_to_next_topic')
        self.machine.add_transition('start_quiz', 'topic_exploration', 'quiz', unless=['has_next_topic'])
        self.machine.add_transition('complete', 'quiz', 'completed')

    def has_next_topic(self):
        return self.current_topic_index < len(self.topics) - 1

    def get_current_topic(self) -> Topic:
        return self.topics[self.current_topic_index]

    def move_to_next_topic(self):
        if self.has_next_topic():
            self.current_topic_index += 1

    def explore_topic(self):
        current_topic = self.get_current_topic()
        typer.echo(f"Topic: {current_topic.name}")
        typer.echo(current_topic.content)

    def start_quiz(self):
        typer.echo("Let's put your knowledge to the test with a quiz!")
        typer.echo("Answer the following questions based on what you've learned.")

        for question in self.questions:
            typer.echo(question.question)
            for option in question.options:
                typer.echo(option)
            user_answer = typer.prompt("Enter your answer (A/B/C/D):")
            if user_answer.upper() == question.answer:
                typer.echo("Correct!")
                self.score += 1
            else:
                typer.echo(f"Incorrect. The correct answer is {question.answer}.")

        typer.echo(f"Quiz completed. Your score: {self.score}/{len(self.questions)}")

# Root Aggregate
class TutoringSessionAggregate:
    def __init__(self, session: TutoringSession):
        self.session = session

    def start_session(self):
        self.session.start_topic()

    def next_topic(self):
        if self.session.has_next_topic():
            self.session.move_to_next_topic()
        else:
            self.session.start_quiz()

    def complete_session(self):
        self.session.complete()

# Repository
class TutoringSessionRepository:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_session(self) -> TutoringSessionAggregate:
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                topics = [Topic(topic['name'], topic['content']) for topic in data['topics']]
                questions = [Question(question['question'], question['options'], question['answer']) for question in data['questions']]
                session = TutoringSession(topics, questions, data['current_topic_index'], data['score'])
                return TutoringSessionAggregate(session)
        except FileNotFoundError:
            typer.echo("No existing session found. Starting a new session.")
            return self.create_new_session()

    def save_session(self, session_aggregate: TutoringSessionAggregate):
        session = session_aggregate.session
        data = {
            'topics': [{'name': topic.name, 'content': topic.content} for topic in session.topics],
            'questions': [{'question': question.question, 'options': question.options, 'answer': question.answer} for question in session.questions],
            'current_topic_index': session.current_topic_index,
            'score': session.score
        }
        with open(self.file_path, 'w') as file:
            json.dump(data, file)

    def create_new_session(self) -> TutoringSessionAggregate:
        topics = [
            Topic("Topic 1: Introduction to Philosophy", "Philosophy is the study of fundamental questions about existence, knowledge, values, reason, and the mind."),
            Topic("Topic 2: Socratic Method", "The Socratic method is a form of dialogue and questioning used to stimulate critical thinking and draw out ideas.")
        ]
        questions = [
            Question("What is philosophy?", [
                "A. The study of fundamental questions about existence, knowledge, values, reason, and the mind",
                "B. A branch of science that deals with the natural world",
                "C. The practice of making persuasive arguments",
                "D. The art of creating beautiful works"
            ], "A"),
            Question("What is the goal of the Socratic method?", [
                "A. To memorize facts and information",
                "B. To engage in small talk and casual conversation",
                "C. To deepen understanding, encourage self-reflection, and facilitate the discovery of truth",
                "D. To prove one's superiority over others"
            ], "C")
        ]
        session = TutoringSession(topics, questions)
        return TutoringSessionAggregate(session)

@app.command()
def tutor(file_path: str = "session_data.json"):
    """
    Processes commands to navigate through the tutoring session and quiz.
    """
    repository = TutoringSessionRepository(file_path)
    session_aggregate = repository.load_session()
    session = session_aggregate.session

    while True:
        if session.state == 'introduction':
            typer.echo("Welcome to the Socratic Method Text Adventure!")
            typer.echo("In this game, you will explore philosophical concepts and engage in Socratic dialogue.")
            command = typer.prompt("Enter /start to begin:")
            if command == "/start":
                session_aggregate.start_session()
        elif session.state == 'topic_exploration':
            topic = session.get_current_topic()
            typer.echo(f"Current Topic: {topic.name}")
            session.explore_topic()
            command = typer.prompt("Enter /next to move to the next topic, or /quiz to start the quiz:")
            if command == "/next":
                session_aggregate.next_topic()
                if not session.has_next_topic():
                    session.start_quiz()
            elif command == "/quiz":
                session.start_quiz()
            else:
                typer.echo("Unknown command. Please try again.")
        elif session.state == 'quiz':
            session.start_quiz()
            command = typer.prompt("Enter /complete to finish the tutoring session:")
            if command == "/complete":
                session_aggregate.complete_session()
                repository.save_session(session_aggregate)
                typer.echo("Tutoring session completed. Thank you for participating!")
                break
            else:
                typer.echo("Unknown command. Please try again.")
        elif session.state == 'completed':
            break
        else:
            typer.echo("Unknown state. Please try again.")

        repository.save_session(session_aggregate)

if __name__ == "__main__":
    app()