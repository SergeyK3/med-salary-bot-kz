# Development Container Configuration

This directory contains the development container configuration for the Medical Salary Bot KZ project.

## What's Configured

The devcontainer provides:

- **Base Image**: `mcr.microsoft.com/devcontainers/python:3.12`
- **Auto-setup**: Dependencies are automatically installed via `pip install --user -r requirements.txt`
- **VS Code Extensions**: 
  - Python extension pack (Python, Pylint, Black formatter, isort)
  - Jupyter support
  - YAML support
  - Ruff linter

## Port Forwarding

- Port 8000 is automatically forwarded for the FastAPI application
- You can start the API server with: `python -m src.api`

## VS Code Settings

The configuration includes Python-specific settings:
- Python interpreter path set to `/usr/local/bin/python`
- Test discovery configured for pytest
- Code analysis enabled
- Python cache files excluded from file explorer

## Getting Started

1. Open this repository in GitHub Codespaces or VS Code with Dev Containers extension
2. The container will build automatically
3. Dependencies will be installed via the postCreateCommand
4. You can immediately run tests with `pytest` or start the API with `python -m src.api`

## Troubleshooting

If you encounter issues:
- Ensure Docker is running (for local development)
- Check that the requirements.txt file is present in the project root
- Verify Python 3.12 compatibility of all dependencies