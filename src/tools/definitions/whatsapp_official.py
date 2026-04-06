from typing import Any

TOOLS: dict[str, dict[str, Any]] = {
    "whatsapp_template_message": {
        "method": "POST",
        "path": "/whatsapp/{phoneNumberId}/template-message",
        "description": "Send a pre-approved WhatsApp template message with optional dynamic variables to a contact.",
        "input_schema": {
            "type": "object",
            "properties": {
                "phoneNumberId": {"type": "string", "description": "ID of the WhatsApp Business phone number"},
                "to": {"type": "string", "description": "Recipient's phone number with country code"},
                "text": {"type": "string", "description": "Message text to store in conversation history"},
                "agentId": {"type": "string", "description": "ID of the agent to associate with this message"},
                "templateName": {"type": "string", "description": "Name of the pre-approved WhatsApp template"},
                "templateLangCode": {
                    "type": "string",
                    "description": "Language code for the template (e.g., 'en_US', 'pt_BR')",
                },
                "defaultStatus": {
                    "type": "string",
                    "enum": ["RESOLVED", "UNRESOLVED", "HUMAN_REQUESTED"],
                    "description": "Default status for conversation",
                },
                "contactName": {"type": "string", "description": "Optional contact name for new contacts"},
                "crmScenarioId": {"type": "string", "description": "Optional CRM scenario ID for synchronization"},
                "crmStepId": {"type": "string", "description": "Optional CRM step ID for synchronization"},
                "header_type": {
                    "type": "string",
                    "enum": ["image", "video", "document", "text"],
                    "description": "Type of media for header",
                },
                "header_text": {"type": "string", "description": "Required if header_type is text"},
                "header_link": {"type": "string", "description": "URL for the media file"},
                "header_id": {"type": "string", "description": "ID of previously uploaded media file"},
                "header_filename": {"type": "string", "description": "Optional filename for documents"},
            },
            "required": ["phoneNumberId", "to", "text", "agentId", "templateName", "templateLangCode"],
        },
    },
    "whatsapp_list_templates": {
        "method": "GET",
        "path": "/whatsapp/templates",
        "description": "List all Meta WhatsApp message templates available for your business account.",
        "input_schema": {
            "type": "object",
            "properties": {
                "agentId": {"type": "string", "description": "Filter templates by agent ID"},
            },
            "required": [],
        },
    },
    "whatsapp_create_template": {
        "method": "POST",
        "path": "/whatsapp/templates",
        "description": "Create a new message template in the associated WhatsApp Business Account (WABA).",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Template name"},
                "language": {"type": "string", "description": "Template language code"},
                "category": {
                    "type": "string",
                    "enum": ["AUTHENTICATION", "MARKETING", "UTILITY"],
                    "description": "Template category",
                },
                "components": {
                    "type": "array",
                    "items": {"type": "object"},
                    "description": "Template components (header, body, footer, buttons)",
                },
            },
            "required": ["name", "language", "category", "components"],
        },
    },
}
