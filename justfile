#!/usr/bin/env just --justfile
SOURCE_DIR := "makeqr"
TESTS_DIR := "tests"

lint: ruff mypy

mypy:
  python -m mypy --pretty --package {{ SOURCE_DIR }}

ruff:
  python -m ruff check --fix {{ SOURCE_DIR }}
  python -m ruff check --fix --unsafe-fixes {{ TESTS_DIR }}

format:
  python -m ruff format {{ SOURCE_DIR }} {{ TESTS_DIR }}

