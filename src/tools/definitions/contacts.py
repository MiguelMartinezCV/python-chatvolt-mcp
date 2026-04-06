from typing import Any

TOOLS: dict[str, dict[str, Any]] = {
    "list_contacts": {
        "method": "GET",
        "path": "/contacts",
        "description": "List all contacts, optionally filtered by search query, tags, or date range.",
        "input_schema": {
            "type": "object",
            "properties": {
                "search": {
                    "type": "string",
                    "description": "Search query to filter contacts by name, email, phone, or userId",
                },
                "tags": {"type": "array", "items": {"type": "string"}, "description": "Filter contacts by tags"},
                "createdAt": {"type": "string", "description": "Filter by creation date (e.g., 'YYYY-MM-DD HH:mm:ss')"},
                "limit": {"type": "integer", "description": "Maximum number of contacts to return"},
                "offset": {"type": "integer", "description": "Number of contacts to skip for pagination"},
            },
        },
    },
    "get_contact": {
        "method": "GET",
        "path": "/contacts/{id}",
        "description": "Retrieve details of a specific contact by ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID of the contact"},
            },
            "required": ["id"],
        },
    },
    "create_contact": {
        "method": "POST",
        "path": "/contacts",
        "description": "Create a new contact in the system.",
        "input_schema": {
            "type": "object",
            "properties": {
                "firstName": {"type": "string", "description": "Contact's first name"},
                "lastName": {"type": "string", "description": "Contact's last name"},
                "email": {"type": "string", "description": "Contact's email address"},
                "phoneNumber": {"type": "string", "description": "Contact's phone number (e.g., 5511988887777)"},
                "userId": {"type": "string", "description": "External ID from your system"},
                "tags": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Tags to associate with the contact",
                },
                "customFields": {
                    "type": "object",
                    "description": "Additional custom fields for the contact",
                },
            },
            "required": [],
        },
    },
    "update_contact": {
        "method": "PATCH",
        "path": "/contacts/{id}",
        "description": "Update an existing contact's information.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID of the contact to update"},
                "firstName": {"type": "string"},
                "lastName": {"type": "string"},
                "email": {"type": "string"},
                "phoneNumber": {"type": "string"},
                "userId": {"type": "string"},
                "tags": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Replace all tags with this list",
                },
                "addTags": {"type": "array", "items": {"type": "string"}, "description": "Tags to add"},
                "removeTags": {"type": "array", "items": {"type": "string"}, "description": "Tags to remove"},
                "customFields": {"type": "object", "description": "Custom fields to update"},
            },
            "required": ["id"],
        },
    },
    "delete_contact": {
        "method": "DELETE",
        "path": "/contacts/{id}",
        "description": "Delete a contact. This action is irreversible.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID of the contact to delete"},
            },
            "required": ["id"],
        },
    },
    "get_contact_conversations": {
        "method": "GET",
        "path": "/contacts/{id}/conversations",
        "description": "Get all conversations associated with a specific contact.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID of the contact"},
                "limit": {"type": "integer", "description": "Maximum number of conversations to return"},
            },
            "required": ["id"],
        },
    },
}
