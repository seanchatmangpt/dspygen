.PHONY: install install-all test test-all test-mcp test-lsp test-coverage \
        lint lint-fix typecheck docs \
        mcp-serve lsp-serve api-serve \
        docker-build docker-up docker-down docker-test \
        pre-commit-install pre-commit-run \
        clean clean-all

# ---------------------------------------------------------------------------
# Python / Poetry
# ---------------------------------------------------------------------------

## Install main + test + dev dependencies
install:
	poetry install --with test,dev --no-interaction

## Install ALL optional dependency groups and extras
install-all:
	poetry install --all-extras --with test,dev,docs,jupyter,llm,retrieval --no-interaction

# ---------------------------------------------------------------------------
# Testing
# ---------------------------------------------------------------------------

## Run offline tests (excludes slow, requires_openai, requires_ollama)
test:
	poetry run pytest tests/ \
	  -m "not requires_openai and not requires_ollama and not slow" \
	  --tb=short -v

## Run the complete test suite (all markers)
test-all:
	poetry run pytest tests/ -v

## Run MCP server tests
test-mcp:
	poetry run pytest tests/ -v -m mcp --tb=short

## Run LSP server tests
test-lsp:
	poetry run pytest tests/ -v -m lsp --tb=short

## Run offline tests with HTML + terminal coverage report
test-coverage:
	poetry run pytest tests/ \
	  -m "not requires_openai and not requires_ollama and not slow" \
	  --cov=src/dspygen \
	  --cov-report=html:htmlcov \
	  --cov-report=xml:reports/coverage.xml \
	  --cov-report=term \
	  --tb=short

# ---------------------------------------------------------------------------
# Linting / formatting
# ---------------------------------------------------------------------------

## Check linting and formatting (CI-safe — no auto-fix)
lint:
	poetry run ruff check src/ tests/
	poetry run ruff format --check src/ tests/

## Auto-fix linting issues and reformat
lint-fix:
	poetry run ruff check --fix src/ tests/
	poetry run ruff format src/ tests/

# ---------------------------------------------------------------------------
# Type checking
# ---------------------------------------------------------------------------

## Run mypy type checking
typecheck:
	poetry run mypy src/dspygen/ --ignore-missing-imports

# ---------------------------------------------------------------------------
# Documentation
# ---------------------------------------------------------------------------

## Build Sphinx HTML docs
docs:
	@if [ -f docs/Makefile ]; then \
	  cd docs && poetry run make html; \
	else \
	  poetry run sphinx-build -b html docs/ docs/_build/html; \
	fi

## Serve docs locally (requires docs build first)
docs-serve:
	poetry run python -m http.server 8080 --directory docs/_build/html

# ---------------------------------------------------------------------------
# Servers (local dev)
# ---------------------------------------------------------------------------

## Start the MCP server (stdio transport by default)
mcp-serve:
	poetry run python -m dspygen.mcp.server

## Start the LSP server (stdio transport by default)
lsp-serve:
	poetry run python -m dspygen.lsp.server

## Start the API server (uvicorn, hot-reload)
api-serve:
	poetry run uvicorn dspygen.api:app --host 0.0.0.0 --port 8000 --reload

# ---------------------------------------------------------------------------
# Docker
# ---------------------------------------------------------------------------

## Build all Docker targets (api, mcp, lsp)
docker-build:
	docker build --target api -t dspygen:api .
	docker build --target mcp -t dspygen:mcp .
	docker build --target lsp -t dspygen:lsp .

## Start production services (api + chroma + redis)
docker-up:
	docker-compose --profile api --profile retrieval --profile cache up -d

## Stop all services
docker-down:
	docker-compose down

## Run tests inside Docker (isolated, no env vars needed)
docker-test:
	docker-compose -f docker-compose.test.yml run --rm test

## Run coverage inside Docker
docker-test-coverage:
	docker-compose -f docker-compose.test.yml run --rm test-coverage

# ---------------------------------------------------------------------------
# Pre-commit
# ---------------------------------------------------------------------------

## Install pre-commit hooks
pre-commit-install:
	poetry run pre-commit install --install-hooks

## Run pre-commit on all files
pre-commit-run:
	poetry run pre-commit run --all-files --color always

# ---------------------------------------------------------------------------
# Cleanup
# ---------------------------------------------------------------------------

## Remove Python bytecode and cache files
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .coverage htmlcov/ .mypy_cache/ .ruff_cache/ .pytest_cache/

## Remove everything including build artifacts and reports
clean-all: clean
	rm -rf dist/ reports/ docs/_build/ *.egg-info src/*.egg-info
