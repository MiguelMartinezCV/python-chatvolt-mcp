from typing import Any

TOOLS: dict[str, dict[str, Any]] = {
    "get_whitelist_numbers": {
        "method": "GET",
        "path": "/agent-whitelist-whatsapp/{id}",
        "description": "Get all WhatsApp whitelist numbers for an agent.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "Agent ID"},
            },
            "required": ["id"],
        },
    },
    "add_whitelist_number": {
        "method": "POST",
        "path": "/agent-whitelist-whatsapp",
        "description": "Add a WhatsApp number to the whitelist for an agent.",
        "input_schema": {
            "type": "object",
            "properties": {
                "agentId": {"type": "string", "description": "Agent ID"},
                "whatsappNumber": {"type": "string", "description": "WhatsApp number to whitelist"},
            },
            "required": ["agentId", "whatsappNumber"],
        },
    },
    "update_whitelist_number": {
        "method": "PATCH",
        "path": "/agent-whitelist-whatsapp/{id}",
        "description": "Update a WhatsApp number in the whitelist (replace old with new).",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "Agent ID"},
                "oldWhatsappNumber": {"type": "string", "description": "Current WhatsApp number in whitelist"},
                "newWhatsappNumber": {"type": "string", "description": "New WhatsApp number to add"},
            },
            "required": ["id", "oldWhatsappNumber", "newWhatsappNumber"],
        },
    },
    "delete_whitelist_number": {
        "method": "DELETE",
        "path": "/agent-whitelist-whatsapp/{id}",
        "description": "Remove a WhatsApp number from the whitelist.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "Agent ID"},
                "whatsappNumber": {"type": "string", "description": "WhatsApp number to remove from whitelist"},
            },
            "required": ["id", "whatsappNumber"],
        },
    },
}
