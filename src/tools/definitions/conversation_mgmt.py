from typing import Any

TOOLS: dict[str, dict[str, Any]] = {
    "create_conversation": {
        "method": "POST",
        "path": "/conversation",
        "description": "Create a new conversation.",
        "input_schema": {
            "type": "object",
            "properties": {
                "agentId": {"type": "string", "description": "ID of the agent to associate with the conversation"},
                "contactId": {"type": "string", "description": "ID of the contact"},
                "channel": {
                    "type": "string",
                    "enum": ["whatsapp", "telegram", "zapi", "instagram", "web"],
                    "description": "Communication channel",
                },
                "status": {
                    "type": "string",
                    "enum": ["RESOLVED", "UNRESOLVED", "HUMAN_REQUESTED"],
                    "default": "UNRESOLVED",
                },
            },
        },
    },
    "resolve_conversation": {
        "method": "POST",
        "path": "/conversation/{conversationId}/resolve",
        "description": "Mark a conversation as resolved.",
        "input_schema": {
            "type": "object",
            "properties": {
                "conversationId": {"type": "string", "description": "ID of the conversation to resolve"},
            },
            "required": ["conversationId"],
        },
    },
    "delete_conversation": {
        "method": "DELETE",
        "path": "/conversation/{conversationId}",
        "description": "Delete a conversation. This action is irreversible.",
        "input_schema": {
            "type": "object",
            "properties": {
                "conversationId": {"type": "string", "description": "ID of the conversation to delete"},
            },
            "required": ["conversationId"],
        },
    },
    "request_human_intervention": {
        "method": "POST",
        "path": "/conversation/{conversationId}/request-human",
        "description": "Request human intervention for a conversation.",
        "input_schema": {
            "type": "object",
            "properties": {
                "conversationId": {"type": "string", "description": "ID of the conversation"},
                "reason": {"type": "string", "description": "Reason for requesting human intervention"},
            },
            "required": ["conversationId"],
        },
    },
}
