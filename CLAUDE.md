# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

This project uses PDM for dependency management and includes a Makefile with Python.mk.

```bash
# Install dependencies
pdm install

# Full build (install deps, lint, test, build package)
make build

# Linting (runs black, isort, flake8, and mypy via `make lint`)
make lint        # black, isort, flake8
make mypy        # type checking (included via `lint :: mypy` in Makefile)

# Testing
make test                    # run pytest with coverage (100% required)
make pytest_debug            # run tests with output capture disabled
PYTESTOPTS="-k test_name" make test  # run single test

# Individual lint tools
make black       # format code
make isort       # sort imports
make flake8      # style checks
```

## Architecture

Single-module Python package (`libgoogle/__init__.py`) providing Google API connectivity with XDG-compliant credential storage.

**Key functions:**
- `connect(scope, version)` - Main entry point. Connects to Google services (Calendar, Drive, Gmail, etc.). Handles OAuth flow, token refresh, and optional caching.
- `set_debug(flag)` - Enable/disable httplib2 debug logging
- `use_cache(flag)` - Enable/disable connection caching

**File locations (XDG):**
- Credentials: `$XDG_CONFIG_HOME/libgoogle/credentials.json`
- Tokens: `$XDG_CACHE_HOME/libgoogle/{scope}-token.json`

## Code Style

- Line length: 97 characters (black, isort, pylint)
- Type hints required (mypy strict mode)
- Docstrings: Google convention (pydocstyle)
