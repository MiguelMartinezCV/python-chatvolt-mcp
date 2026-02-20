from typing import Dict, Any

TOOLS: Dict[str, Dict[str, Any]] = {
    "get_conversation_messages": {
        "method": "GET",
        "path": "/conversation/{conversationId}/messages/{count}",
        "description": "Retrieves the last ‘N’ messages from a conversation.",
        "input_schema": {
            "type": "object",
            "properties": {
                "conversationId": {"type": "string", "description": "ID of the conversation"},
                "count": {"type": "integer", "default": 2, "description": "Number of most recent messages to retrieve"}
            },
            "required": ["conversationId", "count"]
        }
    },
    "get_message": {
        "method": "GET",
        "path": "/messages/{messageId}",
        "description": "Retrieve details of a single message by its ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "messageId": {"type": "string", "description": "The unique ID of the message"},
                "includeSources": {"type": "boolean", "default": False, "description": "Include document sources in the response"}
            },
            "required": ["messageId"]
        }
    },
    "list_conversations": {
        "method": "GET",
        "path": "/conversation",
        "description": "Search for conversations by agent ID, creation date, and status.",
        "input_schema": {
            "type": "object",
            "properties": {
                "agentId": {"type": "string", "description": "Filter by agent ID. Pass 'null' for unassigned conversations."},
                "createdAt": {"type": "string", "description": "Filter by creation date (e.g., 'YYYY-MM-DD HH:mm:ss')"},
                "status": {"type": "string", "enum": ["RESOLVED", "UNRESOLVED", "HUMAN_REQUESTED"], "description": "Filter by status"}
            }
        }
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
            "required": ["conversationId"]
        }
    },
    "set_conversation_ai": {
        "method": "POST",
        "path": "/conversations/{conversationId}/set-ai-enabled",
        "description": "Enable or disable AI for a specific conversation.",
        "input_schema": {
            "type": "object",
            "properties": {
                "conversationId": {"type": "string", "description": "ID of the conversation"},
                "enabled": {"type": "boolean", "description": "True to enable AI, false to disable"}
            },
            "required": ["conversationId", "enabled"]
        }
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
                "from": {"type": "string", "enum": ["human", "agent"], "default": "human", "description": "Who the message is from"}
            },
            "required": ["conversationId", "message"]
        }
    }
}
