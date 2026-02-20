from typing import Dict, Any

TOOLS: Dict[str, Dict[str, Any]] = {
    "query_agent": {
        "method": "POST",
        "path": "/agents/{id}/query",
        "description": "Send a query to a specific agent and receive a response.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID of the agent to query"},
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
                        "userId": {"type": "string"}
                    }
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
                        "datasource_ids": {"type": "array", "items": {"type": "string"}}
                    }
                },
                "systemPrompt": {"type": "string"},
                "context": {"type": "object"},
                "callbackURL": {"type": "string"}
            },
            "required": ["id", "query"]
        }
    },
    "get_agent": {
        "method": "GET",
        "path": "/agents/{id}",
        "description": "Retrieve details of a specific agent.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID of the agent"}
            },
            "required": ["id"]
        }
    },
    "create_agent": {
        "method": "POST",
        "path": "/agents",
        "description": "Create a new AI agent.",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "description": {"type": "string"},
                "modelName": {"type": "string"},
                "temperature": {"type": "number"},
                "systemPrompt": {"type": "string"}
            },
            "required": ["name"]
        }
    },
    "update_agent": {
        "method": "PATCH",
        "path": "/agents/{id}",
        "description": "Update an existing agent's configuration.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID of the agent to update"},
                "name": {"type": "string"},
                "description": {"type": "string"},
                "modelName": {"type": "string"},
                "temperature": {"type": "number"},
                "systemPrompt": {"type": "string"}
            },
            "required": ["id"]
        }
    },
    "get_models": {
        "method": "GET",
        "path": "/agents/models",
        "description": "Get available AI models and their pricing.",
        "input_schema": {
            "type": "object",
            "properties": {}
        }
    },
    "toggle_webhook": {
        "method": "PATCH",
        "path": "/agents/{id}/webhook",
        "description": "Enable or disable a specific webhook for an agent.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "Agent ID"},
                "type": {"type": "string", "enum": ["whatsapp", "telegram", "zapi", "instagram"]},
                "enabled": {"type": "boolean"}
            },
            "required": ["id", "type", "enabled"]
        }
    },
    "get_agent_tools": {
        "method": "GET",
        "path": "/api/agents/{agentId}/tools",
        "description": "Get all tools associated with a specific agent.",
        "input_schema": {
            "type": "object",
            "properties": {
                "agentId": {"type": "string", "description": "ID of the agent"}
            },
            "required": ["agentId"]
        }
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
                    "enum": ["http", "datastore", "mark_as_resolved", "request_human", "delayed_responses", "follow_up_messages"],
                    "description": "The type of tool to create."
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
                                    "acceptedValues": {"type": "array", "items": {"type": "string"}}
                                }
                            }
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
                                    "acceptedValues": {"type": "array", "items": {"type": "string"}}
                                }
                            }
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
                                    "acceptedValues": {"type": "array", "items": {"type": "string"}}
                                }
                            }
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
                                    "acceptedValues": {"type": "array", "items": {"type": "string"}}
                                }
                            }
                        },
                        "rawBody": {"type": "string", "description": "Raw JSON string for the request body"},
                        "hasMaximumToolCalls": {"type": "boolean"},
                        "maximumToolCalls": {"type": "integer"},
                        "isErrorCountable": {"type": "boolean"},
                        "delay": {"type": "integer", "description": "Seconds for delayed_responses"},
                        "max_sends": {"type": "integer", "description": "Used in follow_up_messages"},
                        "interval_hours": {"type": "integer", "description": "Used in follow_up_messages"},
                        "messages": {"type": "string", "description": "Used in follow_up_messages, separated by ||"}
                    }
                }
            },
            "required": ["agentId", "type"]
        }
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
                    "enum": ["http", "datastore", "mark_as_resolved", "request_human", "delayed_responses", "follow_up_messages"],
                    "description": "The type of tool."
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
                                    "acceptedValues": {"type": "array", "items": {"type": "string"}}
                                }
                            }
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
                                    "acceptedValues": {"type": "array", "items": {"type": "string"}}
                                }
                            }
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
                                    "acceptedValues": {"type": "array", "items": {"type": "string"}}
                                }
                            }
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
                                    "acceptedValues": {"type": "array", "items": {"type": "string"}}
                                }
                            }
                        },
                        "rawBody": {"type": "string"},
                        "hasMaximumToolCalls": {"type": "boolean"},
                        "maximumToolCalls": {"type": "integer"},
                        "isErrorCountable": {"type": "boolean"},
                        "delay": {"type": "integer"},
                        "max_sends": {"type": "integer"},
                        "interval_hours": {"type": "integer"},
                        "messages": {"type": "string"}
                    }
                }
            },
            "required": ["agentId", "toolId", "type"]
        }
    },
    "delete_agent_tool": {
        "method": "DELETE",
        "path": "/api/agents/{agentId}/tools/{toolId}",
        "description": "Delete a specific tool from an agent.",
        "input_schema": {
            "type": "object",
            "properties": {
                "agentId": {"type": "string", "description": "ID of the agent"},
                "toolId": {"type": "string", "description": "ID of the tool to delete"}
            },
            "required": ["agentId", "toolId"]
        }
    }
}
