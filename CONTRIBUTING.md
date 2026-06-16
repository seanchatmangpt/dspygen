# Contributing to DSPyGen

Thank you for your interest in contributing! This guide covers everything you
need to go from a fresh clone to a merged pull request.

---

## Table of Contents

1. [Development Setup](#development-setup)
2. [Running Tests](#running-tests)
3. [Running Servers](#running-servers)
4. [Code Style](#code-style)
5. [PR Process](#pr-process)

---

## Development Setup

DSPyGen uses [Poetry](https://python-poetry.org/) for dependency management.

### Prerequisites

- Python 3.10 or later
- [Poetry](https://python-poetry.org/docs/#installation) 1.8+
- (Optional) [Ollama](https://ollama.ai/) for local model testing

### Install all extras

```bash
git clone https://github.com/seanchatmangpt/dspygen.git
cd dspygen

# Install the package plus every optional dependency group
poetry install --all-extras

# Activate the virtual environment
poetry shell
```

The `--all-extras` flag installs the `lsp`, `mcp`, `jupyter`, `dev`, and `docs`
dependency groups.  If you only need a subset, pass the specific extras:

```bash
poetry install --extras "lsp mcp"
```

### Environment variables

Copy the example file and fill in your API keys:

```bash
cp .env.example .env
# then edit .env with your actual keys
```

Load the variables into your shell before running any command that calls an LLM:

```bash
export $(grep -v '^#' .env | xargs)
# or use direnv: echo "dotenv" >> .envrc && direnv allow
```

---

## Running Tests

DSPyGen's test suite is organised into unit tests, MCP integration tests, and
LSP integration tests.  A top-level `Makefile` provides convenient targets.

### All tests (unit + integration)

```bash
make test
```

This runs `pytest tests/` with the project's default configuration in
`pyproject.toml`.

### MCP integration tests

Tests that start the MCP server and exercise all 66 tools end-to-end:

```bash
make test-mcp
```

Equivalent to:

```bash
pytest tests/mcp/ -v --timeout=60
```

Set `OPENAI_API_KEY` (or configure a mock LM) before running these tests,
as many tools invoke a language model.

### LSP integration tests

Tests that launch the LSP server and send JSON-RPC messages covering all
14 capabilities:

```bash
make test-lsp
```

Equivalent to:

```bash
pytest tests/lsp/ -v --timeout=60
```

### Running a single test file

```bash
pytest tests/test_blog_module.py -v
```

### Useful pytest flags

| Flag | Purpose |
|------|---------|
| `-x` | Stop on the first failure |
| `-k "blog"` | Run only tests whose names match `blog` |
| `--lf` | Re-run only the tests that failed last time |
| `-s` | Show stdout / `print()` output |
| `-v` | Verbose: show each test name |
| `--tb=short` | Short tracebacks (default is `long`) |

---

## Running Servers

### MCP server

Start the MCP server over stdio (default transport used by Claude Desktop,
Cursor, and Continue):

```bash
dspygen mcp serve
```

Start over SSE on a custom port (useful for browser-based clients):

```bash
dspygen mcp serve --transport sse --port 8000
```

You can also start the server programmatically:

```python
from dspygen.mcp.server import create_server
import asyncio

server = create_server()
asyncio.run(server.run_stdio())
```

### LSP server

Start the LSP server over stdio (the transport used by most editors):

```bash
dspygen lsp serve
```

Start over TCP (useful for debugging with raw JSON-RPC):

```bash
dspygen lsp serve --tcp --host 127.0.0.1 --port 2087
```

Programmatic start:

```python
from dspygen.lsp.server import create_lsp_server
import asyncio

server = create_lsp_server()
asyncio.run(server.start_io())
```

---

## Code Style

DSPyGen uses [Ruff](https://docs.astral.sh/ruff/) for linting and formatting.

### Check for linting issues

```bash
ruff check .
```

### Auto-fix fixable issues

```bash
ruff check --fix .
```

### Format code

```bash
ruff format .
```

### Type checking

```bash
mypy src/dspygen
```

### Pre-commit hooks

A `.pre-commit-config.yaml` is provided.  Install the hooks once:

```bash
pre-commit install
```

After that, `ruff check`, `ruff format`, and `mypy` run automatically on
every `git commit`.

---

## PR Process

1. **Fork** the repository and create a feature branch off `main`:

   ```bash
   git checkout -b feat/my-new-feature
   ```

2. **Write your code** following the style guidelines above.

3. **Add or update tests** in the appropriate `tests/` subdirectory.  New
   modules should have at least one unit test in `tests/modules/`.

4. **Run the full test suite** locally to confirm nothing is broken:

   ```bash
   make test
   ```

5. **Commit** with a conventional commit message:

   ```
   feat: add FooBarModule for summarising foo into bar
   fix: handle empty prediction in GenDspyModule
   docs: add Neovim LSP setup instructions
   test: add integration tests for run_pipeline MCP tool
   ```

6. **Push** your branch and open a pull request against `main`.  Fill in the
   PR template — describe what changed, why, and how to test it.

7. **CI must pass** — all seven GitHub Actions workflows must be green before
   a maintainer will review the PR.

8. A maintainer will review your PR, leave feedback, and merge it once
   approved.  Squash merges are used to keep `main`'s history linear.

### Reporting bugs

Open a [GitHub Issue](https://github.com/seanchatmangpt/dspygen/issues) with:

- A minimal reproducible example
- The DSPyGen version (`dspygen --version`)
- Python version and OS
- The full traceback

### Requesting features

Open a GitHub Issue with the `enhancement` label.  Describe the use case and
the proposed API before writing any code — it saves everyone time if the
design is agreed on first.
