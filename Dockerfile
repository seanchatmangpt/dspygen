# syntax=docker/dockerfile:1
# Multi-stage Dockerfile for dspygen — targets: deps, app, mcp, lsp, api, dev

ARG PYTHON_VERSION=3.11
ARG POETRY_VERSION=1.8.3
ARG UID=1000
ARG GID=1000

# ---------------------------------------------------------------------------
# Stage 1: base — minimal Python slim image with non-root user
# ---------------------------------------------------------------------------
FROM python:${PYTHON_VERSION}-slim AS base

# Keep apt cache available for build caching
RUN rm -f /etc/apt/apt.conf.d/docker-clean

ARG UID
ARG GID
RUN groupadd --gid ${GID} user && \
    useradd --create-home --gid ${GID} --uid ${UID} user --no-log-init && \
    chown user /opt/

USER user

# Create and activate a virtual environment
ENV VIRTUAL_ENV=/opt/dspygen-env
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"
RUN python -m venv ${VIRTUAL_ENV}

WORKDIR /app

# ---------------------------------------------------------------------------
# Stage 2: poetry-installer — install Poetry in an isolated venv
# ---------------------------------------------------------------------------
FROM base AS poetry-installer

USER root

ARG POETRY_VERSION
ENV POETRY_VIRTUAL_ENV=/opt/poetry-env
RUN --mount=type=cache,target=/root/.cache/pip/ \
    python -m venv ${POETRY_VIRTUAL_ENV} && \
    ${POETRY_VIRTUAL_ENV}/bin/pip install "poetry==${POETRY_VERSION}" && \
    ln -s ${POETRY_VIRTUAL_ENV}/bin/poetry /usr/local/bin/poetry

# Build tools needed for native extensions
RUN --mount=type=cache,target=/var/cache/apt/ \
    --mount=type=cache,target=/var/lib/apt/ \
    apt-get update && \
    apt-get install --no-install-recommends --yes build-essential curl

USER user

# ---------------------------------------------------------------------------
# Stage 3: deps — install only main (production) dependencies, no source
# ---------------------------------------------------------------------------
FROM poetry-installer AS deps

COPY --chown=user:user poetry.lock pyproject.toml ./
RUN mkdir -p src/dspygen && touch src/dspygen/__init__.py && touch README.md

ARG UID
RUN --mount=type=cache,uid=${UID},gid=${UID},target=/home/user/.cache/pypoetry/ \
    poetry install --only main --no-root --no-interaction

# ---------------------------------------------------------------------------
# Stage 4: app — copy source and install package (editable)
# ---------------------------------------------------------------------------
FROM deps AS app

COPY --chown=user:user src/ src/
RUN --mount=type=cache,uid=${UID},gid=${UID},target=/home/user/.cache/pypoetry/ \
    poetry install --only main --no-interaction

# ---------------------------------------------------------------------------
# Stage 5: mcp — MCP server target
# ---------------------------------------------------------------------------
FROM app AS mcp

EXPOSE 8765

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import socket; s=socket.socket(); s.settimeout(3); s.connect(('localhost',8765)); s.close()" || exit 1

CMD ["python", "-m", "dspygen.mcp.server", "--transport", "sse", "--port", "8765"]

# ---------------------------------------------------------------------------
# Stage 6: lsp — LSP server target
# ---------------------------------------------------------------------------
FROM app AS lsp

EXPOSE 2087

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import socket; s=socket.socket(); s.settimeout(3); s.connect(('localhost',2087)); s.close()" || exit 1

CMD ["python", "-m", "dspygen.lsp.server", "--transport", "tcp", "--port", "2087"]

# ---------------------------------------------------------------------------
# Stage 7: api — FastAPI / uvicorn target  (default production target)
# ---------------------------------------------------------------------------
FROM app AS api

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "dspygen.api:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]

# ---------------------------------------------------------------------------
# Stage 8: dev — full dev environment with tools, zsh, pre-commit, etc.
# ---------------------------------------------------------------------------
FROM poetry-installer AS dev

USER root
RUN --mount=type=cache,target=/var/cache/apt/ \
    --mount=type=cache,target=/var/lib/apt/ \
    apt-get update && \
    apt-get install --no-install-recommends --yes curl git gnupg ssh sudo vim zsh && \
    sh -c "$(curl -fsSL https://starship.rs/install.sh)" -- "--yes" && \
    usermod --shell /usr/bin/zsh user && \
    echo 'user ALL=(root) NOPASSWD:ALL' > /etc/sudoers.d/user && chmod 0440 /etc/sudoers.d/user

USER user

COPY --chown=user:user poetry.lock pyproject.toml ./
RUN mkdir -p src/dspygen && touch src/dspygen/__init__.py && touch README.md

ARG UID
RUN --mount=type=cache,uid=${UID},gid=${UID},target=/home/user/.cache/pypoetry/ \
    poetry install --with test,dev --no-interaction

COPY --chown=user:user .pre-commit-config.yaml ./
RUN mkdir -p /opt/build/poetry/ && cp poetry.lock /opt/build/poetry/ && \
    git init && pre-commit install --install-hooks && \
    mkdir -p /opt/build/git/ && cp .git/hooks/pre-commit /opt/build/git/ 2>/dev/null || true

ENV ANTIDOTE_VERSION=1.8.6
RUN git clone --branch v${ANTIDOTE_VERSION} --depth=1 https://github.com/mattmc3/antidote.git ~/.antidote/ && \
    echo 'zsh-users/zsh-syntax-highlighting' >> ~/.zsh_plugins.txt && \
    echo 'zsh-users/zsh-autosuggestions' >> ~/.zsh_plugins.txt && \
    echo 'source ~/.antidote/antidote.zsh' >> ~/.zshrc && \
    echo 'antidote load' >> ~/.zshrc && \
    echo 'eval "$(starship init zsh)"' >> ~/.zshrc && \
    echo 'HISTFILE=~/.history/.zsh_history' >> ~/.zshrc && \
    echo 'HISTSIZE=1000' >> ~/.zshrc && \
    echo 'SAVEHIST=1000' >> ~/.zshrc && \
    echo 'setopt share_history' >> ~/.zshrc && \
    mkdir ~/.history/ && \
    zsh -c 'source ~/.zshrc'

ENTRYPOINT ["/opt/dspygen-env/bin/poe"]
CMD ["api"]
