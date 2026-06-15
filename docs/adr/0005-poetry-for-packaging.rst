ADR-0005: Poetry for Package Management
========================================

:Status: Accepted
:Date: 2024-09-14
:Deciders: Sean Chatman

Context
-------

Python packaging requires choosing between pip+requirements.txt, pipenv, Poetry, and PDM.

Decision
--------

Use **Poetry** with ``pyproject.toml`` for all dependency management and packaging.

Rationale
---------

- Single ``pyproject.toml`` file for all metadata, dependencies, and tool config
- Lock file (``poetry.lock``) ensures reproducible installs
- Dependency groups (test, dev, docs, llm, retrieval) allow selective installs
- Extras (``pip install "dspygen[mcp]"``) enable optional features
- Poetry's resolver handles complex constraints better than pip

Consequences
------------

- ``poetry install`` for development, ``poetry install --only main`` for production
- Dependency groups prevent test/dev packages in production images
- Version bumps go through ``scripts/bump_version.py``
- CI uses ``poetry install --no-interaction`` with cached virtualenv
