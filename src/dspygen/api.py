"""dspygen REST API."""
import datetime as dt

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware

# from dspygen.experiments.convo_ddd.abstract_aggregate.conversation_aggregate import ConversationAggregate
# from dspygen.experiments.convo_ddd.abstract_event.user_input_received_event import UserInputReceivedEvent
from dspygen.rdddy.base_command import BaseCommand
from dspygen.rdddy.actor_system import ActorSystem
from dspygen.utils.file_tools import dspy_modules_dir
from dspygen.workflow.workflow_router import router as workflow_router


app = FastAPI()


from importlib import import_module
import os

from dspygen.dsl.dsl_pipeline_executor import router as pipeline_router


@app.on_event("startup")
async def startup_event():
    await get_actor_system()


app.include_router(pipeline_router)
app.include_router(workflow_router)


def load_module_routers(app: FastAPI):
    for filename in os.listdir(dspy_modules_dir()):
        if filename.endswith(".py"):
            module_name = filename[:-3]
            module = import_module(f"dspygen.modules.{module_name}")
            if hasattr(module, "router"):
                app.include_router(module.router)


async def get_actor_system():
    global actor_system

    try:
        actor_system
    except NameError:
        actor_system = ActorSystem(mqtt_broker="9.tcp.ngrok.io", mqtt_port=24651)

    return actor_system  # Assume actor_system is globally available


@app.get("/")
async def read_root(user_input: str, asys: ActorSystem = Depends(get_actor_system)):
    """Read root."""
    return "Hello, world!"
    # convo_agg: ConversationAggregate = await asys.actor_of(ConversationAggregate)
    # msg = await convo_agg.handle_user_input(UserInputReceivedEvent(content=user_input))
    # return msg.model_dump()


# Define endpoint
@app.get("/pingpong")
def ping_pong():
    return {"message": "pong"}


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your specific origins if needed
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Adjust as per your requirements
    allow_headers=["*"],  # Adjust this to your specific headers if needed
)
