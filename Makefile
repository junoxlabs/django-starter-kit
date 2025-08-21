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


#### - DEV - #### --------------------------------------------------------------------------------
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
		config.asgi:application

.PHONY: vite-dev
vite-dev:
	cd frontend && bun --bun run dev
## - END DEV - ## --------------------------------------------------------------------------------

#### - build - #### ------------------------------------------------------------------------------
.PHONY: vite-build
vite-build:
	cd frontend && bun --bun run build

.PHONY: docker-build
docker-build:
	docker build -t django-starter-kit .
## - END build - ## ------------------------------------------------------------------------------

### - PROD - ### ---------------------------------------------------------------------------------
.PHONY: collectstatic
collectstatic:
	uv run python manage.py collectstatic --no-input --clear

.PHONY: start
start:
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
