"""dspygen REST API."""
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware

from dspygen.rdddy.abstract_command import AbstractCommand
from dspygen.rdddy.actor_system import ActorSystem
from dspygen.utils.file_tools import dspy_modules_dir
from dspygen.workflow.workflow_router import router as workflow_router


app = FastAPI()


from importlib import import_module
import os

from dspygen.dsl.dsl_pipeline_executor import router as pipeline_router


@app.on_event("startup")
async def startup_event():
    global actor_system
    actor_system = ActorSystem()


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
        actor_system = ActorSystem()

    return actor_system  # Assume actor_system is globally available


@app.get("/")
async def read_root(asys: ActorSystem = Depends(get_actor_system)):
    """Read root."""
    await asys.publish(AbstractCommand(content="Hello world"))

    return "Hello world"


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
