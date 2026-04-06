from typing import Any

TOOLS: dict[str, dict[str, Any]] = {
    "twilio_send_sms": {
        "method": "POST",
        "path": "/twilio/{ownerPhone}/{contactPhone}/message",
        "description": "Send an SMS message to a destination phone number using a configured Twilio instance.",
        "input_schema": {
            "type": "object",
            "properties": {
                "ownerPhone": {"type": "string", "description": "The Twilio phone number that owns the integration"},
                "contactPhone": {"type": "string", "description": "Recipient's phone number"},
                "message": {"type": "string", "description": "Textual content of the message"},
            },
            "required": ["ownerPhone", "contactPhone", "message"],
        },
    },
}
