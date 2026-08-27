#!/usr/bin/env just --justfile

SOURCE_DIR := "makeqr"
TESTS_DIR := "tests"

# List available recipes
default:
  @just --list

# Install the project and dev dependencies
sync:
  uv sync

# Install git hooks (requires: uv tool install prek)
hooks:
  prek install

# Run every check: lint, formatting, types
lint: ruff fmt-check types

ruff:
  uv run ruff check {{ SOURCE_DIR }} {{ TESTS_DIR }}

fmt-check:
  uv run ruff format --check {{ SOURCE_DIR }} {{ TESTS_DIR }}

types:
  uv run ty check

# Auto-fix what can be auto-fixed, then format
fix:
  uv run ruff check --fix {{ SOURCE_DIR }} {{ TESTS_DIR }}
  uv run ruff format {{ SOURCE_DIR }} {{ TESTS_DIR }}

# Format sources
format:
  uv run ruff format {{ SOURCE_DIR }} {{ TESTS_DIR }}

# Run the test suite
test:
  uv run pytest -vv {{ TESTS_DIR }}
