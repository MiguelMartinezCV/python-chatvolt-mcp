from typing import Any

TOOLS: dict[str, dict[str, Any]] = {
    "update_datasource": {
        "method": "PATCH",
        "path": "/datasources/{id}",
        "description": "Update a datasource configuration.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID of the datasource"},
                "name": {"type": "string", "description": "New name for the datasource"},
                "customId": {"type": "string", "description": "Custom identifier"},
            },
            "required": ["id"],
        },
    },
    "delete_datasource": {
        "method": "DELETE",
        "path": "/datasources/{id}",
        "description": "Delete a datasource. This action is irreversible.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID of the datasource to delete"},
            },
            "required": ["id"],
        },
    },
    "sync_datasource": {
        "method": "POST",
        "path": "/datasources/{id}/sync",
        "description": "Trigger a manual sync of the datasource.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID of the datasource to sync"},
            },
            "required": ["id"],
        },
    },
    "get_datasource_status": {
        "method": "GET",
        "path": "/datasources/{id}/status",
        "description": "Get the sync status and health of a datasource.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID of the datasource"},
            },
            "required": ["id"],
        },
    },
}
