# BRIEF.md

### **1. Introduction**

#### **1.1. Purpose**

This document outlines the system architecture for a universal, modern, and efficient Django 5.2 LTS Starter Kit. Its primary purpose is to serve as a robust, secure, and flexible foundation for building high-performance web applications, from API services to content-driven sites.

#### **1.2. Scope**

The architecture covers the backend structure, data modeling, frontend integration, performance strategies, security considerations, and deployment. It is intended to guide development by providing a reusable boilerplate that prioritizes developer experience (DX), application performance, and long-term maintainability.

#### **1.3. Core Principles**

- **Modularity:** Functionality is built from independent, reusable Django apps.
- **Convention over Configuration:** A clear and logical project structure reduces cognitive overhead and ensures consistency.
- **Performance First:** The system is architected for speed, incorporating caching, asset optimization, and efficient data retrieval by default.
- **Decoupled Services:** The application, data, and message brokering layers are separated to enable independent scaling and improve resilience.
- **Streamlined Development (DX):** Provides a clean, well-documented, and modern development environment to maximize productivity.
- **Security by Default:** Integrates security best practices and tooling from the ground up.

---

### **2. System Architecture Overview**

The system is a modular monolithic web application built on the Django framework. While monolithic in codebase, its dependencies (database, cache, message broker) are decoupled services, enabling flexible deployment and scaling.

- **Presentation Layer (Frontend):** Renders the user interface using Django's templating engine, styled with Tailwind CSS, and enhanced with Hotwire (Turbo + Stimulus) for a single-page application (SPA) feel without the complexity of a heavy JavaScript framework.
- **Application Layer (Backend):** Contains the core business logic, managed by Django views, Django REST Framework (DRF) for APIs, and Celery for asynchronous tasks. It handles user requests, data processing, and routing.
- **Data Layer:** Manages data persistence, caching, and search. This includes a primary relational database (**ParadeDB**) for structured data and full-text search, and an in-memory cache (**Redis**) for high-speed data access.

---

### **3. Technology Stack**

All Python dependencies are managed by **`uv`** via a single `pyproject.toml` file.

- **Backend Framework:** Django 5.2 LTS
- **API Framework:** Django REST Framework (DRF)
- **Database:** ParadeDB (PostgreSQL 17 with search & analytics extensions)
- **Cache:** Redis (valkey 7)
- **Task Queue:** Celery + RabbitMQ (as the message broker)
- **Python Tooling:** `uv` (package manager), `ruff` (linter/formatter), `mypy` (type checker), `pytest` (testing)
- **Configuration:** `django-environ` (for managing settings via environment variables)
- **Authentication:** `django-allauth` (for social auth, OIDC, and local accounts)
- **Frontend Bundler:** Vite (`django-vite`)
- **Frontend Styling:** Tailwind CSS v4 + Daisy UI 5
- **Interactivity:** Hotwire (Turbo 8 + Stimulus 3) + GSAP 3 (for animations)
- **Real-time/WebSockets:** `@rails/actioncable@8` + `django-actioncable` (actioncable is a ported rails feature, use django-channels for websockets)
- **Email:** `django-anymail` (with a provider like Postmark or AWS SES)
- **File Storage:** `django-storages` (with an S3-compatible backend)
- **Media Processing:** `django-imagekit`
- **Observability:** Sentry + OpenTelemetry
- **Server:** Granian 2.5.0 (Production ASGI) + Whitenoise (Static File Serving)

---

### **4. Application Structure (Django Apps)**

A modular structure is mandated to ensure a clean separation of concerns.

- **`config/`**: The core Django project directory containing `settings/`, `urls.py`, and `asgi.py`. Settings are split into `base.py`, `dev.py`, and `production.py`.
- **`frontend`**: Manages all frontend assets. Its sole purpose is to house the Vite build process, source files (`src/`), and load compiled assets (/dist) into templates.
- **`templates/`**: Templates directory for all apps.
- **`apps/`**: A top-level directory containing all custom applications.
  - **`users`**: Manages the custom `User` model, profiles, authentication logic, and 2FA implementation.
  - **`core`**: Contains foundational, project-wide logic. This includes abstract base models (`BaseModel`, `SoftDeleteModel`), utility functions, custom template tags, asynchronous tasks, and context processors.
  - **`api`**: A dedicated app for defining all DRF serializers, viewsets, permissions, and API-specific routing (e.g., `/api/v1/`).

---

### **5. Authentication & Authorization**

Authentication is handled by **`django-allauth`** to provide a comprehensive and secure solution.

- **Core Functionality:** Manages user registration, login/logout, password reset, and email verification.
- **OpenID Connect (OIDC):** Pre-configured for OIDC-based single sign-on (SSO) using `allauth.socialaccount`, enabling seamless integration with identity providers like Authentik, Keycloak, or Okta.
- **Custom User Model:** The `users` app defines a custom `User` model (`settings.AUTH_USER_MODEL`) inheriting from `AbstractUser`. This is the single source of truth for user data.
- **API Authentication:** API endpoints will be secured using DRF's token-based authentication (e.g., `TokenAuthentication`) or JWT for stateless authentication.

---

### **6. Data & Content Model**

#### **6.1. Common Base Models**

All custom models will inherit from common abstract base models defined in the `core` app to ensure consistency.

- **`BaseModel` (Abstract):** Includes common, non-nullable fields for all models: `id` (UUID), `created_at`, and `updated_at`.
- **`SoftDeleteModel` (Abstract):** Inherits from `BaseModel`. It adds a `deleted_at` nullable timestamp and a custom manager that automatically excludes "deleted" records from all default querysets. This prevents accidental data loss.

#### **6.2. Search and Analytics (ParadeDB)**

- **BM25 Full-Text Search:** A custom `SearchManager` will be available in the `core` app. This manager uses raw SQL to execute ParadeDB's `paradedb.bm25()` function, bypassing the Django ORM for highly performant full-text search queries.
- **Analytics:** For high-volume data, analytics queries will leverage ParadeDB's columnar storage capabilities via optimized `GROUP BY` and aggregation raw SQL queries, wrapped in utility functions for easy reuse.

#### **6.3. File & Media Management**

A clear distinction is made between static and media files.

- **Static Files:** Application assets (CSS, JS, icons) served by **Whitenoise** in production or a CDN. Managed by Vite.
- **Media Files:** User-uploaded content (images, documents). Handled by **`django-storages`**, configured with an S3-compatible object storage backend (e.g., AWS S3, MinIO). This decouples file storage from the application server, enabling stateless and scalable deployments.
- **Image Processing:** **`django-imagekit`** processes uploaded images on-the-fly (or on-save). An `ImageSpecField` on a model defines variants (e.g., thumbnails) with specified processors (e.g., resize, crop).

---

### **7. Frontend Architecture**

#### **7.1. Template Structure**

Templates are designed with **Hotwire** to enable partial page updates, minimizing data transfer and improving perceived latency.

- **`templates/base.html`**: The main site template, loading compiled assets via `django-vite` tags and defining global blocks.
- **`<turbo-frame>`:** Used to define independent sections of a page that can be lazily loaded or updated without a full page refresh.
- **`<turbo-stream>`:** Used with WebSockets (`django-actioncable`) to deliver server-side updates that can prepend, append, or replace content anywhere on the page in real-time.

#### **7.2. Styling & Static Assets**

- **Configuration:** Styling is defined in `frontend/src/css/styles.css`, which imports Tailwind CSS. All frontend source files (JS, CSS, images) reside in `frontend/src/`.
- **Build Process:** **Vite** processes source files and outputs optimized, hashed assets to `/dist/`.
- **Asset Loading:** The `{% vite_hmr_client %}` and `{% vite_asset 'path/to/entry.js' %}` template tags automatically handle asset loading for both development (with Hot Module Replacement) and production environments.

---

### **8. Performance & Optimization**

- **Caching:** A layered caching strategy will be used:
  - **Low-Level Cache API:** `django.core.cache` with **Memcached** as the backend for caching expensive computations or database query results.
  - **Template Fragment Caching:** `{% cache %}` tag for caching expensive-to-render but frequently accessed UI components.
- **Database Queries:** Mandate the use of `select_related` and `prefetch_related` to prevent N+1 query problems. Use `django-debug-toolbar` in development to identify and optimize slow queries.
- **Asynchronous Tasks:** Offload long-running or non-critical tasks (e.g., sending emails, processing data imports) to **Celery** to keep web requests fast and responsive.

---

### **9. Deployment & Operations (DevOps)**

- **Containerization:** The entire application stack (web, database, broker, worker) is defined in a `docker-compose.yml` file for consistent, reproducible development and production environments.
- **Environment Configuration:** All sensitive data and environment-specific settings (e.g., `SECRET_KEY`, `DATABASE_URL`) are managed via environment variables using **`django-environ`**. No secrets are stored in version control.
- **CI/CD Pipeline:** A GitHub Actions pipeline will automate:
  1.  **Linting & Formatting:** Run `ruff` and `mypy`.
  2.  **Testing:** Run `pytest` against the test suite.
  3.  **Building:** Build frontend assets (`vite build`) and the final Docker image.
  4.  **Deployment:** Push the image to a container registry and deploy to the hosting environment.
- **Observability:**
  - **Error Tracking:** **Sentry** SDK is integrated to capture and report exceptions in real-time from Django and Celery.
  - **Performance Monitoring:** **OpenTelemetry** traces requests across the stack (Django, DRF, Celery, DB queries) and sends the data to Sentry for performance analysis and identifying bottlenecks.

---

### **NOTE:**

- **Modern Tooling:** This starter kit is built with modern, actively maintained, and stable tools. Outdated or unmaintained packages are strictly avoided.
- **High-Performance Server:** **Granian** is the recommended production server. Its Rust-based, async-native architecture provides exceptional speed and concurrency for modern ASGI Django applications, significantly outperforming legacy WSGI servers like Gunicorn.
