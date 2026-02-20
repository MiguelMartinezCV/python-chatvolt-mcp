import contextlib
from collections.abc import AsyncIterator

from mcp.server import Server
import mcp.types as types
from src.tools.loader import registry
from src.prompts.workflows import PROMPTS, get_prompt_message
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager

from starlette.applications import Starlette
from starlette.routing import Route
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response

app = Server("chatvolt-mcp")

@app.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools."""
    return registry.get_tool_list()

@app.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool execution requests."""
    return await registry.call_tool(name, arguments or {})

@app.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    """List available prompts."""
    return list(PROMPTS.values())

@app.get_prompt()
async def handle_get_prompt(
    name: str, arguments: dict[str, str] | None
) -> types.GetPromptResult:
    """Get a specific prompt."""
    return get_prompt_message(name, arguments or {})


# StreamableHTTP with stateless=True and json_response=True:
# - stateless: no session tracking, each request is independent
# - json_response: returns JSON body directly (not SSE stream)
# This is what Gemini CLI (antigravity-client) expects.
session_manager = StreamableHTTPSessionManager(
    app=app,
    json_response=True,
    stateless=True,
)


@contextlib.asynccontextmanager
async def lifespan(starlette_app: Starlette) -> AsyncIterator[None]:
    async with session_manager.run():
        yield


class MCPApp:
    """
    Raw ASGI app for the /sse endpoint.
    Injects Accept header before delegating to StreamableHTTPSessionManager.
    """
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            headers = list(scope.get("headers", []))
            accept_values = [v for k, v in headers if k.lower() == b"accept"]
            needs_inject = (
                not accept_values
                or (
                    b"application/json" not in accept_values[0]
                    and b"text/event-stream" not in accept_values[0]
                )
            )
            if needs_inject:
                headers = [(k, v) for k, v in headers if k.lower() != b"accept"]
                headers.append((b"accept", b"application/json, text/event-stream"))
                scope = dict(scope)
                scope["headers"] = headers

        await session_manager.handle_request(scope, receive, send)


mcp_app = MCPApp()

starlette_app = Starlette(
    lifespan=lifespan,
    routes=[
        # Mount (not Route) so handle_mcp gets raw ASGI (scope, receive, send)
        # Route would wrap it in a Request object and cause a TypeError.
        # We strip trailing slashes manually in MCPApp so no 307 redirect occurs.
        # The MCP SDK's handle_request doesn't care about path.
        Route("/sse", endpoint=lambda req: None),  # placeholder for OpenAPI
    ],
    middleware=[
        Middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
    ]
)

# Override the ASGI app so all /sse traffic goes to mcp_app directly
_inner = starlette_app

class RootApp:
    """Routes /sse and /sse/ to MCPApp, everything else to Starlette."""
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            path = scope.get("path", "").rstrip("/")
            if path == "/sse":
                await mcp_app(scope, receive, send)
                return
        elif scope["type"] == "lifespan":
            await _inner(scope, receive, send)
            return
        await _inner(scope, receive, send)

starlette_app = RootApp()

