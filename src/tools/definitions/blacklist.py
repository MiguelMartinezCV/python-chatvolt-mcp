from typing import Any

TOOLS: dict[str, dict[str, Any]] = {
    "list_blacklist": {
        "method": "GET",
        "path": "/agents/{agentId}/blacklist",
        "description": "List all blacklisted users for a specific agent.",
        "input_schema": {
            "type": "object",
            "properties": {
                "agentId": {"type": "string", "description": "ID of the agent"},
                "limit": {"type": "integer", "description": "Maximum number of entries to return"},
                "offset": {"type": "integer", "description": "Number of entries to skip for pagination"},
            },
            "required": ["agentId"],
        },
    },
    "add_to_blacklist": {
        "method": "POST",
        "path": "/agents/{agentId}/blacklist",
        "description": "Add a user to the agent's blacklist. Blacklisted users will not be able to interact with the agent.",
        "input_schema": {
            "type": "object",
            "properties": {
                "agentId": {"type": "string", "description": "ID of the agent"},
                "userId": {"type": "string", "description": "ID of the user/visitor to blacklist"},
                "phoneNumber": {"type": "string", "description": "Phone number to blacklist"},
                "reason": {"type": "string", "description": "Reason for blacklisting"},
            },
            "required": ["agentId"],
        },
    },
    "remove_from_blacklist": {
        "method": "DELETE",
        "path": "/agents/{agentId}/blacklist/{blacklistId}",
        "description": "Remove a user from the agent's blacklist.",
        "input_schema": {
            "type": "object",
            "properties": {
                "agentId": {"type": "string", "description": "ID of the agent"},
                "blacklistId": {"type": "string", "description": "ID of the blacklist entry to remove"},
            },
            "required": ["agentId", "blacklistId"],
        },
    },
}
