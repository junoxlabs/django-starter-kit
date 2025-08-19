MAKEFLAG := -j 4

.PHONY: install i install-py install-js test

install i: install-py install-js
	@echo "Installation complete. You can now run the project."

install-py:
	uv sync

install-js:
	cd frontend && bun --bun install

clean:
	rm -rf .venv frontend/node_modules

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