from typing import Any

TOOLS: dict[str, dict[str, Any]] = {
    "zapi_list_instances": {
        "method": "GET",
        "path": "/zapi/instances",
        "description": "List all Z-API instances connected to your account.",
        "input_schema": {
            "type": "object",
            "properties": {},
        },
    },
    "zapi_send_text": {
        "method": "POST",
        "path": "/zapi/{instanceId}/send-text",
        "description": "Send a text message via Z-API (WhatsApp integration).",
        "input_schema": {
            "type": "object",
            "properties": {
                "instanceId": {"type": "string", "description": "Z-API instance ID"},
                "phone": {
                    "type": "string",
                    "description": "Recipient phone number with country code (e.g., 5511999999999)",
                },
                "message": {"type": "string", "description": "Text message to send"},
                "isGroup": {"type": "boolean", "description": "Set to true if sending to a group"},
            },
            "required": ["instanceId", "phone", "message"],
        },
    },
    "zapi_send_media": {
        "method": "POST",
        "path": "/zapi/{instanceId}/send-media",
        "description": "Send a media message (image, video, audio, document) via Z-API.",
        "input_schema": {
            "type": "object",
            "properties": {
                "instanceId": {"type": "string", "description": "Z-API instance ID"},
                "phone": {"type": "string", "description": "Recipient phone number with country code"},
                "mediaUrl": {"type": "string", "description": "URL of the media file to send"},
                "mediaType": {
                    "type": "string",
                    "enum": ["image", "video", "audio", "document"],
                    "description": "Type of media",
                },
                "caption": {"type": "string", "description": "Optional caption for the media"},
                "filename": {"type": "string", "description": "Filename for document type"},
            },
            "required": ["instanceId", "phone", "mediaUrl", "mediaType"],
        },
    },
    "zapi_send_template": {
        "method": "POST",
        "path": "/zapi/{instanceId}/send-template",
        "description": "Send a WhatsApp template message via Z-API.",
        "input_schema": {
            "type": "object",
            "properties": {
                "instanceId": {"type": "string", "description": "Z-API instance ID"},
                "phone": {"type": "string", "description": "Recipient phone number with country code"},
                "templateName": {"type": "string", "description": "Name of the WhatsApp template"},
                "templateLanguage": {"type": "string", "description": "Template language code (e.g., 'en', 'pt_BR')"},
                "templateVariables": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Variables to fill into the template",
                },
            },
            "required": ["instanceId", "phone", "templateName"],
        },
    },
    "zapi_send_list": {
        "method": "POST",
        "path": "/zapi/{instanceId}/send-list",
        "description": "Send an interactive list message via Z-API WhatsApp.",
        "input_schema": {
            "type": "object",
            "properties": {
                "instanceId": {"type": "string", "description": "Z-API instance ID"},
                "phone": {"type": "string", "description": "Recipient phone number with country code"},
                "title": {"type": "string", "description": "List title"},
                "description": {"type": "string", "description": "List description"},
                "buttonText": {"type": "string", "description": "Text for the list button"},
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
                },
            },
            "required": ["instanceId", "phone", "title", "buttonText", "sections"],
        },
    },
    "zapi_send_buttons": {
        "method": "POST",
        "path": "/zapi/{instanceId}/send-buttons",
        "description": "Send an interactive buttons message via Z-API WhatsApp.",
        "input_schema": {
            "type": "object",
            "properties": {
                "instanceId": {"type": "string", "description": "Z-API instance ID"},
                "phone": {"type": "string", "description": "Recipient phone number with country code"},
                "message": {"type": "string", "description": "Message text"},
                "buttons": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "text": {"type": "string"},
                        },
                    },
                },
            },
            "required": ["instanceId", "phone", "message", "buttons"],
        },
    },
}
