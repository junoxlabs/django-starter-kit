MAKEFLAGS += -j4

.PHONY: install i 
install i: deps-django deps-frontend
	@echo "Installation complete. You can now run the project."

.PHONY: deps-django
deps-django:
	uv sync

.PHONY: deps-frontend
deps-frontend:
	cd frontend && bun --bun install

.PHONY: clean
clean:
	rm -rf .venv frontend/node_modules

.PHONY: lint
lint:
	uv run ruff check .

.PHONY: lint-fix
lint-fix:
	uv run ruff check . --fix

.PHONY: format
format:
	uv run ruff format .

.PHONY: test
test:
	uv run pytest


#### DOCKER DEV #### -----------------------------------------------------------------------------
.PHONY: dev-up
dev-up:
	docker compose -f dev/docker-compose.dev.yml up --build -d

.PHONY: dev-down dev-stop
dev-down dev-stop stop:
	docker compose -f dev/docker-compose.dev.yml down

.PHONY: dev-clean
dev-clean:
	docker compose -f dev/docker-compose.dev.yml down -v

.PHONY: dev-restart
dev-restart:
	make dev-down
	make dev-up

.PHONY: dev-logs
dev-logs logs:
	docker compose -f dev/docker-compose.dev.yml logs -f

.PHONY: dev-ps
dev-ps ps:
	docker compose -f dev/docker-compose.dev.yml ps

.PHONY: dev-shell
dev-shell shell:
	docker compose -f dev/docker-compose.dev.yml exec app bash

## - END DOCKER DEV - ## -------------------------------------------------------------------------

#### - LOCAL DEV - #### ---------------------------------------------------------------------------
.PHONY: dev
dev: django-dev vite-dev

.PHONY: django-dev
django-dev:
	uv run granian --reload \
		--interface asgi \
		--workers 2 \
		--runtime-mode mt \
		--loop uvloop \
		--log-level debug \
		--host 0.0.0.0 \
		--port 8000 \
		config.asgi:application

.PHONY: vite-dev
vite-dev:
	cd frontend && bun --bun run dev --host 0.0.0.0 --port 5173
## - END LOCAL DEV - ## ---------------------------------------------------------------------------

#### - BUILD - #### ------------------------------------------------------------------------------
.PHONY: vite-build
vite-build:
	cd frontend && bun --bun run build

.PHONY: docker-build
docker-build:
	docker build -t django-starter-kit .
## - END BUILD - ## -------------------------------------------------------------------------------

### - PROD - ### ---------------------------------------------------------------------------------
.PHONY: collectstatic
collectstatic:
	uv run python manage.py collectstatic --no-input --clear

.PHONY: prod-start
prod-start:
	env ENVIRONMENT=production uv run granian \
		--interface asginl \
		--workers 3 \
		--runtime-mode mt \
	--loop uvloop \
		--host 0.0.0.0 \
		--port 8000 \
		config.asgi:application 

## - END PROD - ## -------------------------------------------------------------------------------

# deploy:
# 	# This target is for deployment, which is not part of the automated CI/CD pipeline.
# 	# Add your deployment commands here if you need to deploy manually.
# 	echo "Deployment is not automated in CI/CD. Please deploy manually if needed."
