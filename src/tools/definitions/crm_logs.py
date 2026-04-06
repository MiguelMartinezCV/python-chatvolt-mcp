from typing import Any

TOOLS: dict[str, dict[str, Any]] = {
    "list_crm_logs": {
        "method": "GET",
        "path": "/crm/logs",
        "description": "List CRM conversation logs with optional filters. Supports cursor-based pagination.",
        "input_schema": {
            "type": "object",
            "properties": {
                "scenarioId": {"type": "string", "description": "Filter by CRM scenario ID"},
                "stepId": {"type": "string", "description": "Filter by CRM step ID"},
                "conversationId": {"type": "string", "description": "Filter by conversation ID"},
                "status": {
                    "type": "string",
                    "enum": ["RESOLVED", "UNRESOLVED", "HUMAN_REQUESTED"],
                    "description": "Filter by status",
                },
                "from": {"type": "string", "description": "Start date filter (YYYY-MM-DD)"},
                "to": {"type": "string", "description": "End date filter (YYYY-MM-DD)"},
                "cursor": {"type": "string", "description": "Pagination cursor for fetching next page of results"},
                "limit": {"type": "integer", "default": 50, "description": "Number of results to return (max 100)"},
            },
        },
    },
    "get_crm_log": {
        "method": "GET",
        "path": "/crm/logs/{id}",
        "description": "Get details of a specific CRM conversation log.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID of the CRM log entry"},
            },
            "required": ["id"],
        },
    },
}
