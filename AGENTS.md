# Agent Development Guidelines

This document outlines the best practices and conventions for developing agents in this project.

## File Structure

-   **Virtual Environment**: Should be located in `.venv`.
-   **Source Code**: All Python source code should reside in the `src/` directory.
-   **Tests**: All tests should be placed in the `tests/` directory.
-   **Documentation**: The project should have a `README.md` at the root.
-   **Project Configuration**: All tool configurations (e.g., `ruff`, `pytest`, `mypy`) and project metadata should be consolidated in `pyproject.toml`.

## Development Environment

-   **Virtual Environment and Package Management**: Use `uv` to create and manage the virtual environment and dependencies.
    -   Create a virtual environment: `uv venv`
    -   Activate the environment: `source .venv/bin/activate`
-   **Pre-commit Hooks**: Use `pre-commit` to automate checks before committing. A `.pre-commit-config.yaml` should be present in the repository to define the hooks.

## Dependency Management

-   **Project Dependencies**: Define project metadata and main dependencies in `pyproject.toml` under the `[project]` table.
-   **Development Dependencies**: Define dependencies for testing, linting, etc., in `pyproject.toml` under `[project.optional-dependencies]`.
-   **Installation**: For an editable install during development, use `uv pip install -e ".[dev,test]"`. This will install the project, its main dependencies, and the optional dependencies for development and testing.
-   **Locking Dependencies**: For reproducible environments (like CI or production), create `uv.lock` file by running `uv lock`.
-   **Syncing from Lock File**: To install the exact versions from the lock file, use `uv sync`.

## Linting & Formatting

-   **Tool**: Use `ruff` for both linting and code formatting. Its configuration should be in `pyproject.toml`.
-   **Usage**:
    -   Linting: `ruff check .`
    -   Formatting: `ruff format .`
-   This should be integrated into the `pre-commit` hooks.

## Type Checking

-   **Tool**: Use `mypy` for static type analysis. Its configuration should be in `pyproject.toml`.
-   **Usage**: Run `mypy src` to check for type errors.
-   This should also be part of the `pre-commit` hooks.

## Testing

-   **Framework**: Use `pytest` for tests. Its configuration should be in `pyproject.toml`.
-   **Coverage**: Use `pytest-cov` to measure test coverage.
    -   Run with `pytest --cov=src`.

## General Preferences

-   **Web Framework**: `FastAPI` is preferred for web applications backend. `HTMX` is preferred for web applications backend.
-   **Configuration**: Load application configuration from `.env` files using a library like `pydantic-settings`.
-   **Logging**: Use `loguru` for logging.