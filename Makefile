.PHONY: install-py install-js test

install-py:
	uv install

install-js:
	cd frontend && bun install

test:
	uv run pytest