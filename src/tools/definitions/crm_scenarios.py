from typing import Any

TOOLS: dict[str, dict[str, Any]] = {
    "create_crm_scenario": {
        "method": "POST",
        "path": "/crm/scenario",
        "description": "Create a new CRM scenario (workflow blueprint).",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Name of the scenario"},
                "agentId": {"type": "string", "description": "Default agent ID for this scenario"},
                "description": {"type": "string", "description": "Description of the scenario"},
                "defaultStepId": {"type": "string", "description": "Default step ID for new conversations"},
            },
            "required": ["name"],
        },
    },
    "get_crm_scenario": {
        "method": "GET",
        "path": "/crm/scenario/{id}",
        "description": "Get details of a specific CRM scenario.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID of the scenario"},
            },
            "required": ["id"],
        },
    },
    "update_crm_scenario": {
        "method": "PATCH",
        "path": "/crm/scenario/{id}",
        "description": "Update an existing CRM scenario.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID of the scenario to update"},
                "name": {"type": "string"},
                "agentId": {"type": "string"},
                "description": {"type": "string"},
                "defaultStepId": {"type": "string"},
            },
            "required": ["id"],
        },
    },
    "delete_crm_scenario": {
        "method": "DELETE",
        "path": "/crm/scenario/{id}",
        "description": "Delete a CRM scenario. This action is irreversible.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID of the scenario to delete"},
            },
            "required": ["id"],
        },
    },
}
