# Instagram MCP Server - Claude Guidelines

## Project Overview
Enterprise-grade Python MCP server for Instagram Direct Message handling using instagrapi.

## Dependency Management
- NEVER manually edit pyproject.toml for dependencies
- ALWAYS use `uv add <package>` to add dependencies
- ALWAYS use `uv add --dev <package>` for dev dependencies
- Use `uv remove <package>` to remove dependencies
- Use `uv sync` to install dependencies from lockfile

## MCP Server Best Practices
- Never use `print()` - it corrupts JSON-RPC on stdio transport
- Use `logging` module with stderr handler instead
- All tools must have proper docstrings (they become MCP tool descriptions)
- Handle errors gracefully - return error messages, don't crash
- Use FastMCP decorator pattern for tool registration

## Code Quality
- Run `uv run ruff check .` before committing
- Run `uv run ruff format .` to format code
- Run `uv run mypy src/` with strict mode
- Maintain 100% test coverage
- Use type hints for all functions and methods
- Use Google-style docstrings for all public modules, classes, and functions

## Testing
- Unit tests go in `tests/unit/`
- Integration tests go in `tests/integration/`
- Use fixtures from `tests/conftest.py`
- Mock external APIs (Instagram) in unit tests
- Run tests: `uv run pytest tests/ -v --cov=src --cov-report=term-missing`

## Instagram API (instagrapi)
- Always cache sessions to avoid rate limiting
- Never log credentials or session data
- Handle 2FA gracefully
- Respect Instagram's rate limits
- Session file location: configured via INSTAGRAM_SESSION_FILE env var

## Project Structure
```
src/instagram_mcp/
├── __init__.py
├── server.py           # MCP server entry point
├── client.py           # Instagram client wrapper
├── config.py           # Configuration management
├── tools/
│   ├── __init__.py
│   ├── threads.py      # Thread management tools
│   ├── messages.py     # Message operations
│   └── media.py        # Media messaging
└── models/
    ├── __init__.py
    └── schemas.py      # Pydantic models
```

## Environment Variables
```
INSTAGRAM_USERNAME=     # Required
INSTAGRAM_PASSWORD=     # Required
INSTAGRAM_2FA_CODE=     # Optional, for 2FA
INSTAGRAM_SESSION_FILE= # Optional, defaults to .instagram_session
```

## Running the Server
```bash
uv run python -m instagram_mcp.server
```

## Common Commands
```bash
# Add dependency
uv add <package>

# Add dev dependency
uv add --dev <package>

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src --cov-report=term-missing

# Lint
uv run ruff check .

# Format
uv run ruff format .

# Type check
uv run mypy src/

# Run MCP server
uv run python -m instagram_mcp.server
```
