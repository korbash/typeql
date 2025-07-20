.PHONY: format lint typecheck check help

# Default target
help:
	@echo "Available commands:"
	@echo "  format     - Format code with ruff"
	@echo "  lint       - Lint code with ruff"
	@echo "  typecheck  - Run type checking with basedpyright"
	@echo "  check      - Run all checks (lint + typecheck)"

format:
	uv run ruff format

lint:
	uv run ruff check

typecheck:
	uv run basedpyright

check: lint typecheck
