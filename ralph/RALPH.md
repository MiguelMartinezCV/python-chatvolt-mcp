---
agent: opencode run --print
commands:
  - name: tests
    run: uv run pytest -v --tb=short 2>&1
    timeout: 120
  - name: lint
    run: uv run ruff check . 2>&1
    timeout: 60
  - name: format
    run: uv run ruff format --check . 2>&1
    timeout: 60
  - name: git-log
    run: git log --oneline -5 2>&1
    timeout: 30
args: {}
credit: false
---

# Chatvolt MCP - Development Loop

You are working on a Python MCP (Model Context Protocol) server for Chatvolt AI.

## Project Structure

This is a Python 3.13 project using `uv` for dependency management. The server runs on Starlette with SSE transport at `/sse`.

Key files:
- `src/server.py` - Main MCP server with tool/prompt handlers
- `src/tools/loader.py` - Tool registry that maps OpenAPI specs to MCP tools
- `src/tools/definitions/` - Individual tool definition modules (agents, crm, conversations, artifacts, datastores)
- `src/prompts/workflows.py` - Pre-defined workflow prompts
- `src/config.py` - Environment configuration
- `tests/` - pytest test suite

## Current State

### Git Log
{{ commands.git-log }}

### Test Results
{{ commands.tests }}

### Lint Results
{{ commands.lint }}

### Format Check
{{ commands.format }}

## Instructions

1. **If tests are failing, fix them first.** Read the test output, understand the failure, and make targeted fixes.
2. **If lint has errors, fix them next.** Run `uv run ruff check --fix .` to auto-fix what's possible, then manually fix the rest.
3. **If formatting is off, fix it.** Run `uv run ruff format .` to auto-format.
4. **After fixes, commit your changes** with a clear, conventional commit message (e.g., `fix: resolve test failure in loader.py`, `style: format imports with ruff`).
5. **Do not modify test files** unless explicitly instructed in TODO.md. The tests define the expected behavior.

## Guardrails

<!-- Read guardrails.md for persistent rules learned from past iterations -->
{{ ralph.guardrails }}

## TODO

<!-- Check TODO.md for current tasks to work on -->
