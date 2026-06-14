"""dspygen REST API."""
import datetime as dt
import os
from contextlib import asynccontextmanager
from importlib import import_module

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware

# from dspygen.experiments.convo_ddd.abstract_aggregate.conversation_aggregate import ConversationAggregate
# from dspygen.experiments.convo_ddd.abstract_event.user_input_received_event import UserInputReceivedEvent
from dspygen.rdddy.base_command import BaseCommand
from dspygen.rdddy.service_colony import ServiceColony
from dspygen.utils.file_tools import dspy_modules_dir
from dspygen.workflow.workflow_router import router as workflow_router

from dspygen.llm_pipe.dsl_pipeline_executor import router as pipeline_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await get_service_colony()
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(pipeline_router)
app.include_router(workflow_router)


def load_module_routers(app: FastAPI) -> None:
    for filename in os.listdir(dspy_modules_dir()):
        if filename.endswith(".py"):
            module_name = filename[:-3]
            module = import_module(f"dspygen.modules.{module_name}")
            if hasattr(module, "router"):
                app.include_router(module.router)


async def get_service_colony() -> ServiceColony:
    global service_colony

    try:
        service_colony
    except NameError:
        mqtt_url = os.environ.get("MQTT_BROKER_URL", "localhost:1883")
        mqtt_host, mqtt_port_str = mqtt_url.rsplit(":", 1)
        mqtt_port = int(mqtt_port_str)
        service_colony = ServiceColony(mqtt_broker=mqtt_host, mqtt_port=mqtt_port)

    return service_colony  # Assume service_colony is globally available


@app.get("/")
async def read_root(user_input: str, asys: ServiceColony = Depends(get_service_colony)) -> str:
    """Read root."""
    return "Hello, world!"
    # convo_agg: ConversationAggregate = await asys.inhabitant_of(ConversationAggregate)
    # msg = await convo_agg.handle_user_input(UserInputReceivedEvent(content=user_input))
    # return msg.model_dump()


# Define endpoint
@app.get("/pingpong")
def ping_pong() -> dict:
    return {"message": "pong"}


@app.get("/health")
async def health() -> dict:
    """Run all registered health checks and return aggregated status."""
    from dspygen.observability.health import check_all
    results = check_all()
    status = "ok" if all(r.status != "fail" for r in results) else "degraded"
    return {"status": status, "checks": [r.__dict__ for r in results]}


@app.get("/metrics")
async def metrics() -> dict:
    """Return all collected in-memory metrics."""
    from dspygen.observability.metrics import get_all_metrics
    return get_all_metrics()


# Add CORS middleware
cors_origins_env = os.environ.get("CORS_ORIGINS", "*")
cors_origins = [origin.strip() for origin in cors_origins_env.split(",")] if cors_origins_env != "*" else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Adjust as per your requirements
    allow_headers=["*"],  # Adjust this to your specific headers if needed
)
