from mcp.server import Server
import mcp.types as types
from src.tools.loader import registry
from src.prompts.workflows import PROMPTS, get_prompt_message
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from mcp.server.sse import SseServerTransport
import asyncio

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

sse = SseServerTransport("/messages")

async def handle_sse(request):
    async with sse.connect_sse(request.scope, request.receive, request._send) as streams:
        await app.run(
            streams[0],
            streams[1],
            app.create_initialization_options()
        )

starlette_app = Starlette(
    routes=[
        Route("/sse", endpoint=handle_sse),
        Mount("/messages", app=sse.handle_post_message),
    ]
)
