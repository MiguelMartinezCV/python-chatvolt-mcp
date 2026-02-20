import httpx
import re
import os
from typing import Dict, Any, List
from src.tools.definitions import TOOLS_DEFINITION
from mcp import types
from src.config import CHATVOLT_API_KEY, CHATVOLT_BASE_URL

class ToolRegistry:
    def __init__(self):
        self.tools = TOOLS_DEFINITION

    def get_tool_list(self) -> List[types.Tool]:
        return [
            types.Tool(
                name=name,
                description=info["description"],
                inputSchema=info["input_schema"]
            )
            for name, info in self.tools.items()
        ]

    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
        if name not in self.tools:
            return [types.TextContent(type="text", text=f"Tool {name} not found")]

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
        
        headers = {
            "Content-Type": "application/json"
        }
        # get_models doesn't need auth according to the request
        if name != "get_models":
            headers["Authorization"] = f"Bearer {CHATVOLT_API_KEY}"

        async with httpx.AsyncClient() as client:
            try:
                if name == "upload_artifact_media" or (name == "create_datasource" and arguments.get("type") == "file"):
                    file_path = arguments.get("file_path")
                    if not file_path or not os.path.exists(file_path):
                        return [types.TextContent(type="text", text=f"File not found: {file_path}")]
                    
                    files = {
                        "file": (os.path.basename(file_path), open(file_path, "rb"))
                    }
                    
                    if name == "upload_artifact_media":
                        data = {
                            "artifact_id": arguments.get("artifact_id"),
                            "name": arguments.get("name"),
                            "alt_description": arguments.get("alt_description", "")
                        }
                    else: # create_datasource
                        data = {
                            "type": "file",
                            "datastoreId": arguments.get("datastoreId"),
                            "fileName": arguments.get("fileName") or os.path.basename(file_path),
                            "custom_id": arguments.get("custom_id", "")
                        }
                        
                    # Remove Content-Type from headers as httpx will set it with the boundary
                    headers.pop("Content-Type", None)
                    
                    response = await client.post(
                        url,
                        headers=headers,
                        data=data,
                        files=files,
                        timeout=60.0 # Increased timeout for uploads
                    )
                else:
                    response = await client.request(
                        method=method,
                        url=url,
                        headers=headers,
                        params=query_params,
                        json=json_body if json_body else None,
                        timeout=30.0
                    )
                
                response.raise_for_status()
                return [types.TextContent(type="text", text=response.text)]
            except httpx.HTTPStatusError as e:
                return [types.TextContent(type="text", text=f"API Error: {e.response.text}")]
            except Exception as e:
                return [types.TextContent(type="text", text=f"Error: {str(e)}")]

# Singleton instance
registry = ToolRegistry()
