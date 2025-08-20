MAKEFLAG := -j 4

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

.PHONY: docker-build
docker-build:
	docker build -t django-starter-kit .

### DEV ###
.PHONY: dev
dev: django-dev

.PHONY: django-dev
django-dev:
	uv run granian --reload --interface asginl --workers 1 --runtime-threads 2 config.asgi:application




# deploy:
# 	# This target is for deployment, which is not part of the automated CI/CD pipeline.
# 	# Add your deployment commands here if you need to deploy manually.
# 	echo "Deployment is not automated in CI/CD. Please deploy manually if needed."