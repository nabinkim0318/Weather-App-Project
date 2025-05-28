.PHONY: install lock format check test test-all run lint migrate pipeline

install:
	poetry install

lock:
	poetry lock && poetry install

format:
	poetry run black . && poetry run isort .

check:
	poetry check && poetry run black --check . && poetry run isort --check-only .

lint:
	poetry run flake8 app

test:
	PYTHONPATH=. poetry run pytest tests/ --disable-warnings

run:
	poetry run uvicorn app.main:app --reload

migrate:
	poetry run alembic upgrade head

pipeline: format lint check test
