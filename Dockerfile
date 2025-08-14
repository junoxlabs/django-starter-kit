# syntax=docker/dockerfile:1

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY pyproject.toml .

RUN pip install uv
RUN uv pip install --system --no-cache -r pyproject.toml

COPY . .

CMD ["uv", "run", "granian", "--interface", "asgi", "--log-level", "info", "config.asgi:application"]