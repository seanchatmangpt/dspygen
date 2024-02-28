"""dspygen REST API."""
import importlib
import logging
import os

import coloredlogs
from fastapi import FastAPI

from dspygen.utils.file_tools import dspy_modules_dir

app = FastAPI()

from importlib import import_module
import os


def load_module_routers(app: FastAPI):
    for filename in os.listdir(dspy_modules_dir()):
        if filename.endswith("_module.py"):
            module_name = filename[:-3]
            module = import_module(f"dspygen.modules.{module_name}")
            if hasattr(module, "router"):
                app.include_router(module.router)


@app.on_event("startup")
def startup_event() -> None:
    """Run API startup events."""
    # Remove all handlers associated with the root logger object.
    for handler in logging.root.handlers:
        logging.root.removeHandler(handler)
    # Add coloredlogs' coloured StreamHandler to the root logger.
    coloredlogs.install()
    load_module_routers(app)



@app.get("/")
def read_root() -> str:
    """Read root."""
    return "Hello world"


# Define endpoint
@app.get("/pingpong")
def ping_pong():
    return {"message": "pong"}
