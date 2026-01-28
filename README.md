# Chatvolt MCP Server

An MCP (Model Context Protocol) server for Chatvolt AI, providing tools and workflow prompts for managing agents, contacts, conversations, and more.

## Features
- **SSE Transport**: Runs over HTTP using Server-Sent Events.
- **Dynamic Tool Discovery**: Automatically maps Chatvolt OpenAPI specifications to MCP tools.
- **Workflow Prompts**: Pre-defined guided workflows for common tasks like onboarding and agent creation.
- **Python-based**: Built with Python and `uv`.

## Installation

1. **Install uv**:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clone and Initialize**:
   ```bash
   cd chatvolt-mcp
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv sync
   ```

3. **Configure Environment**:
   ```bash
   cp .env.example .env
   # Edit .env and add your CHATVOLT_API_KEY
   ```

## Running the Server

```bash
uv run python run.py
```
The server will start at `http://localhost:8000/sse`.

## Usage with MCP Clients

Point your MCP client (e.g., Claude Desktop or MCP Inspector) to the SSE endpoint:
- **URL**: `http://localhost:8000/sse`

### Available Tools
Tools are prefixed by their service name (e.g., `contacts_get_contacts`, `agents_post_agents`). All parameters from the OpenAPI specs are mapped to JSON schemas.

### Available Prompts
- `onboard_new_user`: Guide to creating a contact and sending a welcome message.
- `support_ticket_workflow`: Retrieve conversation history and create a CRM entry.
- `broadcast_campaign`: Setup a dispatch for a list of contacts.
- `create_new_agent`: Interactive workflow to design and deploy a new AI agent.
