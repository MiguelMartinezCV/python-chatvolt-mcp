from typing import Dict, Any

TOOLS: Dict[str, Dict[str, Any]] = {
    "list_datastores": {
        "method": "GET",
        "path": "/datastores/list",
        "description": "Retrieves a paginated list of all datastores belonging to the organization.",
        "input_schema": {
            "type": "object",
            "properties": {
                "offset": {"type": "integer", "default": 0, "description": "Number of items to skip"},
                "limit": {"type": "integer", "default": 20, "description": "Maximum number of items to return"}
            }
        }
    },
    "query_datastore": {
        "method": "POST",
        "path": "/datastores/{id}/query",
        "description": "Query a specific datastore for information.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID of the datastore"},
                "query": {"type": "string", "description": "The question or query for the datastore"},
                "topK": {"type": "number", "description": "Number of results to return"},
                "filters": {
                    "type": "object",
                    "properties": {
                        "custom_ids": {"type": "array", "items": {"type": "string"}},
                        "datasource_ids": {"type": "array", "items": {"type": "string"}}
                    }
                }
            },
            "required": ["id", "query"]
        }
    },
    "get_datastore": {
        "method": "GET",
        "path": "/datastores/{id}",
        "description": "Retrieve details of a specific datastore, including its datasources.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID of the datastore"},
                "search": {"type": "string", "description": "Search datasources by name (optional)"},
                "status": {"type": "string", "enum": ["unsynched", "pending", "running", "synched", "error", "usage_limit_reached"], "description": "Filter datasources by status (optional)"},
                "type": {"type": "string", "enum": ["file", "web_page", "web_site", "qa"], "description": "Filter datasources by type (optional)"},
                "offset": {"type": "integer", "default": 0, "description": "Datasource pagination offset (optional)"},
                "limit": {"type": "integer", "default": 100, "description": "Datasource pagination limit (optional)"},
                "groupId": {"type": "string", "description": "Filter datasources by group ID (optional)"}
            },
            "required": ["id"]
        }
    },
    "create_datastore": {
        "method": "POST",
        "path": "/datastores",
        "description": "Create a new datastore with the provided configurations.",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Datastore name (optional)"},
                "description": {"type": "string", "description": "Datastore description"},
                "type": {"type": "string", "enum": ["qdrant"], "description": "Datastore type (e.g., 'qdrant')"},
                "isPublic": {"type": "boolean", "default": False, "description": "Whether the datastore is public"},
                "pluginName": {"type": "string", "description": "Short name for the OpenAI plugin (max 20 chars)"},
                "pluginDescriptionForHumans": {"type": "string", "description": "Description for the OpenAI plugin (max 90 chars)"}
            },
            "required": ["type"]
        }
    },
    "update_datastore": {
        "method": "PATCH",
        "path": "/datastores/{id}",
        "description": "Update an existing datastore's configuration.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID of the datastore to update"},
                "name": {"type": "string"},
                "description": {"type": "string"},
                "type": {"type": "string", "enum": ["qdrant"]},
                "isPublic": {"type": "boolean"},
                "pluginName": {"type": "string", "description": "Short name for the OpenAI plugin (max 20 chars)"},
                "pluginDescriptionForHumans": {"type": "string", "description": "Description for the OpenAI plugin (max 90 chars)"}
            },
            "required": ["id"]
        }
    },
    "delete_datastore": {
        "method": "DELETE",
        "path": "/datastores/{id}",
        "description": "Permanently delete a datastore and all its associated data.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID of the datastore to delete"}
            },
            "required": ["id"]
        }
    },
    "list_datasources": {
        "method": "GET",
        "path": "/datasources/list",
        "description": "Retrieves a paginated list of all datasources belonging to a specific datastore.",
        "input_schema": {
            "type": "object",
            "properties": {
                "datastoreId": {"type": "string", "description": "ID of the datastore to list datasources from"},
                "offset": {"type": "integer", "default": 0, "description": "Number of items to skip"},
                "limit": {"type": "integer", "default": 20, "description": "Maximum number of items to return"}
            },
            "required": ["datastoreId"]
        }
    },
    "get_datasource": {
        "method": "GET",
        "path": "/datasources/{id}",
        "description": "Retrieves details of a specific datasource by its ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID of the datasource to retrieve"},
                "idstore": {"type": "string", "description": "ID of the datastore to which the datasource belongs"}
            },
            "required": ["id", "idstore"]
        }
    },
    "create_datasource": {
        "method": "POST",
        "path": "/datasources",
        "description": "Create a new datasource. Supports 'file' upload (multipart/form-data) or 'web_page', 'web_site', 'qa' (JSON).",
        "input_schema": {
            "type": "object",
            "properties": {
                "datastoreId": {"type": "string", "description": "ID of the datastore"},
                "type": {"type": "string", "enum": ["file", "web_page", "web_site", "qa"], "description": "The type of datasource"},
                "name": {"type": "string", "description": "Name for the datasource (optional for files)"},
                "file_path": {"type": "string", "description": "Absolute path to a local file (required if type is 'file')"},
                "fileName": {"type": "string", "description": "Optional name for the uploaded file"},
                "datasourceText": {"type": "string", "description": "Textual content (for 'file' or 'qa' if isUpdateText is true)"},
                "isUpdateText": {"type": "boolean"},
                "custom_id": {"type": "string", "description": "Optional custom ID"},
                "config": {
                    "type": "object",
                    "properties": {
                        "source_url": {"type": "string", "format": "url"},
                        "sitemap": {"type": "string", "format": "url"},
                        "tags": {"type": "array", "items": {"type": "string"}},
                        "question": {"type": "string"},
                        "answer": {"type": "string"}
                    }
                }
            },
            "required": ["datastoreId", "type"]
        }
    }
}
