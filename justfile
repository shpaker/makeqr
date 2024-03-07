#!/usr/bin/env just --justfile

SOURCE_DIR := "makeqr"
TESTS_DIR := "tests"

lint: mypy ruff

mypy:
  poetry run python -m mypy --pretty --package {{ SOURCE_DIR }}

ruff:
  poetry run python -m ruff check --fix {{ SOURCE_DIR }}
  poetry run python -m ruff check --fix --unsafe-fixes {{ TESTS_DIR }}

format:
  poetry run python -m ruff format {{ SOURCE_DIR }} {{ TESTS_DIR }}

tests:
  poetry run pytest -vv {{ TESTS_DIR }}
