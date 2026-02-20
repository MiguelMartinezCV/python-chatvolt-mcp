from typing import Dict, Any

TOOLS: Dict[str, Dict[str, Any]] = {
    "search_artifacts": {
        "method": "GET",
        "path": "/artifacts/search",
        "description": "Search for artifacts with advanced filters (name, description, price, categories, media types).",
        "input_schema": {
            "type": "object",
            "properties": {
                "q": {"type": "string", "description": "Search term for name, description, or category name"},
                "ids": {"type": "array", "items": {"type": "string"}, "description": "List of specific Artifact IDs. Overrides 'q' if provided."},
                "minPrice": {"type": "number", "description": "Minimum price filter"},
                "maxPrice": {"type": "number", "description": "Maximum price filter"},
                "categoryIds": {"type": "array", "items": {"type": "string"}, "description": "List of category IDs (includes sub-categories)"},
                "mediaTypes": {
                    "type": "array",
                    "items": {"type": "string", "enum": ["IMAGE", "VIDEO", "AUDIO", "DOCUMENT", "OTHER"]},
                    "description": "Filter by media types"
                },
                "maxMedias": {"type": "integer", "default": 10},
                "includeInactive": {"type": "boolean", "default": False},
                "limit": {"type": "integer", "default": 20},
                "page": {"type": "integer", "default": 1}
            }
        }
    },
    "list_artifacts": {
        "method": "GET",
        "path": "/artifacts",
        "description": "List all artifacts for the organization with basic filtering.",
        "input_schema": {
            "type": "object",
            "properties": {
                "categoryId": {"type": "string", "description": "Filter by category ID"},
                "name": {"type": "string", "description": "Filter by exact name match"},
                "search": {"type": "string", "description": "General search string (name, description, id)"}
            }
        }
    },
    "create_artifact": {
        "method": "POST",
        "path": "/artifacts",
        "description": "Create a new artifact (product or service).",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "description": {"type": "string"},
                "price": {"type": "number"},
                "externalUrl": {"type": "string"},
                "customJson": {"type": "object"},
                "categoryId": {"type": "string"},
                "isActive": {"type": "boolean"}
            },
            "required": ["name", "categoryId"]
        }
    },
    "get_artifact": {
        "method": "GET",
        "path": "/artifacts/{id}",
        "description": "Retrieve details of a specific artifact by its id.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID of the artifact"}
            },
            "required": ["id"]
        }
    },
    "update_artifact": {
        "method": "PUT",
        "path": "/artifacts/{id}",
        "description": "Update an existing artifact.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID of the artifact to update"},
                "name": {"type": "string"},
                "description": {"type": "string"},
                "price": {"type": "number"},
                "externalUrl": {"type": "string"},
                "customJson": {"type": "object"},
                "categoryId": {"type": "string"},
                "isActive": {"type": "boolean"}
            },
            "required": ["id"]
        }
    },
    "list_artifact_media": {
        "method": "GET",
        "path": "/artifacts/media",
        "description": "List all media associated with a specific artifact.",
        "input_schema": {
            "type": "object",
            "properties": {
                "artifact_id": {"type": "string", "description": "ID of the artifact to list media for"},
                "q": {"type": "string", "description": "Search by name or alt description"},
                "type": {"type": "string", "enum": ["IMAGE", "VIDEO", "AUDIO", "DOCUMENT", "OTHER", "all"], "description": "Filter by media type"}
            },
            "required": ["artifact_id"]
        }
    },
    "upload_artifact_media": {
        "method": "POST",
        "path": "/artifacts/media/upload",
        "description": "Upload a media file (image, video, etc.) for a specific artifact.",
        "input_schema": {
            "type": "object",
            "properties": {
                "artifact_id": {"type": "string", "description": "ID of the artifact"},
                "name": {"type": "string", "description": "Name for the media file"},
                "alt_description": {"type": "string", "description": "Alt text/description for accessibility"},
                "file_path": {"type": "string", "description": "Absolute path to the local file to upload"}
            },
            "required": ["artifact_id", "name", "file_path"]
        }
    },
    "update_artifact_media": {
        "method": "PATCH",
        "path": "/artifacts/media/{id}",
        "description": "Update details of an existing media item.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID of the media item"},
                "name": {"type": "string"},
                "altDescription": {"type": "string"},
                "isActive": {"type": "boolean"}
            },
            "required": ["id"]
        }
    },
    "delete_artifact_media": {
        "method": "DELETE",
        "path": "/artifacts/media/{id}",
        "description": "Delete a specific media item from an artifact.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID of the media item to delete"}
            },
            "required": ["id"]
        }
    },
    "list_artifact_categories": {
        "method": "GET",
        "path": "/artifact-categories",
        "description": "List all artifact categories.",
        "input_schema": {
            "type": "object",
            "properties": {}
        }
    },
    "create_artifact_category": {
        "method": "POST",
        "path": "/artifact-categories",
        "description": "Create a new category for artifacts.",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Name of the category"},
                "description": {"type": "string", "description": "Description of the category"},
                "parentId": {"type": "string", "description": "Optional parent category ID"}
            },
            "required": ["name"]
        }
    },
    "get_artifact_category": {
        "method": "GET",
        "path": "/artifact-categories/{id}",
        "description": "Retrieve details of a specific artifact category.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID of the category"}
            },
            "required": ["id"]
        }
    },
    "update_artifact_category": {
        "method": "PUT",
        "path": "/artifact-categories/{id}",
        "description": "Update an existing artifact category.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID of the category to update"},
                "name": {"type": "string"},
                "description": {"type": "string"},
                "parentId": {"type": "string"},
                "isActive": {"type": "boolean"}
            },
            "required": ["id"]
        }
    },
    "delete_artifact_category": {
        "method": "DELETE",
        "path": "/artifact-categories/{id}",
        "description": "Delete a specific artifact category.",
        "input_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "ID of the category to delete"}
            },
            "required": ["id"]
        }
    }
}
