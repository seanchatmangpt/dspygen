ADR-0004: RDDDY for Domain Modeling
=====================================

:Status: Accepted
:Date: 2024-09-14
:Deciders: Sean Chatman

Context
-------

Complex agentic workflows need structure beyond simple function calls. We need explicit domain objects for commands, events, queries, and aggregates.

Decision
--------

Implement **RDDDY** (Reactive Domain-Driven Design with Inhabitants) as the structural framework for domain modeling in dspygen.

Rationale
---------

- Explicit Commands/Events/Queries document intent and make event sourcing natural
- Aggregates enforce invariants and own their state
- Sagas coordinate multi-step workflows with compensation
- Pykka actors provide lightweight concurrency for reactive patterns
- Enables event storming as a design practice

Consequences
------------

- ``src/dspygen/rdddy/`` contains all base classes
- New domain features should model Commands and Events explicitly
- BaseMessage uses UUID v4 for all message IDs
- MCP tools expose RDDDY scaffolding (``scaffold_domain``, ``create_aggregate``, etc.)
