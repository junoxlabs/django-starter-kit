# syntax=docker/dockerfile:1

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY pyproject.toml .

RUN pip install uv

# Install Python dependencies
COPY pyproject.toml .
RUN uv pip install --system --no-cache-dir .

# Install Bun and frontend dependencies
RUN apt-get update && apt-get install -y curl
RUN curl -fsSL https://bun.sh/install | bash
ENV PATH="/root/.bun/bin:$PATH"
COPY frontend/package.json frontend/bun.lockb ./frontend/
RUN cd frontend && bun install --frozen-lockfile

# Build frontend assets
COPY frontend/src ./frontend/src
COPY frontend/postcss.config.js frontend/vite.config.js ./frontend/
RUN cd frontend && bun run build

# Copy remaining project files
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uv", "run", "granian", "--interface", "asgi", "--log-level", "info", "config.asgi:application"]