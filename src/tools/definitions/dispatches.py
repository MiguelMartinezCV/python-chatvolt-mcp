from typing import Any

TOOLS: dict[str, dict[str, Any]] = {
    "list_dispatches": {
        "method": "GET",
        "path": "/dispatches",
        "description": "List all dispatches (broadcast campaigns), optionally filtered by status or date.",
        "input_schema": {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "enum": ["pending", "sending", "completed", "failed"],
                    "description": "Filter by dispatch status",
                },
                "createdAt": {"type": "string", "description": "Filter by creation date (e.g., 'YYYY-MM-DD HH:mm:ss')"},
                "limit": {"type": "integer", "description": "Maximum number of dispatches to return"},
                "offset": {"type": "integer", "description": "Number of dispatches to skip for pagination"},
            },
        },
    },
    "get_dispatch": {
        "method": "GET",
        "path": "/dispatches/{id}",
        "description": "Retrieve details of a specific dispatch by ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID of the dispatch"},
            },
            "required": ["id"],
        },
    },
    "create_dispatch": {
        "method": "POST",
        "path": "/dispatches",
        "description": "Create a new dispatch (broadcast campaign) to send messages to a list of contacts.",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Name of the dispatch campaign"},
                "agentId": {"type": "string", "description": "ID of the agent to use for sending"},
                "contactIds": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of contact IDs to send to",
                },
                "message": {
                    "type": "string",
                    "description": "Message template to send. Can include variables like {{firstName}}",
                },
                "scheduledAt": {
                    "type": "string",
                    "description": "Optional scheduled time (e.g., 'YYYY-MM-DD HH:mm:ss')",
                },
                "channel": {
                    "type": "string",
                    "enum": ["whatsapp", "telegram", "zapi", "instagram"],
                    "description": "Channel to send through",
                },
                "tags": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Filter contacts by tags instead of explicit contactIds",
                },
            },
            "required": ["name", "agentId", "message"],
        },
    },
    "update_dispatch": {
        "method": "PATCH",
        "path": "/dispatches/{id}",
        "description": "Update an existing dispatch configuration.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID of the dispatch to update"},
                "name": {"type": "string"},
                "agentId": {"type": "string"},
                "contactIds": {"type": "array", "items": {"type": "string"}},
                "message": {"type": "string"},
                "scheduledAt": {"type": "string"},
                "channel": {"type": "string", "enum": ["whatsapp", "telegram", "zapi", "instagram"]},
            },
            "required": ["id"],
        },
    },
    "delete_dispatch": {
        "method": "DELETE",
        "path": "/dispatches/{id}",
        "description": "Delete a dispatch. Only pending dispatches can be deleted.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID of the dispatch to delete"},
            },
            "required": ["id"],
        },
    },
}
