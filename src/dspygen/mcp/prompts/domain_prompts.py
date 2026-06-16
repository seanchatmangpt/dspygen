"""
MCP Prompt library — Domain-Driven Design / RDDDY prompts.

10 prompts covering DDD and RDDDY design tasks.
"""

from __future__ import annotations

from mcp import types

__all__ = ["DOMAIN_PROMPTS", "DOMAIN_RENDERERS"]


def _msg(text: str) -> list[types.PromptMessage]:
    return [types.PromptMessage(role="user", content=types.TextContent(type="text", text=text))]


# ---------------------------------------------------------------------------
# Prompt: design-bounded-context
# ---------------------------------------------------------------------------

_DESIGN_BOUNDED_CONTEXT = types.Prompt(
    name="design-bounded-context",
    description=(
        "Design a DDD Bounded Context from a business domain description. "
        "Produces ubiquitous language, aggregate roots, domain events, and context map."
    ),
    arguments=[
        types.PromptArgument(name="domain_description", description="High-level business domain description", required=True),
        types.PromptArgument(name="team_context", description="Team or organisational context", required=False),
    ],
)


def _render_design_bounded_context(args: dict) -> list[types.PromptMessage]:
    domain = args.get("domain_description", "")
    team = args.get("team_context", "")
    text = (
        "You are an expert Domain-Driven Design architect.\n\n"
        f"Design a comprehensive Bounded Context for the following domain:\n\n"
        f"**Domain:** {domain}\n"
        + (f"**Team context:** {team}\n" if team else "")
        + "\n"
        "Provide:\n"
        "1. **Bounded Context Name** — a clear, meaningful name\n"
        "2. **Ubiquitous Language** — 10–15 key domain terms with definitions\n"
        "3. **Aggregate Roots** — main aggregates with their responsibilities\n"
        "4. **Domain Events** — key events that occur in this context (past tense)\n"
        "5. **Commands** — actions that change state (imperative mood)\n"
        "6. **Queries** — read operations (CQRS read side)\n"
        "7. **Context Map** — how this context relates to other contexts\n"
        "8. **dspygen RDDDY mapping** — map each element to the correct RDDDY base class\n\n"
        "Format each section clearly with headers and bullet points."
    )
    return _msg(text)


# ---------------------------------------------------------------------------
# Prompt: create-aggregate-root
# ---------------------------------------------------------------------------

_CREATE_AGGREGATE_ROOT = types.Prompt(
    name="create-aggregate-root",
    description=(
        "Generate a complete RDDDY aggregate root class with commands, events, and invariants."
    ),
    arguments=[
        types.PromptArgument(name="aggregate_name", description="Name of the aggregate root", required=True),
        types.PromptArgument(name="domain_context", description="Domain context and business rules", required=True),
        types.PromptArgument(name="operations", description="Comma-separated list of operations (create, update, cancel, etc.)", required=False),
    ],
)


def _render_create_aggregate_root(args: dict) -> list[types.PromptMessage]:
    name = args.get("aggregate_name", "")
    context = args.get("domain_context", "")
    ops = args.get("operations", "create, update, delete")
    text = (
        "You are an expert DDD developer using the dspygen RDDDY framework.\n\n"
        f"Generate a complete aggregate root for **{name}** in the following context:\n{context}\n\n"
        f"Operations to support: {ops}\n\n"
        "Produce:\n"
        "1. **`{name}Aggregate`** — extends `BaseAggregate`, with:\n"
        "   - Pydantic fields for state\n"
        "   - Command handler methods\n"
        "   - Domain invariant checks\n"
        "2. **Command classes** — one per operation, extending `BaseCommand`\n"
        "3. **Event classes** — one per operation (past tense), extending `BaseEvent`\n"
        "4. **Value Objects** — any embedded value objects needed\n\n"
        "All classes must import from `dspygen.rdddy.*` base classes.\n"
        "Include pydantic Field annotations with descriptions.\n"
        "Return complete, runnable Python source code."
    ).replace("{name}", name)
    return _msg(text)


# ---------------------------------------------------------------------------
# Prompt: event-storm-domain
# ---------------------------------------------------------------------------

_EVENT_STORM_DOMAIN = types.Prompt(
    name="event-storm-domain",
    description=(
        "Run a full Event Storming session on a domain and produce a complete event storm model."
    ),
    arguments=[
        types.PromptArgument(name="domain", description="Domain name or business area", required=True),
        types.PromptArgument(name="scenario", description="Specific scenario or use case to storm", required=True),
        types.PromptArgument(name="stakeholders", description="Key stakeholders or actors", required=False),
    ],
)


def _render_event_storm_domain(args: dict) -> list[types.PromptMessage]:
    domain = args.get("domain", "")
    scenario = args.get("scenario", "")
    stakeholders = args.get("stakeholders", "system users and administrators")
    text = (
        "You are a Domain Events expert facilitating an Event Storming workshop.\n\n"
        f"Run a complete Event Storming session for:\n"
        f"**Domain:** {domain}\n"
        f"**Scenario:** {scenario}\n"
        f"**Stakeholders:** {stakeholders}\n\n"
        "Produce a structured Event Storm with these colour-coded artifacts:\n\n"
        "🟠 **Domain Events** (orange) — things that happened, past tense, chronological\n"
        "🔵 **Commands** (blue) — actions that trigger events, imperative mood\n"
        "🟡 **Aggregates** (yellow) — cluster of objects handling commands\n"
        "🟣 **Policies** (purple) — automated reactions ('When X happens, do Y')\n"
        "🟢 **Read Models** (green) — views and projections needed\n"
        "🔴 **External Systems** (red) — third-party systems involved\n"
        "🩷 **Hotspots** (pink) — areas of uncertainty or debate\n\n"
        "Then map each artifact to the correct dspygen RDDDY class:\n"
        "- Events → `BaseEvent` subclass\n"
        "- Commands → `BaseCommand` subclass\n"
        "- Aggregates → `BaseAggregate` subclass\n"
        "- Policies → `BasePolicy` subclass\n"
        "- Read Models → `BaseReadModel` subclass\n\n"
        "Finally, suggest which artifacts to implement first (walking skeleton)."
    )
    return _msg(text)


# ---------------------------------------------------------------------------
# Prompt: design-saga
# ---------------------------------------------------------------------------

_DESIGN_SAGA = types.Prompt(
    name="design-saga",
    description="Design a RDDDY Saga for a long-running, multi-step business process.",
    arguments=[
        types.PromptArgument(name="process_name", description="Name of the business process", required=True),
        types.PromptArgument(name="steps", description="Comma-separated list of steps in the process", required=True),
        types.PromptArgument(name="compensations", description="What to do if a step fails (compensation transactions)", required=False),
    ],
)


def _render_design_saga(args: dict) -> list[types.PromptMessage]:
    process = args.get("process_name", "")
    steps = args.get("steps", "")
    compensations = args.get("compensations", "")
    text = (
        "You are an expert in distributed systems and Saga patterns.\n\n"
        f"Design a RDDDY Saga for the **{process}** process.\n\n"
        f"**Steps:** {steps}\n"
        + (f"**Compensations if failure:** {compensations}\n" if compensations else "")
        + "\n"
        "Produce:\n"
        "1. **Saga state diagram** — Mermaid stateDiagram-v2 showing happy path and compensation paths\n"
        "2. **`{process}Saga`** Python class extending `BaseSaga` with:\n"
        "   - State machine using transitions\n"
        "   - Step handler methods\n"
        "   - Compensation handlers\n"
        "   - Timeout handling\n"
        "3. **Commands issued** at each step\n"
        "4. **Events consumed** to trigger transitions\n"
        "5. **Idempotency strategy** for replay safety\n\n"
        "Use dspygen RDDDY imports: `from dspygen.rdddy.base_saga import BaseSaga`"
    ).replace("{process}", process)
    return _msg(text)


# ---------------------------------------------------------------------------
# Prompt: create-value-object
# ---------------------------------------------------------------------------

_CREATE_VALUE_OBJECT = types.Prompt(
    name="create-value-object",
    description="Generate a DDD Value Object with validation, equality, and factory methods.",
    arguments=[
        types.PromptArgument(name="value_object_name", description="Name of the value object", required=True),
        types.PromptArgument(name="attributes", description="Comma-separated list of attributes with types (e.g. 'amount:Decimal, currency:str')", required=True),
        types.PromptArgument(name="validation_rules", description="Business validation rules for this value object", required=False),
    ],
)


def _render_create_value_object(args: dict) -> list[types.PromptMessage]:
    vo_name = args.get("value_object_name", "")
    attributes = args.get("attributes", "")
    rules = args.get("validation_rules", "")
    text = (
        "You are an expert DDD developer.\n\n"
        f"Generate a complete Value Object for **{vo_name}**.\n\n"
        f"**Attributes:** {attributes}\n"
        + (f"**Validation rules:** {rules}\n" if rules else "")
        + "\n"
        "Requirements:\n"
        "1. Extend `BaseValueObject` from `dspygen.rdddy.base_value_object`\n"
        "2. Make it **immutable** (frozen Pydantic model)\n"
        "3. Implement **equality by value** (not identity)\n"
        "4. Add **`@validator`** or **`@model_validator`** for all business rules\n"
        "5. Add **factory class methods** for common construction patterns\n"
        "6. Add a `__str__` representation\n"
        "7. Include type hints and docstrings\n\n"
        "Return complete Python source code using Pydantic v2."
    )
    return _msg(text)


# ---------------------------------------------------------------------------
# Prompt: design-api
# ---------------------------------------------------------------------------

_DESIGN_API = types.Prompt(
    name="design-api",
    description="Design a REST/GraphQL API for a DDD bounded context with CQRS endpoints.",
    arguments=[
        types.PromptArgument(name="context_name", description="Bounded context name", required=True),
        types.PromptArgument(name="aggregates", description="Comma-separated list of aggregate names", required=True),
        types.PromptArgument(name="api_style", description="API style: rest, graphql, or grpc", required=False),
    ],
)


def _render_design_api(args: dict) -> list[types.PromptMessage]:
    ctx = args.get("context_name", "")
    aggregates = args.get("aggregates", "")
    style = args.get("api_style", "rest")
    text = (
        "You are an expert API architect using DDD and CQRS principles.\n\n"
        f"Design a **{style.upper()}** API for the **{ctx}** bounded context.\n\n"
        f"**Aggregates:** {aggregates}\n\n"
        "Design:\n"
        "1. **Command endpoints** — one per aggregate command (POST/mutation)\n"
        "2. **Query endpoints** — one per read model (GET/query)\n"
        "3. **Event stream endpoint** — SSE or WebSocket for domain events\n"
        "4. **Request/Response DTOs** — with validation rules\n"
        "5. **OpenAPI spec** or **GraphQL schema** (based on chosen style)\n"
        "6. **Error handling** — domain exception mapping to HTTP status codes\n"
        "7. **FastAPI implementation sketch** if REST, or strawberry/graphene if GraphQL\n\n"
        "Apply CQRS separation: commands change state, queries only read."
    )
    return _msg(text)


# ---------------------------------------------------------------------------
# Prompt: write-command-handler
# ---------------------------------------------------------------------------

_WRITE_COMMAND_HANDLER = types.Prompt(
    name="write-command-handler",
    description="Implement a command handler that validates, applies domain logic, and raises events.",
    arguments=[
        types.PromptArgument(name="command_name", description="Name of the command class", required=True),
        types.PromptArgument(name="aggregate_name", description="Name of the aggregate that handles this command", required=True),
        types.PromptArgument(name="business_rules", description="Business rules and invariants to enforce", required=True),
    ],
)


def _render_write_command_handler(args: dict) -> list[types.PromptMessage]:
    cmd = args.get("command_name", "")
    agg = args.get("aggregate_name", "")
    rules = args.get("business_rules", "")
    text = (
        "You are an expert DDD developer.\n\n"
        f"Implement a command handler for **{cmd}** on the **{agg}** aggregate.\n\n"
        f"**Business rules to enforce:**\n{rules}\n\n"
        "Implement:\n"
        "1. **`handle_{cmd}`** method on `{agg}Aggregate` that:\n"
        "   - Validates preconditions (raise `DomainException` if violated)\n"
        "   - Applies state changes\n"
        "   - Records domain events via `self._raise_event()`\n"
        "   - Enforces all invariants post-change\n"
        "2. **Unit tests** for happy path and each error case\n"
        "3. **Domain exception** classes for each business rule violation\n\n"
        "Use dspygen RDDDY imports. Keep logic in the domain layer (no infrastructure)."
    ).replace("{cmd}", cmd).replace("{agg}", agg)
    return _msg(text)


# ---------------------------------------------------------------------------
# Prompt: implement-policy
# ---------------------------------------------------------------------------

_IMPLEMENT_POLICY = types.Prompt(
    name="implement-policy",
    description="Implement a domain policy that reacts to events and issues commands.",
    arguments=[
        types.PromptArgument(name="policy_name", description="Name of the policy", required=True),
        types.PromptArgument(name="trigger_event", description="Domain event that triggers this policy", required=True),
        types.PromptArgument(name="resulting_command", description="Command issued when the policy fires", required=True),
    ],
)


def _render_implement_policy(args: dict) -> list[types.PromptMessage]:
    policy = args.get("policy_name", "")
    event = args.get("trigger_event", "")
    command = args.get("resulting_command", "")
    text = (
        "You are an expert DDD developer using the dspygen RDDDY framework.\n\n"
        f"Implement the **{policy}** domain policy.\n\n"
        f"**Trigger:** When `{event}` is received\n"
        f"**Action:** Issue `{command}` command\n\n"
        "Produce:\n"
        "1. **`{policy}`** class extending `BasePolicy` with:\n"
        "   - `handle_{event}(event)` method\n"
        "   - Condition checks before issuing the command\n"
        "   - Command construction and dispatch\n"
        "2. **Registration** — how to subscribe this policy to the event bus\n"
        "3. **Unit tests** covering: policy fires, policy condition not met\n"
        "4. **Mermaid sequence diagram** showing the event → policy → command flow\n\n"
        "Use dspygen RDDDY imports: `from dspygen.rdddy.base_policy import BasePolicy`"
    ).replace("{policy}", policy).replace("{event}", event)
    return _msg(text)


# ---------------------------------------------------------------------------
# Prompt: generate-read-model
# ---------------------------------------------------------------------------

_GENERATE_READ_MODEL = types.Prompt(
    name="generate-read-model",
    description="Generate a CQRS read model (projection) optimised for a specific query pattern.",
    arguments=[
        types.PromptArgument(name="model_name", description="Name of the read model", required=True),
        types.PromptArgument(name="query_use_case", description="What query does this model serve?", required=True),
        types.PromptArgument(name="source_events", description="Comma-separated domain events that update this model", required=True),
    ],
)


def _render_generate_read_model(args: dict) -> list[types.PromptMessage]:
    model = args.get("model_name", "")
    use_case = args.get("query_use_case", "")
    events = args.get("source_events", "")
    text = (
        "You are an expert CQRS developer.\n\n"
        f"Generate a read model for: **{model}**\n\n"
        f"**Query use case:** {use_case}\n"
        f"**Updated by events:** {events}\n\n"
        "Produce:\n"
        "1. **`{model}`** Pydantic model extending `BaseReadModel` with:\n"
        "   - All fields needed for the query use case\n"
        "   - Indexed fields annotated with comments\n"
        "2. **Projection handler** — methods to update the read model from each event:\n"
        "   - `handle_{event}(event)` methods\n"
        "   - Upsert logic\n"
        "3. **Query class** extending `BaseQuery` for this model\n"
        "4. **Repository interface** for persisting/retrieving the read model\n"
        "5. **Example query response** JSON\n\n"
        "Keep the read model denormalised for query performance."
    ).replace("{model}", model).replace("{event}", "event")
    return _msg(text)


# ---------------------------------------------------------------------------
# Prompt: scaffold-microservice
# ---------------------------------------------------------------------------

_SCAFFOLD_MICROSERVICE = types.Prompt(
    name="scaffold-microservice",
    description="Scaffold a complete microservice using dspygen RDDDY patterns with FastAPI and Docker.",
    arguments=[
        types.PromptArgument(name="service_name", description="Microservice name in snake_case", required=True),
        types.PromptArgument(name="domain_description", description="What this service is responsible for", required=True),
        types.PromptArgument(name="tech_stack", description="Additional tech: postgresql, redis, kafka, etc.", required=False),
    ],
)


def _render_scaffold_microservice(args: dict) -> list[types.PromptMessage]:
    service = args.get("service_name", "")
    domain = args.get("domain_description", "")
    stack = args.get("tech_stack", "postgresql, redis")
    text = (
        "You are an expert microservices architect using DDD and dspygen.\n\n"
        f"Scaffold a complete microservice for **{service}**.\n\n"
        f"**Responsibility:** {domain}\n"
        f"**Tech stack:** FastAPI, dspygen RDDDY, {stack}\n\n"
        "Generate the full project structure:\n"
        "```\n"
        f"{service}/\n"
        f"  src/{service}/\n"
        f"    domain/      # aggregates, events, commands, queries, sagas, policies\n"
        f"    application/ # command/query handlers, use cases\n"
        f"    infrastructure/ # repositories, event bus adapters\n"
        f"    api/         # FastAPI routes and DTOs\n"
        f"  tests/\n"
        f"  Dockerfile\n"
        f"  pyproject.toml\n"
        "```\n\n"
        "For each layer, provide:\n"
        "1. Complete file list with purpose\n"
        "2. Key code snippets for domain classes\n"
        "3. FastAPI router with CQRS endpoints\n"
        "4. Docker configuration\n"
        "5. Integration points with other services\n\n"
        "Use dspygen RDDDY base classes throughout."
    )
    return _msg(text)


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

DOMAIN_PROMPTS: list[types.Prompt] = [
    _DESIGN_BOUNDED_CONTEXT,
    _CREATE_AGGREGATE_ROOT,
    _EVENT_STORM_DOMAIN,
    _DESIGN_SAGA,
    _CREATE_VALUE_OBJECT,
    _DESIGN_API,
    _WRITE_COMMAND_HANDLER,
    _IMPLEMENT_POLICY,
    _GENERATE_READ_MODEL,
    _SCAFFOLD_MICROSERVICE,
]

DOMAIN_RENDERERS: dict = {
    "design-bounded-context": _render_design_bounded_context,
    "create-aggregate-root": _render_create_aggregate_root,
    "event-storm-domain": _render_event_storm_domain,
    "design-saga": _render_design_saga,
    "create-value-object": _render_create_value_object,
    "design-api": _render_design_api,
    "write-command-handler": _render_write_command_handler,
    "implement-policy": _render_implement_policy,
    "generate-read-model": _render_generate_read_model,
    "scaffold-microservice": _render_scaffold_microservice,
}
