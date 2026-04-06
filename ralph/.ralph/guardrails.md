# Guardrails

Persistent rules learned from past iterations. The agent reads this every loop.

## General
- Run `uv run ruff format .` before committing to ensure consistent formatting
- Run `uv run pytest -v` to verify all tests pass before committing
- Never commit files containing secrets or API keys
- Keep imports sorted (ruff isort handles this)
