### **1. Introduction**

#### **1.1. Purpose**

This document outlines the system architecture for a universal, modern, and efficient Django 5.2 LTS Starter Kit. Its primary purpose is to serve as a robust and flexible foundation for building high-performance web applications, from API services to content-driven sites.

#### **1.2. Scope**

The architecture described herein covers the backend structure, data modeling, frontend integration, performance strategies, and deployment considerations. It is intended to guide the development team in building a reusable boilerplate that prioritizes developer experience (DX), application performance, and long-term maintainability.

#### **1.3. Core Principles**

The design is guided by the following core principles:

- **Modularity:** Application functionality will be constructed from independent, reusable Django apps.
- **Convention over Configuration:** A clear and logical project structure will be established to ensure consistency and reduce cognitive overhead.
- **Performance First:** The system will be architected for speed, incorporating caching, asset optimization, and efficient data retrieval by default.
- **Decoupled Services:** The architecture separates the application, data, and message brokering layers to enable independent scaling and improve resilience.
- **Streamlined Development (DX):** The starter kit will provide a clean, well-documented, and modern development environment to maximize productivity.

---

### **2. System Architecture Overview**

The system is a monolithic web application built on the Django framework. Its architecture can be visualized in three primary layers:

- **Presentation Layer (Frontend):** Responsible for rendering the user interface. This layer is powered by Django's templating engine, styled with a utility-first CSS framework, and enhanced with a lightweight JavaScript approach.
- **Application Layer (Backend):** Contains the core business logic. This is managed by Django views, serializers, and custom application logic. It handles user requests, data processing, and routing.
- **Data Layer:** Responsible for data persistence and caching. This includes a primary relational database (ParadeDB) for structured data and an in-memory cache (Memcached) for high-speed data access.

---

### **3. Technology Stack**

The following technologies will form the foundation of the starter kit. All dependencies are managed by **`uv`** via a single `pyproject.toml` file.

- **Backend Framework:** Django (5.2 LTS)
- **API Framework:** Django REST Framework
- **Database:** ParadeDB (PostgreSQL 17 extension)
- **Cache:** Memcached
- **Task Queue:** Celery + RabbitMQ
- **Python Tooling:** `uv` (package manager), `ruff`, `mypy`, `pytest`
- **Authentication:** django-allauth (for social auth and OIDC)
- **Frontend Bundler:** Vite (django-vite)
- **Frontend Styling:** Tailwind CSS v4 + Daisy UI 5
- **Interactivity:** Turbo 8 + Stimulus 3 + GSAP 3
- **Turbo + WebSockets:** @rails/actioncable@8 + django-actioncable
- **Email:** `django-anymail`
- **Media Processing:** `django-imagekit`
- **Observability:** Sentry + OpenTelemetry
- **Server:** Granian 2.5.0 (for production) + Whitenoise (for static files)

---

### **4. Application Structure (Django Apps)**

A modular application structure is mandated to ensure separation of concerns.

- **`config/`**: The core Django project directory containing `settings`, `urls.py`, and `asgi.py`.
- **`apps/`**: A top-level directory to contain all custom applications.
  - **`users`**: Manages the custom `User` model, authentication logic, and 2FA implementation.
  - **`core`**: Contains foundational, project-wide logic. This includes abstract base models, utility functions, asynchronous tasks, and context processors.
  - **`frontend`**: Manages all frontend assets. Its sole purpose is to house the Vite build process, source files for Tailwind CSS and Stimulus, and load compiled assets.
  - **`api`**: A dedicated app for defining all DRF serializers, viewsets, and API-specific routing.

---

### **5. Authentication**

Authentication is handled centrally by django-allauth to provide a comprehensive and secure solution out of the box.

- **Core Functionality:** django-allauth will manage user registration, login/logout, password reset, and email verification.
- **OpenID Connect (OIDC):** The system will be pre-configured for OIDC-based single sign-on (SSO). The allauth.socialaccount provider for OIDC will be used to connect to identity providers like Authentik. This enables seamless integration with centralized identity management systems.
- **Custom User Model:** The users app will define a custom User model that inherits from Django's AbstractUser. This model is designated in settings.AUTH_USER_MODEL and is the single source of truth for user data.
- **Social Authentication:** Additional OAuth2 providers (e.g., Google, GitHub) can be easily enabled through django-allauth's configuration as needed.

---

### **6. Data and Content Model**

This section defines the structure of core data within the system.

#### **6.1. Common Base Models**

All custom models will inherit from a common base to ensure consistency and pre-configured behavior.

- **`BaseModel` (Abstract Model):** Defined in the `core` app. It will not be creatable on its own. It will include common fields essential for all models, such as `created_at` and `updated_at` timestamps.

#### **6.2. Search and Analytics**

The system leverages ParadeDB's powerful capabilities directly.

- **BM25 Search:** A custom `SearchManager` class can be attached to models to provide a consistent API for full-text search. The manager will use raw SQL queries to execute ParadeDB's BM25 search function, bypassing the standard Django ORM lookups for superior performance.
- **Analytics:** For data models with high-volume write operations, developers can use a dedicated utility function to execute `GROUP BY` and aggregation queries that are optimized by ParadeDB's columnar storage.

#### **6.3. Media Processing**

`django-imagekit` is used to handle image processing. On a model, an `ImageSpecField` defines an image variant (e.g., a thumbnail). This field's `processors` attribute specifies the actions (e.g., resizing, cropping) to be taken.

---

### **7. Frontend Architecture**

#### **7.1. Template Structure**

A standardized template hierarchy is used. Templates will be designed with Hotwire in mind, using <turbo-frame> and <turbo-stream> elements to define sections for partial page updates.

- **`templates/base.html`**: The main site template. Contains the `<html>`, `<head>`, and `<body>` tags, loads the compiled CSS and JS, and defines global block areas.
- **`templates/includes/`**: Contains reusable template fragments like the site header, footer, and navigation.
- **`apps/frontend/templates/frontend/base.html`**: A base template specific to the frontend app, inheriting from the global `base.html`.

#### **7.2. Styling & Static Assets**

- **Configuration:** The core styling is defined in `apps/frontend/assets/css/styles.css`. This file uses the `@import "tailwindcss"` and `@source` directives to configure Tailwind and manage class purging. No separate JavaScript configuration file is required.
- **Build Process:** Vite is the bundler. It processes source files in `apps/frontend/assets/` and outputs optimized, hashed assets to `apps/frontend/static/dist/`.
- **Asset Loading:** The compiled assets are loaded in Django templates using the `{% vite_hmr_client %}` and `{% vite_asset %}` template tags provided by `django-vite`. These tags handle the logic for development vs. production environments automatically.

---

### **8. Performance & Optimization Strategy**

- **Caching:**
  - Implement a production cache backend with Memcached.
  - Use Django's template fragment caching for expensive-to-render but frequently accessed components.
- **Partial Page Loads:** Leverage Hotwire Turbo extensively to prevent full-page reloads. Turbo Drive intercepts navigation and form submissions, fetching new content and replacing only the <body> or designated <turbo-frame>s, dramatically improving perceived performance.
- **Database Queries:** Mandate the use of `select_related` and `prefetch_related` in querysets to prevent N+1 query problems.
- **Image Optimization:** Use `django-imagekit`'s `{% image %}` template tag for all images. This enables on-the-fly resizing and cropping, ensuring appropriately sized images are served.
- **Asset Minification:** The Vite build process automatically minifies the final CSS and JavaScript output for production.

---

### **9. Deployment & Operations**

- **Environment Configuration:** All sensitive information is managed via environment variables.
- **Static Files:** A production-grade static file serving strategy is required, such as using Whitenoise or a Content Delivery Network (CDN).
- **CI/CD Pipeline:** A continuous integration and deployment pipeline is configured using GitHub Actions. This pipeline will automate linting, testing, frontend asset building, and Docker image creation.
- **Logging & Monitoring:** Configure structured logging and integrate Sentry for error tracking and OpenTelemetry for performance monitoring and tracing. The OpenTelemetry SDK collects data from Django, Celery, and other components and forwards it to Sentry for analysis.
- **Containerization:** Docker support is a first-class citizen for consistent development and deployment environments.

---

### **NOTE:**

- **Core Principles:** This starter kit is built using modern, actively maintained, and stable tools. Outdated or unmaintained packages are avoided to ensure long-term stability and security.
- **Application Server:** The recommended application server is **Granian 2.5.0**. It is a high-performance, async-native ASGI server that is significantly faster than Gunicorn for modern Django applications. Granian's architecture is built on Rust, providing exceptional speed and concurrency for handling I/O-bound tasks.
- **Configuration:** All sensitive data (e.g., API keys, passwords) must be stored in environment variables, not hardcoded in the settings files.
