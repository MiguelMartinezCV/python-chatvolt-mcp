from typing import Any

TOOLS: dict[str, dict[str, Any]] = {
    "list_dispatches": {
        "method": "GET",
        "path": "/dispatches",
        "description": "List all dispatches (broadcast campaigns), optionally filtered by status or date. Supports cursor-based pagination.",
        "input_schema": {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "enum": ["pending", "sending", "completed", "failed"],
                    "description": "Filter by dispatch status",
                },
                "createdAt": {"type": "string", "description": "Filter by creation date (e.g., 'YYYY-MM-DD HH:mm:ss')"},
                "cursor": {"type": "string", "description": "Pagination cursor for fetching next page of results"},
                "limit": {"type": "integer", "default": 50, "description": "Number of results to return (max 100)"},
            },
        },
    },
    "get_dispatch": {
        "method": "GET",
        "path": "/dispatches/{id}",
        "description": "Retrieve details of a specific dispatch by ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID of the dispatch"},
            },
            "required": ["id"],
        },
    },
    "create_dispatch": {
        "method": "POST",
        "path": "/dispatches",
        "description": "Create a new dispatch (broadcast campaign) to send messages to a list of contacts.",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Name of the dispatch campaign"},
                "agentId": {"type": "string", "description": "ID of the agent to use for sending"},
                "contactIds": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of contact IDs to send to",
                },
                "message": {
                    "type": "string",
                    "description": "Message template to send. Can include variables like {{firstName}}",
                },
                "scheduledAt": {
                    "type": "string",
                    "description": "Optional scheduled time (e.g., 'YYYY-MM-DD HH:mm:ss')",
                },
                "channel": {
                    "type": "string",
                    "enum": ["whatsapp", "telegram", "zapi", "instagram"],
                    "description": "Channel to send through",
                },
                "tags": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Filter contacts by tags instead of explicit contactIds",
                },
            },
            "required": ["name", "agentId", "message"],
        },
    },
    "update_dispatch": {
        "method": "PATCH",
        "path": "/dispatches/{id}",
        "description": "Update an existing dispatch configuration.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID of the dispatch to update"},
                "name": {"type": "string"},
                "agentId": {"type": "string"},
                "contactIds": {"type": "array", "items": {"type": "string"}},
                "message": {"type": "string"},
                "scheduledAt": {"type": "string"},
                "channel": {"type": "string", "enum": ["whatsapp", "telegram", "zapi", "instagram"]},
            },
            "required": ["id"],
        },
    },
    "delete_dispatch": {
        "method": "DELETE",
        "path": "/dispatches/{id}",
        "description": "Delete a dispatch. Only pending dispatches can be deleted.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID of the dispatch to delete"},
            },
            "required": ["id"],
        },
    },
    "populate_dispatch_queue": {
        "method": "POST",
        "path": "/dispatches/{id}/populate-queue",
        "description": "Populate the dispatch queue for a given dispatch. Clears existing queue and repopulates based on contact lists. Respects inclusion and exclusion rules.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID of the dispatch to populate"},
            },
            "required": ["id"],
        },
    },
    "list_contact_lists": {
        "method": "GET",
        "path": "/dispatches/contacts/lists",
        "description": "Retrieve all contact lists with optional filtering and pagination.",
        "input_schema": {
            "type": "object",
            "properties": {
                "offset": {"type": "integer", "default": 0, "description": "Number of records to skip"},
                "limit": {"type": "integer", "default": 100, "description": "Max records to return"},
                "search": {"type": "string", "description": "Search term for list name"},
            },
        },
    },
    "get_contact_list": {
        "method": "GET",
        "path": "/dispatches/contacts/lists/{id}",
        "description": "Retrieve a specific contact list by ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID of the contact list"},
            },
            "required": ["id"],
        },
    },
    "create_contact_list": {
        "method": "POST",
        "path": "/dispatches/contacts/lists",
        "description": "Create a new contact list for dispatches.",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Name of the contact list"},
                "description": {"type": "string", "description": "Description of the contact list"},
            },
            "required": ["name"],
        },
    },
    "update_contact_list": {
        "method": "PUT",
        "path": "/dispatches/contacts/lists/{id}",
        "description": "Update an existing contact list.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID of the contact list to update"},
                "name": {"type": "string", "description": "New name for the contact list"},
                "description": {"type": "string", "description": "New description"},
            },
            "required": ["id"],
        },
    },
    "delete_contact_list": {
        "method": "DELETE",
        "path": "/dispatches/contacts/lists/{id}",
        "description": "Delete a contact list.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID of the contact list to delete"},
            },
            "required": ["id"],
        },
    },
}
