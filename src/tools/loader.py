import json
import os
import re
from typing import Any

import httpx
from mcp import types

from src.config import CHATVOLT_API_KEY, CHATVOLT_BASE_URL
from src.tools.definitions import TOOLS_DEFINITION

TOOL_ANNOTATIONS = {
    "query_agent": {
        "title": "Query Agent",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
    "get_agent": {
        "title": "Get Agent",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "create_agent": {
        "title": "Create Agent",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
    "update_agent": {
        "title": "Update Agent",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "delete_agent": {
        "title": "Delete Agent",
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "get_models": {
        "title": "Get Available Models",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
    "toggle_webhook": {
        "title": "Toggle Agent Webhook",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "get_agent_tools": {
        "title": "Get Agent Tools",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "create_agent_tool": {
        "title": "Create Agent Tool",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
    "update_agent_tool": {
        "title": "Update Agent Tool",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "delete_agent_tool": {
        "title": "Delete Agent Tool",
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "get_conversation_messages": {
        "title": "Get Conversation Messages",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "get_message": {
        "title": "Get Message",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "list_conversations": {
        "title": "List Conversations",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "get_conversation": {
        "title": "Get Conversation",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "set_conversation_ai": {
        "title": "Toggle Conversation AI",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "register_message_in_context": {
        "title": "Register Message in Context",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
    "search_artifacts": {
        "title": "Search Artifacts",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "list_artifacts": {
        "title": "List Artifacts",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "get_artifact": {
        "title": "Get Artifact",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "create_artifact": {
        "title": "Create Artifact",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
    "update_artifact": {
        "title": "Update Artifact",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "delete_artifact": {
        "title": "Delete Artifact",
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "list_artifact_categories": {
        "title": "List Artifact Categories",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "create_artifact_category": {
        "title": "Create Artifact Category",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
    "delete_artifact_category": {
        "title": "Delete Artifact Category",
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "get_artifact_category": {
        "title": "Get Artifact Category",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "update_artifact_category": {
        "title": "Update Artifact Category",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "list_artifact_media": {
        "title": "List Artifact Media",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "upload_artifact_media": {
        "title": "Upload Artifact Media",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
    "update_artifact_media": {
        "title": "Update Artifact Media",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "delete_artifact_media": {
        "title": "Delete Artifact Media",
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "list_datastores": {
        "title": "List Datastores",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "query_datastore": {
        "title": "Query Datastore",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "get_datastore": {
        "title": "Get Datastore",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "create_datastore": {
        "title": "Create Datastore",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
    "update_datastore": {
        "title": "Update Datastore",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "delete_datastore": {
        "title": "Delete Datastore",
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "list_datasources": {
        "title": "List Datasources",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "get_datasource": {
        "title": "Get Datasource",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "create_datasource": {
        "title": "Create Datasource",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
    "list_crm_scenarios": {
        "title": "List CRM Scenarios",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "list_crm_steps": {
        "title": "List CRM Steps",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "create_crm_step": {
        "title": "Create CRM Step",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
    "update_crm_step": {
        "title": "Update CRM Step",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "delete_crm_step": {
        "title": "Delete CRM Step",
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "add_conversation_to_step": {
        "title": "Add Conversation to CRM Step",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
    "move_conversation_to_step": {
        "title": "Move Conversation to CRM Step",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
    "list_contacts": {
        "title": "List Contacts",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "get_contact": {
        "title": "Get Contact",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "create_contact": {
        "title": "Create Contact",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
    "update_contact": {
        "title": "Update Contact",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "delete_contact": {
        "title": "Delete Contact",
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "get_contact_conversations": {
        "title": "Get Contact Conversations",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "list_dispatches": {
        "title": "List Dispatches",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "get_dispatch": {
        "title": "Get Dispatch",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "create_dispatch": {
        "title": "Create Dispatch",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
    "update_dispatch": {
        "title": "Update Dispatch",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "delete_dispatch": {
        "title": "Delete Dispatch",
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "list_blacklist": {
        "title": "List Blacklisted Users",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
    "add_to_blacklist": {
        "title": "Add to Blacklist",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
    "remove_from_blacklist": {
        "title": "Remove from Blacklist",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
}


def _make_annotations(name: str) -> types.ToolAnnotations | None:
    ann = TOOL_ANNOTATIONS.get(name)
    if not ann:
        return None
    return types.ToolAnnotations(
        title=ann.get("title"),
        readOnlyHint=ann.get("readOnlyHint"),
        destructiveHint=ann.get("destructiveHint"),
        idempotentHint=ann.get("idempotentHint"),
        openWorldHint=ann.get("openWorldHint"),
    )


def _structured_result(text: str, is_error: bool = False) -> list[types.TextContent | types.EmbeddedResource]:
    """Return both text and structured content for backwards compatibility."""
    return [types.TextContent(type="text", text=text)]


class ToolRegistry:
    def __init__(self):
        self.tools = TOOLS_DEFINITION

    def get_tool_list(self) -> list[types.Tool]:
        result = []
        for name, info in self.tools.items():
            result.append(
                types.Tool(
                    name=name,
                    description=info["description"],
                    inputSchema=info["input_schema"],
                    annotations=_make_annotations(name),
                )
            )
        return result

    async def call_tool(self, name: str, arguments: dict[str, Any]) -> list[types.TextContent | types.EmbeddedResource]:
        if name not in self.tools:
            return _structured_result(
                json.dumps({"error": True, "status": 404, "message": f"Tool {name} not found"}), is_error=True
            )

        tool_info = self.tools[name]
        method = tool_info["method"]
        path = tool_info["path"]

        args_copy = arguments.copy()

        # Replace path variables {id}
        path_vars = re.findall(r"\{(\w+)\}", path)
        for var in path_vars:
            if var in args_copy:
                path = path.replace(f"{{{var}}}", str(args_copy.pop(var)))

        query_params = {}
        json_body = {}

        # Special case for toggle_webhook query parameters
        if name == "toggle_webhook":
            if "type" in args_copy:
                query_params["type"] = args_copy.pop("type")
            if "enabled" in args_copy:
                query_params["enabled"] = str(args_copy.pop("enabled")).lower()

        # Special case for search_artifacts: convert lists to comma-separated strings
        if name == "search_artifacts":
            for key in ["ids", "categoryIds", "mediaTypes"]:
                if key in args_copy and isinstance(args_copy[key], list):
                    args_copy[key] = ",".join(map(str, args_copy[key]))

        if method == "GET":
            query_params.update(args_copy)
        else:
            json_body.update(args_copy)

        url = f"{CHATVOLT_BASE_URL}{path}"

        headers = {"Content-Type": "application/json"}
        # get_models doesn't need auth according to the request
        if name != "get_models":
            headers["Authorization"] = f"Bearer {CHATVOLT_API_KEY}"

        async with httpx.AsyncClient() as client:
            try:
                if name == "upload_artifact_media" or (name == "create_datasource" and arguments.get("type") == "file"):
                    file_path = arguments.get("file_path")
                    if not file_path or not os.path.exists(file_path):
                        return _structured_result(
                            json.dumps({"error": True, "status": 400, "message": f"File not found: {file_path}"}),
                            is_error=True,
                        )

                    with open(file_path, "rb") as f:
                        files = {
                            "file": (os.path.basename(file_path), f),
                        }

                        if name == "upload_artifact_media":
                            data = {
                                "artifact_id": arguments.get("artifact_id"),
                                "name": arguments.get("name"),
                                "alt_description": arguments.get("alt_description", ""),
                            }
                        else:  # create_datasource
                            data = {
                                "type": "file",
                                "datastoreId": arguments.get("datastoreId"),
                                "fileName": arguments.get("fileName") or os.path.basename(file_path),
                                "custom_id": arguments.get("custom_id", ""),
                            }

                        # Remove Content-Type from headers as httpx will set it with the boundary
                        headers.pop("Content-Type", None)

                        response = await client.post(
                            url,
                            headers=headers,
                            data=data,
                            files=files,
                            timeout=60.0,  # Increased timeout for uploads
                        )
                else:
                    response = await client.request(
                        method=method,
                        url=url,
                        headers=headers,
                        params=query_params,
                        json=json_body if json_body else None,
                        timeout=30.0,
                    )

                response.raise_for_status()
                return _structured_result(response.text)
            except httpx.HTTPStatusError as e:
                return _structured_result(
                    json.dumps({"error": True, "status": e.response.status_code, "message": e.response.text}),
                    is_error=True,
                )
            except Exception as e:
                return _structured_result(
                    json.dumps({"error": True, "status": 500, "message": str(e)}),
                    is_error=True,
                )


# Singleton instance
registry = ToolRegistry()
