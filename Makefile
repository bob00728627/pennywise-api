.PHONY: install dev test lint format

install:
	pip install -r requirements-dev.txt

dev:
	uvicorn app.main:app --reload --port 8000

test:
	pytest

lint:
	ruff check .

format:
	ruff format .
