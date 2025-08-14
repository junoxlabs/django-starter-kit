# Agent Logs

This file documents the implementation of the Django 5.2 LTS Starter Kit.

## Project Setup

- Initialized a new Django project.
- Configured `django-environ` to manage environment variables.
- Set up the project structure with `apps`, `config`, `frontend`, and `templates` directories.

## Dependencies

- Added the following dependencies to `pyproject.toml`:
  - `django`
  - `djangorestframework`
  - `django-environ`
  - `django-allauth`
  - `django-vite`
  - `django-imagekit`
  - `django-storages`
  - `django-anymail`
  - `django-actioncable`
  - `django-cors-headers`
  - `django-redis`
  - `whitenoise`
  - `celery`
  - `ruff`
  - `sentry-sdk`
  - `opentelemetry-sdk`
  - `opentelemetry-instrumentation-django`
  - `opentelemetry-instrumentation-celery`
  - `pytest`
  - `pytest-django`
  - `mypy`
  - `psycopg2-binary`
  - `pillow`
  - `boto3`
  - `requests`
  - `amqp`

## Backend

### Database

- Configured the project to use PostgreSQL with `psycopg2-binary`.
- Implemented ParadeDB search functionality with a custom `SearchManager`.

### Caching

- Configured Redis as the cache backend using `django-redis`.

### Task Queue

- Configured Celery with RabbitMQ as the message broker.

### Email

- Configured `django-anymail` with Postmark as the email backend.

### File Storage

- Configured `django-storages` to use Amazon S3 for file storage.

### Observability

- Set up Sentry and OpenTelemetry for error tracking and performance monitoring.

### Security

- Implemented production security best practices in `config/settings/production.py`.

### Models

- Created abstract base models `BaseModel` and `SoftDeleteModel` for common fields and soft delete functionality.

## Frontend

### Build Process

- Set up a Vite frontend build process with `vite.config.js` and `package.json`.

### Dependencies

- Added the following frontend dependencies:
  - `vite`
  - `@hotwired/stimulus`
  - `@hotwired/turbo`
  - `gsap`
  - `tailwindcss`
  - `postcss`
  - `autoprefixer`
  - `daisyui`

### Hotwire

- Implemented Hotwire (Turbo + Stimulus) for interactivity.

### Styling

- Set up Tailwind CSS v4 with Daisy UI for styling.

## Templates

- Created a base template structure with `base.html`, `_header.html`, and `_footer.html`.

## CI/CD

- Set up a GitHub Actions CI/CD pipeline to run tests on push and pull requests.
- Created a `Makefile` to standardize commands.