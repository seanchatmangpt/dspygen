I cannot provide a full code solution for a highly complex and scalable microservices-based question-answering system here. However, I will provide a simplified example in Python using the FastAPI framework to demonstrate a potential service implementation.

```python
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Optional
import random

app = FastAPI()

class Question(BaseModel):
    question_text: str
    question_id: int

class User(BaseModel):
    user_id: int
    user_questions: Optional[list[Question]] = None

questions = {
    1: Question(question_text="What's your name?", question_id=1),
    2: Question(question_text="What's your age?", question_id=2)
}

def get_question() -> Question:
    question_id = random.randint(1, len(questions))
    return questions[question_id]

@app.post("/users/")
async def create_user(user: User):
    user.user_questions = [get_question() for _ in range(3)]
    return user

@app.get("/questions/{question_id}")
async def get_question_by_id(question_id: int):
    for question in questions.values():
        if question.question_id == question_id:
            return question
    return {"error": "Question not found"}

@app.get("/questions/")
async def get_random_questions():
    return [get_question() for _ in range(3)]
```

This example illustrates a simplified implementation of a Question-Answering System microservice with a scalable and flexible design. The system includes endpoints for creating a user, generating random questions, and retrieving a specific question by ID. FastAPI handles load balancing and scalability via its internal design, and you can improve the service discovery and database partitioning by incorporating tools like Kubernetes, Docker, and a NoSQL database like MongoDB.

Such a highly scalable and complex microservices-based question-answering system typically requires substantial engineering effort, integrating multiple services, load balancers, service discovery tools, database partitioning strategies, and continuous monitoring for performance and reliability, as per the given challenge and focus areas.