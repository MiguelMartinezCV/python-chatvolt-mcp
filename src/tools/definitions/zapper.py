from typing import Any

TOOLS: dict[str, dict[str, Any]] = {
    "zapper_send_message": {
        "method": "POST",
        "path": "/zapper/instances/{id}/message",
        "description": "Send a message through the Zapper integration with text and/or attachments.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "string",
                    "description": "Zapper instance ID (externalId of the ServiceProvider of type 'zapper')",
                },
                "message": {"type": "string", "description": "Textual content of the message"},
                "contactPhone": {"type": "string", "description": "Recipient's number"},
                "attachments": {
                    "type": "array",
                    "items": {"type": "object"},
                    "description": "Optional list of attachments to be sent",
                },
            },
            "required": ["id", "message", "contactPhone"],
        },
    },
}
