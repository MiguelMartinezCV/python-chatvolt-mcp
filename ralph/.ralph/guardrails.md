# Guardrails

Persistent rules learned from past iterations. The agent reads this every loop.

## General
- Run `uv run ruff format .` before committing to ensure consistent formatting
- Run `uv run pytest -v` to verify all tests pass before committing
- Never commit files containing secrets or API keys
- Keep imports sorted (ruff isort handles this)
- Every new tool/feature must have corresponding tests
- Tool names should be action-first (e.g., `create_agent`, `list_contacts`, not `agents_post_agents`)
- All tools should have proper `description` fields that explain when/how to use them
- Prompts must reference actual tool names, not hypothetical ones
- When adding new tool definition modules, update both `src/tools/definitions/__init__.py` and `src/tools/all_definitions.py`
