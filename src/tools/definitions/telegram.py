from typing import Any

TOOLS: dict[str, dict[str, Any]] = {
    "telegram_list_agents": {
        "method": "GET",
        "path": "/telegram/agents",
        "description": "List all agents connected to Telegram.",
        "input_schema": {
            "type": "object",
            "properties": {},
        },
    },
    "telegram_connect": {
        "method": "POST",
        "path": "/telegram/connect",
        "description": "Connect a Telegram bot to an agent using the bot token from @BotFather.",
        "input_schema": {
            "type": "object",
            "properties": {
                "agentId": {"type": "string", "description": "ID of the agent to connect"},
                "botToken": {"type": "string", "description": "Telegram bot token from @BotFather"},
            },
            "required": ["agentId", "botToken"],
        },
    },
    "telegram_disconnect": {
        "method": "POST",
        "path": "/telegram/disconnect",
        "description": "Disconnect a Telegram bot from an agent.",
        "input_schema": {
            "type": "object",
            "properties": {
                "agentId": {"type": "string", "description": "ID of the agent to disconnect"},
            },
            "required": ["agentId"],
        },
    },
}
