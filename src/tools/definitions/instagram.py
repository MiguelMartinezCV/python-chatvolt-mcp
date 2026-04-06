from typing import Any

TOOLS: dict[str, dict[str, Any]] = {
    "instagram_list_agents": {
        "method": "GET",
        "path": "/instagram/agents",
        "description": "List all agents connected to Instagram.",
        "input_schema": {
            "type": "object",
            "properties": {},
        },
    },
    "instagram_connect": {
        "method": "POST",
        "path": "/instagram/connect",
        "description": "Connect an Instagram Business Account to an agent.",
        "input_schema": {
            "type": "object",
            "properties": {
                "agentId": {"type": "string", "description": "ID of the agent to connect"},
                "instagramAccountId": {"type": "string", "description": "Instagram Business Account ID"},
                "accessToken": {"type": "string", "description": "Meta Platform API access token"},
                "directMessages": {
                    "type": "boolean",
                    "description": "Enable agent to respond to direct messages",
                    "default": True,
                },
                "comments": {
                    "type": "boolean",
                    "description": "Enable agent to respond to comments",
                    "default": False,
                },
            },
            "required": ["agentId", "instagramAccountId", "accessToken"],
        },
    },
    "instagram_disconnect": {
        "method": "POST",
        "path": "/instagram/disconnect",
        "description": "Disconnect an Instagram Business Account from an agent.",
        "input_schema": {
            "type": "object",
            "properties": {
                "agentId": {"type": "string", "description": "ID of the agent to disconnect"},
            },
            "required": ["agentId"],
        },
    },
}
