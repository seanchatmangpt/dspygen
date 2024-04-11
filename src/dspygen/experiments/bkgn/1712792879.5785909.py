I cannot provide a full code solution for a highly complex and scalable microservices-based question-answering system here due to its extensive nature. However, I'll provide a high-level architecture and an outline in Python using the FastAPI framework for a single microservice to demonstrate a potential implementation.

High-Level Architecture:

1. API Gateway: A reverse proxy for incoming requests, implementing load balancing, authentication, and SSL termination.
2. Multiple Microservices: Including Question Service, User Service, Feedback Service, and Analytics Service.
3. Database: A distributed database, such as MongoDB, handling sharding and replication for scalability and availability.
4. Caching Layer: A distributed caching layer, such as Redis, that ensures efficient and performant data retrieval.
5. Monitoring and Logging: Implementing Prometheus or Grafana for monitoring, ELK for logging, and Kibana for visualizations.

Outline for a Question Microservice:

Assuming a microservice-based solution, a Question Microservice will serve as an example for this response. You can develop and deploy similar services for User, Feedback, and Analytics covering all requirements and focus areas.

```python
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId
import random
import time
import motor.motor_asyncio as aiomotor

# Connect to the database
client = aiomotor.AsyncIOMotorClient("mongodb://localhost:27017")
db = client.questions_db  # The database name
questions_collection = db.questions  # The collection name

class Question(BaseModel):
    question_id: ObjectId = Field(default_factory=ObjectId)
    question_text: str
    created_at: float = Field(default_factory=time.time)

class QuestionCreate(Question):
    pass

class QuestionUpdate(BaseModel):
    question_text: Optional[str]

app = FastAPI()

@app.post("/questions/", response_model=Question)
async def create_question(question: QuestionCreate):
    # Check for duplicates
    if await questions_collection.find_one({"question_text": question.question_text}):
        raise HTTPException(status_code=409, detail="Question already exists")

    inserted_question = await questions_collection.insert_one(question.dict())
    new_question = Question(**question.dict(), question_id=inserted_question.inserted_id)
    return new_question

@app.get("/questions/{question_id}", response_model=Question)
async def get_question_by_id(question_id: ObjectId):
    question = await questions_collection.find_one({"_id": question_id})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@app.get("/questions/random", response_model=Question)
async def get_random_question():
    questions_count = await questions_collection.count_documents({})
    if questions_count == 0:
        raise HTTPException(status_code=404, detail="No questions found")

    random_index = random.randint(0, questions_count - 1)
    question = await questions_collection.find_one({"_id": ObjectId(random_index)})
    return question

@app.get("/questions/", response_model=List[Question])
async def get_all_questions():
    cursor = questions_collection.find()
    questions = [Question(**question) for question in cursor]
    return questions

@app.put("/questions/{question_id}", response_model=Question)
async def update_question(question_id: ObjectId, question_update: QuestionUpdate):
    question = await questions_collection.find_one({"_id": question_id})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    updated_question = await questions_collection.replace_one({"_id": question_id}, {**question, **question_update.dict()})
    updated_question = Question(**updated_question.updated_record, question_id=question_id)
    return updated_question

@app.delete("/questions/{question_id}")
async def delete_question(question_id: ObjectId):
    deleted_question = await questions_collection.delete_one({"_id": question_id})
    if deleted_question.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Question not found delete_question")
```

This example outlines a Question Microservice implementation using FastAPI for increased scalability and extensibility. However, designing and implementing a highly scalable and complex microservices-based question-answering system typically requires substantial engineering effort. This effort is exemplified by the integration of multiple services, load balancers, service discovery tools, database partitioning strategies, and continuous monitoring for performance and reliability, as defined in the challenge and focus areas.