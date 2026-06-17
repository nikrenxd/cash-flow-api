FROM python:3.13-slim AS base


ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=1

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app/

FROM base AS final

RUN apt-get update && apt-get install -y netcat-openbsd

COPY ../pyproject.toml ../uv.lock /app/
RUN uv pip install -r pyproject.toml --group dev

COPY ./src/ /app/src/