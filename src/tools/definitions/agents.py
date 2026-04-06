from typing import Any

TOOLS: dict[str, dict[str, Any]] = {
    "query_agent": {
        "method": "POST",
        "path": "/agents/{id}/query",
        "description": "Send a query to a specific agent and receive a response. The ID can be the agent's UUID or its handle (prefixed with '@', e.g., '@my-agent').",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "string",
                    "description": "ID or handle of the agent to query (use '@' prefix for handles)",
                },
                "query": {"type": "string", "description": "The question or command"},
                "streaming": {"type": "boolean", "default": False},
                "conversationId": {"type": "string"},
                "contactId": {"type": "string"},
                "contact": {
                    "type": "object",
                    "properties": {
                        "firstName": {"type": "string"},
                        "lastName": {"type": "string"},
                        "email": {"type": "string"},
                        "phoneNumber": {"type": "string"},
                        "userId": {"type": "string"},
                    },
                },
                "visitorId": {"type": "string"},
                "temperature": {"type": "number"},
                "modelName": {"type": "string"},
                "presencePenalty": {"type": "number"},
                "frequencyPenalty": {"type": "number"},
                "topP": {"type": "number"},
                "filters": {
                    "type": "object",
                    "properties": {
                        "custom_ids": {"type": "array", "items": {"type": "string"}},
                        "datasource_ids": {"type": "array", "items": {"type": "string"}},
                    },
                },
                "systemPrompt": {"type": "string"},
                "context": {"type": "object"},
                "callbackURL": {"type": "string"},
            },
            "required": ["id", "query"],
        },
    },
    "get_agent": {
        "method": "GET",
        "path": "/agents/{id}",
        "description": "Retrieve details of a specific agent. The ID can be the agent's UUID or its handle (prefixed with '@', e.g., '@my-agent').",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID or handle of the agent (use '@' prefix for handles)"}
            },
            "required": ["id"],
        },
    },
    "list_agents": {
        "method": "GET",
        "path": "/agents",
        "description": "List all agents in the organization with pagination support.",
        "input_schema": {
            "type": "object",
            "properties": {
                "limit": {"type": "integer", "description": "Maximum number of agents to return (default 50)"},
                "offset": {"type": "integer", "description": "Number of agents to skip for pagination"},
            },
        },
    },
    "create_agent": {
        "method": "POST",
        "path": "/agents",
        "description": "Create a new AI agent with customizable settings including visibility, handle, interface configuration, and external URL integrations.",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Agent name. If not provided, a fun name will be generated automatically.",
                },
                "description": {"type": "string", "description": "Agent description."},
                "modelName": {
                    "type": "string",
                    "description": "LLM model to be used by the agent. Check the API for available model names.",
                },
                "temperature": {
                    "type": "number",
                    "description": "Model temperature (min 0.0, max 1.0). Controls randomness.",
                },
                "systemPrompt": {"type": "string", "description": "System prompt to guide the agent's behavior."},
                "visibility": {
                    "type": "string",
                    "enum": ["public", "private"],
                    "description": "Agent visibility. 'public' allows access without authentication, 'private' restricts access to the organization.",
                },
                "handle": {
                    "type": "string",
                    "description": "A unique identifier (slug) for the agent. Used for friendly URLs.",
                },
                "interfaceConfig": {
                    "type": "object",
                    "description": "Chat interface settings (colors, initial messages, etc.).",
                },
                "configUrlExternal": {
                    "type": "object",
                    "description": "External URL configurations.",
                    "properties": {
                        "url": {"type": "string"},
                        "header": {"type": "string"},
                    },
                },
                "configUrlInfosSystemExternal": {
                    "type": "object",
                    "description": "External URL configurations of the system.",
                    "properties": {
                        "url_webhook_external": {"type": "string"},
                        "headerKey": {"type": "string"},
                    },
                },
                "enableInactiveHours": {
                    "type": "boolean",
                    "description": "Enable or disable inactive hours for the agent.",
                },
                "inactiveHours": {
                    "type": "object",
                    "description": "JSON object specifying the agent's inactive hours per channel (whatsapp, website, instagram) with days and time ranges.",
                },
                "tools": {
                    "type": "array",
                    "items": {"type": "object"},
                    "description": "List of tools to be associated with the agent.",
                },
            },
            "required": ["name"],
        },
    },
    "update_agent": {
        "method": "PATCH",
        "path": "/agents/{id}",
        "description": "Update an existing agent's configuration including name, description, model, temperature, system prompt, visibility, handle, interface settings, and inactive hours. The ID can be the agent's UUID or its handle.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "string",
                    "description": "ID or handle of the agent to update (use '@' prefix for handles)",
                },
                "name": {"type": "string", "description": "Agent name."},
                "description": {"type": "string", "description": "Agent description."},
                "modelName": {"type": "string", "description": "LLM model to be used by the agent."},
                "temperature": {"type": "number", "description": "Model temperature (min 0.0, max 1.0)."},
                "systemPrompt": {"type": "string", "description": "System prompt to guide the agent's behavior."},
                "visibility": {"type": "string", "enum": ["public", "private"], "description": "Agent visibility."},
                "handle": {"type": "string", "description": "A unique identifier (slug) for the agent."},
                "interfaceConfig": {"type": "object", "description": "Chat interface settings."},
                "configUrlExternal": {
                    "type": "object",
                    "description": "External URL configurations.",
                    "properties": {
                        "url": {"type": "string"},
                        "header": {"type": "string"},
                    },
                },
                "configUrlInfosSystemExternal": {
                    "type": "object",
                    "description": "External URL configurations of the system.",
                    "properties": {
                        "url_webhook_external": {"type": "string"},
                        "headerKey": {"type": "string"},
                    },
                },
                "enableInactiveHours": {
                    "type": "boolean",
                    "description": "Enable or disable inactive hours for the agent.",
                },
                "inactiveHours": {
                    "type": "object",
                    "description": "JSON object specifying the agent's inactive hours per channel.",
                },
                "tools": {
                    "type": "array",
                    "items": {"type": "object"},
                    "description": "List of tools to be associated with the agent.",
                },
            },
            "required": ["id"],
        },
    },
    "delete_agent": {
        "method": "DELETE",
        "path": "/agents/{id}",
        "description": "Delete an AI agent. This action is irreversible. The ID can be the agent's UUID or its handle.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "string",
                    "description": "ID or handle of the agent to delete (use '@' prefix for handles)",
                },
            },
            "required": ["id"],
        },
    },
    "get_models": {
        "method": "GET",
        "path": "/agents/models",
        "description": "Get available AI models and their pricing.",
        "input_schema": {"type": "object", "properties": {}},
    },
    "toggle_webhook": {
        "method": "PATCH",
        "path": "/agents/{id}/webhook",
        "description": "Enable or disable a specific webhook for an agent. The ID can be the agent's UUID or its handle.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID or handle of the agent (use '@' prefix for handles)"},
                "type": {"type": "string", "enum": ["whatsapp", "telegram", "zapi", "instagram"]},
                "enabled": {"type": "boolean"},
            },
            "required": ["id", "type", "enabled"],
        },
    },
    "get_agent_tools": {
        "method": "GET",
        "path": "/api/agents/{agentId}/tools",
        "description": "Get all tools associated with a specific agent.",
        "input_schema": {
            "type": "object",
            "properties": {"agentId": {"type": "string", "description": "ID of the agent"}},
            "required": ["agentId"],
        },
    },
    "create_agent_tool": {
        "method": "POST",
        "path": "/api/agents/{agentId}/tools",
        "description": "Create a new tool for a specific agent. IMPORTANT: For GET tools with query parameters, define them both in the 'url' and the 'queryParameters' array.",
        "input_schema": {
            "type": "object",
            "properties": {
                "agentId": {"type": "string", "description": "ID of the agent"},
                "type": {
                    "type": "string",
                    "enum": [
                        "http",
                        "datastore",
                        "mark_as_resolved",
                        "request_human",
                        "delayed_responses",
                        "follow_up_messages",
                    ],
                    "description": "The type of tool to create.",
                },
                "datastoreId": {"type": "string", "description": "Required if type is 'datastore'"},
                "formId": {"type": "string", "description": "Required if type is 'form'"},
                "isRaw": {"type": "boolean", "description": "Only for 'http' type. If true, uses a raw cURL command."},
                "config": {
                    "type": "object",
                    "description": "Configuration object for the tool.",
                    "properties": {
                        "name": {"type": "string", "description": "Friendly name of the tool"},
                        "description": {"type": "string", "description": "Clear explanation of what the tool does"},
                        "url": {"type": "string", "description": "Base URL for HTTP tools"},
                        "method": {"type": "string", "enum": ["GET", "POST", "PUT", "DELETE", "PATCH"]},
                        "withApproval": {"type": "boolean", "description": "Require human approval before execution"},
                        "headers": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "key": {"type": "string"},
                                    "value": {"type": "string"},
                                    "isUserProvided": {"type": "boolean"},
                                    "description": {"type": "string"},
                                    "acceptedValues": {"type": "array", "items": {"type": "string"}},
                                },
                            },
                        },
                        "queryParameters": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "key": {"type": "string"},
                                    "value": {"type": "string"},
                                    "isUserProvided": {"type": "boolean"},
                                    "description": {"type": "string"},
                                    "acceptedValues": {"type": "array", "items": {"type": "string"}},
                                },
                            },
                        },
                        "pathVariables": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "key": {"type": "string"},
                                    "value": {"type": "string"},
                                    "isUserProvided": {"type": "boolean"},
                                    "description": {"type": "string"},
                                    "acceptedValues": {"type": "array", "items": {"type": "string"}},
                                },
                            },
                        },
                        "body": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "key": {"type": "string"},
                                    "value": {"type": "string"},
                                    "isUserProvided": {"type": "boolean"},
                                    "description": {"type": "string"},
                                    "acceptedValues": {"type": "array", "items": {"type": "string"}},
                                },
                            },
                        },
                        "rawBody": {"type": "string", "description": "Raw JSON string for the request body"},
                        "hasMaximumToolCalls": {"type": "boolean"},
                        "maximumToolCalls": {"type": "integer"},
                        "isErrorCountable": {"type": "boolean"},
                        "delay": {"type": "integer", "description": "Seconds for delayed_responses"},
                        "max_sends": {"type": "integer", "description": "Used in follow_up_messages"},
                        "interval_hours": {"type": "integer", "description": "Used in follow_up_messages"},
                        "messages": {"type": "string", "description": "Used in follow_up_messages, separated by ||"},
                    },
                },
            },
            "required": ["agentId", "type"],
        },
    },
    "update_agent_tool": {
        "method": "PATCH",
        "path": "/api/agents/{agentId}/tools/{toolId}",
        "description": "Update an existing tool for a specific agent. IMPORTANT: For GET tools with query parameters, define them both in the 'url' and the 'queryParameters' array.",
        "input_schema": {
            "type": "object",
            "properties": {
                "agentId": {"type": "string", "description": "ID of the agent"},
                "toolId": {"type": "string", "description": "ID of the tool to update"},
                "type": {
                    "type": "string",
                    "enum": [
                        "http",
                        "datastore",
                        "mark_as_resolved",
                        "request_human",
                        "delayed_responses",
                        "follow_up_messages",
                    ],
                    "description": "The type of tool.",
                },
                "datastoreId": {"type": "string", "description": "Required if type is 'datastore'"},
                "formId": {"type": "string", "description": "Required if type is 'form'"},
                "isRaw": {"type": "boolean", "description": "Only for 'http' type."},
                "config": {
                    "type": "object",
                    "description": "Configuration object for the tool.",
                    "properties": {
                        "name": {"type": "string"},
                        "description": {"type": "string"},
                        "url": {"type": "string"},
                        "method": {"type": "string", "enum": ["GET", "POST", "PUT", "DELETE", "PATCH"]},
                        "withApproval": {"type": "boolean"},
                        "headers": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "key": {"type": "string"},
                                    "value": {"type": "string"},
                                    "isUserProvided": {"type": "boolean"},
                                    "description": {"type": "string"},
                                    "acceptedValues": {"type": "array", "items": {"type": "string"}},
                                },
                            },
                        },
                        "queryParameters": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "key": {"type": "string"},
                                    "value": {"type": "string"},
                                    "isUserProvided": {"type": "boolean"},
                                    "description": {"type": "string"},
                                    "acceptedValues": {"type": "array", "items": {"type": "string"}},
                                },
                            },
                        },
                        "pathVariables": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "key": {"type": "string"},
                                    "value": {"type": "string"},
                                    "isUserProvided": {"type": "boolean"},
                                    "description": {"type": "string"},
                                    "acceptedValues": {"type": "array", "items": {"type": "string"}},
                                },
                            },
                        },
                        "body": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "key": {"type": "string"},
                                    "value": {"type": "string"},
                                    "isUserProvided": {"type": "boolean"},
                                    "description": {"type": "string"},
                                    "acceptedValues": {"type": "array", "items": {"type": "string"}},
                                },
                            },
                        },
                        "rawBody": {"type": "string"},
                        "hasMaximumToolCalls": {"type": "boolean"},
                        "maximumToolCalls": {"type": "integer"},
                        "isErrorCountable": {"type": "boolean"},
                        "delay": {"type": "integer"},
                        "max_sends": {"type": "integer"},
                        "interval_hours": {"type": "integer"},
                        "messages": {"type": "string"},
                    },
                },
            },
            "required": ["agentId", "toolId", "type"],
        },
    },
    "delete_agent_tool": {
        "method": "DELETE",
        "path": "/api/agents/{agentId}/tools/{toolId}",
        "description": "Delete a specific tool from an agent.",
        "input_schema": {
            "type": "object",
            "properties": {
                "agentId": {"type": "string", "description": "ID of the agent"},
                "toolId": {"type": "string", "description": "ID of the tool to delete"},
            },
            "required": ["agentId", "toolId"],
        },
    },
}
