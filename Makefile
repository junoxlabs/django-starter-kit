.PHONY: install-py install-js test

install-py:
	uv install

install-js:
	cd frontend && bun install

lint:
	uv run ruff check .
	uv run mypy .

test:
	uv run pytest

docker-build:
	docker build -t django-starter-kit .

# deploy:
# 	# This target is for deployment, which is not part of the automated CI/CD pipeline.
# 	# Add your deployment commands here if you need to deploy manually.
# 	echo "Deployment is not automated in CI/CD. Please deploy manually if needed."