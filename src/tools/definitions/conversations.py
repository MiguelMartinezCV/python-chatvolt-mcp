from typing import Any

TOOLS: dict[str, dict[str, Any]] = {
    "get_conversation_messages": {
        "method": "GET",
        "path": "/conversation/{conversationId}/messages/{count}",
        "description": "Retrieves the last ‘N’ messages from a conversation.",
        "input_schema": {
            "type": "object",
            "properties": {
                "conversationId": {"type": "string", "description": "ID of the conversation"},
                "count": {"type": "integer", "default": 2, "description": "Number of most recent messages to retrieve"},
            },
            "required": ["conversationId", "count"],
        },
    },
    "get_message": {
        "method": "GET",
        "path": "/messages/{messageId}",
        "description": "Retrieve details of a single message by its ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "messageId": {"type": "string", "description": "The unique ID of the message"},
                "includeSources": {
                    "type": "boolean",
                    "default": False,
                    "description": "Include document sources in the response",
                },
            },
            "required": ["messageId"],
        },
    },
    "list_conversations": {
        "method": "GET",
        "path": "/conversation",
        "description": "Search for conversations by agent ID, creation date, and status. Supports pagination with cursor and limit.",
        "input_schema": {
            "type": "object",
            "properties": {
                "agentId": {
                    "type": "string",
                    "description": "Filter by agent ID. Pass 'null' for unassigned conversations.",
                },
                "createdAt": {"type": "string", "description": "Filter by creation date (e.g., 'YYYY-MM-DD HH:mm:ss')"},
                "status": {
                    "type": "string",
                    "enum": ["RESOLVED", "UNRESOLVED", "HUMAN_REQUESTED"],
                    "description": "Filter by status",
                },
                "cursor": {"type": "string", "description": "Pagination cursor for fetching next page of results"},
                "limit": {"type": "integer", "default": 50, "description": "Number of results to return (max 100)"},
            },
        },
    },
    "get_conversation": {
        "method": "GET",
        "path": "/conversation/{conversationId}",
        "description": "Retrieve details of a specific conversation by its ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "conversationId": {"type": "string", "description": "ID of the conversation to be retrieved"}
            },
            "required": ["conversationId"],
        },
    },
    "set_conversation_ai": {
        "method": "POST",
        "path": "/conversations/{conversationId}/set-ai-enabled",
        "description": "Enable or disable AI for a specific conversation.",
        "input_schema": {
            "type": "object",
            "properties": {
                "conversationId": {"type": "string", "description": "ID of the conversation"},
                "enabled": {"type": "boolean", "description": "True to enable AI, false to disable"},
            },
            "required": ["conversationId", "enabled"],
        },
    },
    "register_message_in_context": {
        "method": "POST",
        "path": "/conversations/{conversationId}/message-register",
        "description": "Register a message in the context of a conversation without sending it to the participant.",
        "input_schema": {
            "type": "object",
            "properties": {
                "conversationId": {"type": "string", "description": "ID of the conversation"},
                "message": {"type": "string", "description": "The text of the message to register"},
                "from": {
                    "type": "string",
                    "enum": ["human", "agent"],
                    "default": "human",
                    "description": "Who the message is from",
                },
            },
            "required": ["conversationId", "message"],
        },
    },
    "send_message_by_channel": {
        "method": "POST",
        "path": "/conversation/message/{type}/{value}",
        "description": "Send a message to a conversation identified by conversationId, phone, or email.",
        "input_schema": {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "enum": ["conversationId", "phone", "email"],
                    "description": "Type of conversation identifier",
                },
                "value": {"type": "string", "description": "Value for the identifier type"},
                "message": {"type": "string", "description": "Content of the message to send"},
                "agentId": {"type": "string", "description": "Optional agent ID"},
                "channel": {
                    "type": "string",
                    "enum": ["website", "dashboard", "whatsapp", "zapi", "telegram", "instagramDm"],
                    "description": "Optional channel for sending",
                },
                "attachments": {
                    "type": "array",
                    "items": {"type": "object"},
                    "description": "Optional list of attachments",
                },
                "visitorId": {"type": "string", "description": "Optional visitor ID"},
                "contactId": {"type": "string", "description": "Optional contact ID"},
            },
            "required": ["type", "value", "message"],
        },
    },
    "assign_conversation": {
        "method": "POST",
        "path": "/conversation/{conversationId}/assign",
        "description": "Assign a conversation to a user.",
        "input_schema": {
            "type": "object",
            "properties": {
                "conversationId": {"type": "string", "description": "ID of the conversation"},
                "userId": {"type": "string", "description": "ID of the user to assign the conversation to"},
            },
            "required": ["conversationId", "userId"],
        },
    },
    "set_conversation_priority": {
        "method": "POST",
        "path": "/conversation/{conversationId}/set-priority",
        "description": "Set the priority of a conversation.",
        "input_schema": {
            "type": "object",
            "properties": {
                "conversationId": {"type": "string", "description": "ID of the conversation"},
                "priority": {
                    "type": "string",
                    "enum": ["LOW", "MEDIUM", "HIGH", "URGENT"],
                    "description": "Priority level to set",
                },
            },
            "required": ["conversationId", "priority"],
        },
    },
    "update_conversation_status": {
        "method": "POST",
        "path": "/conversation/{conversationId}/update-status",
        "description": "Update the status of a conversation.",
        "input_schema": {
            "type": "object",
            "properties": {
                "conversationId": {"type": "string", "description": "ID of the conversation"},
                "status": {
                    "type": "string",
                    "enum": ["RESOLVED", "UNRESOLVED", "HUMAN_REQUESTED"],
                    "description": "New status for the conversation",
                },
            },
            "required": ["conversationId", "status"],
        },
    },
    "get_conversation_variables": {
        "method": "GET",
        "path": "/conversation/{conversationId}/variables",
        "description": "Get all custom variables for a conversation.",
        "input_schema": {
            "type": "object",
            "properties": {
                "conversationId": {"type": "string", "description": "ID of the conversation"},
            },
            "required": ["conversationId"],
        },
    },
    "get_conversation_variable": {
        "method": "GET",
        "path": "/conversation/{conversationId}/variables/{variableId}",
        "description": "Get a specific custom variable for a conversation.",
        "input_schema": {
            "type": "object",
            "properties": {
                "conversationId": {"type": "string", "description": "ID of the conversation"},
                "variableId": {"type": "string", "description": "ID of the variable"},
            },
            "required": ["conversationId", "variableId"],
        },
    },
    "upsert_conversation_variable": {
        "method": "POST",
        "path": "/conversation/{conversationId}/variables",
        "description": "Create or update a custom variable for a conversation.",
        "input_schema": {
            "type": "object",
            "properties": {
                "conversationId": {"type": "string", "description": "ID of the conversation"},
                "key": {"type": "string", "description": "Variable key/name"},
                "value": {"type": "string", "description": "Variable value"},
            },
            "required": ["conversationId", "key", "value"],
        },
    },
    "delete_conversation_variable": {
        "method": "DELETE",
        "path": "/conversation/{conversationId}/variables/{variableId}",
        "description": "Delete a custom variable from a conversation.",
        "input_schema": {
            "type": "object",
            "properties": {
                "conversationId": {"type": "string", "description": "ID of the conversation"},
                "variableId": {"type": "string", "description": "ID of the variable to delete"},
            },
            "required": ["conversationId", "variableId"],
        },
    },
    "get_conversation_notes": {
        "method": "GET",
        "path": "/conversation/{conversationId}/notes",
        "description": "Get all notes for a conversation.",
        "input_schema": {
            "type": "object",
            "properties": {
                "conversationId": {"type": "string", "description": "ID of the conversation"},
            },
            "required": ["conversationId"],
        },
    },
    "create_conversation_note": {
        "method": "POST",
        "path": "/conversation/{conversationId}/notes",
        "description": "Create a note for a conversation.",
        "input_schema": {
            "type": "object",
            "properties": {
                "conversationId": {"type": "string", "description": "ID of the conversation"},
                "content": {"type": "string", "description": "Note content"},
            },
            "required": ["conversationId", "content"],
        },
    },
    "update_conversation_note": {
        "method": "PUT",
        "path": "/conversation/{conversationId}/notes/{noteId}",
        "description": "Update a note for a conversation.",
        "input_schema": {
            "type": "object",
            "properties": {
                "conversationId": {"type": "string", "description": "ID of the conversation"},
                "noteId": {"type": "string", "description": "ID of the note to update"},
                "content": {"type": "string", "description": "New note content"},
            },
            "required": ["conversationId", "noteId", "content"],
        },
    },
    "delete_conversation_note": {
        "method": "DELETE",
        "path": "/conversation/{conversationId}/notes/{noteId}",
        "description": "Delete a note from a conversation.",
        "input_schema": {
            "type": "object",
            "properties": {
                "conversationId": {"type": "string", "description": "ID of the conversation"},
                "noteId": {"type": "string", "description": "ID of the note to delete"},
            },
            "required": ["conversationId", "noteId"],
        },
    },
}
