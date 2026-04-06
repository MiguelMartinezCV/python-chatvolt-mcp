from typing import Any

TOOLS: dict[str, dict[str, Any]] = {
    "send_interactive_buttons": {
        "method": "POST",
        "path": "/messages/interactive/send-buttons",
        "description": "Send a message with up to 3 reply buttons. Supported on WhatsApp, Z-API, and ZapperAPI.",
        "input_schema": {
            "type": "object",
            "properties": {
                "agentId": {"type": "string", "description": "The ID of the agent sending the message"},
                "conversationId": {"type": "string", "description": "The ID of the conversation"},
                "header_text": {"type": "string", "description": "Optional header text"},
                "body_text": {"type": "string", "description": "The main message body"},
                "footer_text": {"type": "string", "description": "Optional footer text"},
                "button_1_id": {"type": "string", "description": "ID for the first button"},
                "button_1_title": {"type": "string", "description": "Label for the first button"},
                "button_2_id": {"type": "string", "description": "ID for the second button"},
                "button_2_title": {"type": "string", "description": "Label for the second button"},
                "button_3_id": {"type": "string", "description": "ID for the third button"},
                "button_3_title": {"type": "string", "description": "Label for the third button"},
            },
            "required": ["agentId", "conversationId", "body_text", "button_1_id", "button_1_title"],
        },
    },
    "send_interactive_list": {
        "method": "POST",
        "path": "/messages/interactive/send-lists",
        "description": "Send an interactive list message with sections and rows.",
        "input_schema": {
            "type": "object",
            "properties": {
                "agentId": {"type": "string", "description": "The ID of the agent sending the message"},
                "conversationId": {"type": "string", "description": "The ID of the conversation"},
                "header_text": {"type": "string", "description": "Optional header text"},
                "body_text": {"type": "string", "description": "The main message body"},
                "footer_text": {"type": "string", "description": "Optional footer text"},
                "button_text": {"type": "string", "description": "Text for the list button"},
                "sections": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "rows": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "id": {"type": "string"},
                                        "title": {"type": "string"},
                                        "description": {"type": "string"},
                                    },
                                },
                            },
                        },
                    },
                    "description": "Array of sections with rows",
                },
            },
            "required": ["agentId", "conversationId", "body_text", "button_text", "sections"],
        },
    },
    "send_cta_url": {
        "method": "POST",
        "path": "/messages/interactive/send-cta",
        "description": "Send a call-to-action message with a clickable URL button.",
        "input_schema": {
            "type": "object",
            "properties": {
                "agentId": {"type": "string", "description": "The ID of the agent sending the message"},
                "conversationId": {"type": "string", "description": "The ID of the conversation"},
                "header_text": {"type": "string", "description": "Optional header text"},
                "body_text": {"type": "string", "description": "The main message body"},
                "footer_text": {"type": "string", "description": "Optional footer text"},
                "url": {"type": "string", "description": "The URL to open when button is clicked"},
                "url_text": {"type": "string", "description": "Text to display on the button"},
            },
            "required": ["agentId", "conversationId", "body_text", "url", "url_text"],
        },
    },
    "send_location": {
        "method": "POST",
        "path": "/messages/interactive/send-location",
        "description": "Send a location message with latitude and longitude coordinates.",
        "input_schema": {
            "type": "object",
            "properties": {
                "agentId": {"type": "string", "description": "The ID of the agent sending the message"},
                "conversationId": {"type": "string", "description": "The ID of the conversation"},
                "latitude": {"type": "number", "description": "Latitude coordinate"},
                "longitude": {"type": "number", "description": "Longitude coordinate"},
                "title": {"type": "string", "description": "Optional title for the location"},
                "address": {"type": "string", "description": "Optional address text"},
            },
            "required": ["agentId", "conversationId", "latitude", "longitude"],
        },
    },
    "request_location": {
        "method": "POST",
        "path": "/messages/interactive/location-request",
        "description": "Request the user to share their location.",
        "input_schema": {
            "type": "object",
            "properties": {
                "agentId": {"type": "string", "description": "The ID of the agent sending the message"},
                "conversationId": {"type": "string", "description": "The ID of the conversation"},
                "body_text": {"type": "string", "description": "The message asking for location"},
            },
            "required": ["agentId", "conversationId", "body_text"],
        },
    },
    "send_contact": {
        "method": "POST",
        "path": "/messages/interactive/send-contact",
        "description": "Send a contact card to the conversation.",
        "input_schema": {
            "type": "object",
            "properties": {
                "agentId": {"type": "string", "description": "The ID of the agent sending the message"},
                "conversationId": {"type": "string", "description": "The ID of the conversation"},
                "name": {"type": "string", "description": "Contact's full name"},
                "firstName": {"type": "string", "description": "Contact's first name"},
                "lastName": {"type": "string", "description": "Contact's last name"},
                "phone": {"type": "string", "description": "Contact's phone number"},
                "email": {"type": "string", "description": "Contact's email address"},
                "organization": {"type": "string", "description": "Contact's organization"},
                "title": {"type": "string", "description": "Contact's job title"},
            },
            "required": ["agentId", "conversationId", "name"],
        },
    },
}
