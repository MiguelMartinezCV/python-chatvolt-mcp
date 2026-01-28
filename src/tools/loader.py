import os
import yaml
import httpx
from typing import Dict, Any, List
from mcp import types
from src.config import CHATVOLT_API_KEY, CHATVOLT_BASE_URL

class ToolRegistry:
    def __init__(self, specs_dir: str):
        self.specs_dir = specs_dir
        self.tools: Dict[str, Dict[str, Any]] = {}
        self.load_specs()

    def load_specs(self):
        for filename in os.listdir(self.specs_dir):
            if filename.endswith(".yaml"):
                service_name = filename.replace(".yaml", "")
                with open(os.path.join(self.specs_dir, filename), 'r') as f:
                    spec = yaml.safe_load(f)
                    self.parse_spec(service_name, spec)

    def parse_spec(self, service: str, spec: Dict[str, Any]):
        paths = spec.get("paths")
        if not paths:
            return
        for path, methods in paths.items():
            for method, details in methods.items():
                if method.lower() not in ["get", "post", "put", "delete", "patch"]:
                    continue
                
                operation_id = details.get("operationId")
                summary = details.get("summary", "")
                description = details.get("description", summary)
                
                # Create a unique name for the tool
                # e.g., contacts_get_contacts
                clean_path = path.strip("/").replace("/", "_").replace("{", "").replace("}", "")
                tool_name = f"{service}_{method}_{clean_path}"
                if operation_id:
                   # Optionally use operation_id if available and clean
                   pass

                # Build input schema
                properties = {}
                required = []

                # Path parameters
                parameters = details.get("parameters", [])
                for param in parameters:
                    p_name = param.get("name")
                    p_schema = param.get("schema", {"type": "string"})
                    properties[p_name] = {
                        "type": p_schema.get("type", "string"),
                        "description": param.get("description", "")
                    }
                    if param.get("required"):
                        required.append(p_name)

                # Request body
                request_body = details.get("requestBody", {})
                content = request_body.get("content", {})
                json_content = content.get("application/json", {})
                body_schema = json_content.get("schema", {})
                
                if body_schema.get("type") == "object":
                    body_props = body_schema.get("properties", {})
                    for p_name, p_val in body_props.items():
                        properties[p_name] = p_val
                    required.extend(body_schema.get("required", []))

                self.tools[tool_name] = {
                    "service": service,
                    "method": method.upper(),
                    "path": path,
                    "description": description,
                    "input_schema": {
                        "type": "object",
                        "properties": properties,
                        "required": list(set(required))
                    },
                    "original_spec": details
                }

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
        
        # Replace path variables
        for key, value in arguments.items():
            if f"{{{key}}}" in path:
                path = path.replace(f"{{{key}}}", str(value))
        
        url = f"{CHATVOLT_BASE_URL}{path}"
        
        headers = {
            "Authorization": f"Bearer {CHATVOLT_API_KEY}",
            "Content-Type": "application/json"
        }

        # Separate arguments into path, query, and body
        # For simplicity, we'll try to be smart about where they go
        # If it's a GET, put everything in query. If it's POST/PUT/PATCH, put what's not in path in body.
        
        query_params = {}
        json_body = {}
        
        # Check spec for where params should go
        params_spec = tool_info["original_spec"].get("parameters", [])
        path_param_names = [p["name"] for p in params_spec if p.get("in") == "path"]
        query_param_names = [p["name"] for p in params_spec if p.get("in") == "query"]
        
        for key, value in arguments.items():
            if key in path_param_names:
                continue # Already handled in path replacement
            elif key in query_param_names:
                query_params[key] = value
            else:
                if method in ["POST", "PUT", "PATCH"]:
                    json_body[key] = value
                else:
                    query_params[key] = value

        async with httpx.AsyncClient() as client:
            try:
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
registry = ToolRegistry("specs")
