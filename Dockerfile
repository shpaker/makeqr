FROM ghcr.io/astral-sh/uv:0.11-python3.13-trixie-slim AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

# Build the venv at the path it will live at in the runtime image: entry point
# shebangs bake in an absolute path.
WORKDIR /app

# Dependencies first: they change far less often than the sources.
COPY pyproject.toml uv.lock README.md LICENSE ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-editable --no-install-project

COPY makeqr ./makeqr
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-editable


FROM python:3.13-slim-trixie AS runtime

RUN useradd --create-home --uid 1000 makeqr
COPY --from=builder --chown=makeqr:makeqr /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"
USER makeqr
WORKDIR /home/makeqr

ENTRYPOINT ["makeqr"]
