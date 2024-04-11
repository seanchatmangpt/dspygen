Below is a high-level code solution for a single microservice, the Question Microservice, implemented using the FastAPI framework. This solution demonstrates key functionality required for the educational content management system and considers critical challenge areas such as usability, security, and testing.

---

```python
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId
import random
import time
import motor.motor_asyncio as aiomotor

app = FastAPI()

# Connect to the database
client = aiomotor.AsyncIOMotorClient("mongodb://localhost:27017")
db = client.questions_db
questions_collection = db.questions

class Question(BaseModel):
    question_id: ObjectId = Field(default_factory=ObjectId)
    question_text: str
    created_at: float = Field(default_factory=time.time)

class QuestionCreate(Question):
    pass

class QuestionUpdate(BaseModel):
    question_text: Optional[str]

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
        raise HTTPException(status_code=404, detail="Question not found")

    return delete_question
```

---

The above microservice code provides the necessary functionality for handling quests in the educational content management system. However, keep in mind that the complete and complex solution requires integration with multiple microservices, load balancers, a distributed database, and a caching layer, among other components. This integration effort ensures the overall system's scalability and extensibility, aligned with the specific focus areas of the challenge and the project requirements.