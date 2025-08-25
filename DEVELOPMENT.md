### Developer.md

# Developer Guide

This document provides in-depth guidance for developers working on or extending this starter kit.

---

## Docker Development Environment

The project includes a complete Docker development environment with all necessary services:

### Services Included:

- **PostgreSQL (ParadeDB)** - Database
- **Redis (valkey 7)** - Cache and session storage
- **RabbitMQ 4** - Message broker for Dramatiq
- **MinIO (bitnami/minio:2025.4.22 -- last version with usable webui)** - S3-compatible object storage (TODO: find alternative of minio for dev environments)

### Development Commands:

```bash
# Start development environment (detached)
make dev-up

# Stop development environment
make dev-down

# Follow container logs
make dev-logs

# Clean up containers and volumes
make dev-clean

# Restart development environment
make dev-restart

# Access container shell
make dev-shell
```

### Directory Structure:

```
dev/
├── Dockerfile          # Development Docker image definition
├── docker-compose.dev.yml  # Development services configuration
├── supervisord.conf    # Process management configuration
└── init.sh            # Container initialization script
```

---

## Architectural Philosophy

The primary goal is **separation of concerns** and **developer velocity**.

- **`apps/` vs `frontend/`:** The `apps/` directory is exclusively for Python/Django code. All frontend source code (JS, CSS, images) lives in the `frontend/` directory. This creates a clean boundary and allows frontend and backend developers to work without conflict.
- **The `core` App:** This app is for truly universal, project-wide code, such as abstract models (`BaseModel`) and utility functions that don't belong to a specific business domain. Be disciplined. If a piece of functionality starts to grow (e.g., notifications), it should be extracted into its own app (`apps/notifications`).
- **Fat Models, Thin Views:** Business logic should primarily reside in models, managers, and dedicated service functions. Views and API endpoints should be thin layers responsible for handling HTTP requests/responses and delegating logic.

---

## Dependency Management

- **Python:** All Python dependencies are managed by `uv` in `pyproject.toml`.

  - To add a new dependency: `uv add <package-name>`
  - This will automatically update `pyproject.toml`. Remember to commit this file.

- **Frontend:** Frontend dependencies are managed by `bun` (or your preferred JS package manager) via the `frontend/package.json` file. Run `bun install` inside the `web` container to install them.

---

## Frontend Workflow with Vite

- **Development:** When you run `docker-compose up`, the Vite development server starts automatically and proxies requests from Django. It provides Hot Module Replacement (HMR) for near-instant updates in the browser as you edit CSS and JS files in `frontend/assets/`.
- **Building for Production:** The `Dockerfile` for the production image contains a stage that runs `npm run build`. This command invokes Vite to compile, minify, and hash all frontend assets, placing the output in `static/dist/`. In production, Django uses these compiled files directly.

---

## Database Conventions

- **Models:** All new models should inherit from `apps.core.models.BaseModel`. If the model represents data that should not be permanently deleted (e.g., users, orders), it should inherit from `apps.core.models.SoftDeleteModel`.
- **Query Performance:** Always use `select_related` (for foreign keys/one-to-one) and `prefetch_related` (for many-to-many/reverse relations) in your querysets to prevent N+1 query problems. The Django Debug Toolbar is installed in development to help identify these issues.

---

## CI/CD Pipeline

The `.github/workflows/ci.yml` pipeline automates quality checks on every push and pull request. It performs the following steps:

1.  **Linting:** Runs `ruff check` to find code style issues.
2.  **Type Checking:** Runs `mypy` to enforce static type hints.
3.  **Testing:** Runs the full `pytest` suite against the test database.
4.  **Builds:** Verifies that the Docker image and frontend assets can be built successfully.
