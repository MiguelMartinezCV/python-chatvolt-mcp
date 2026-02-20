import pytest
import respx
import httpx
from src.tools.loader import ToolRegistry
from mcp import types

@pytest.fixture
def registry():
    return ToolRegistry()

@pytest.mark.asyncio
@respx.mock
async def test_call_tool_not_found(registry):
    result = await registry.call_tool("nonexistent_tool", {})
    assert len(result) == 1
    assert "not found" in result[0].text

@pytest.mark.asyncio
@respx.mock
async def test_call_tool_get(registry):
    # Mock search_artifacts which is a GET request
    route = respx.get("https://api.chatvolt.ai/artifacts/search").respond(
        status_code=200, json={"results": []}
    )
    result = await registry.call_tool("search_artifacts", {"q": "test"})
    
    assert len(result) == 1
    import json
    parsed = json.loads(result[0].text)
    assert parsed == {"results": []}
    assert route.called
    assert route.calls.last.request.url.query == b"q=test"
    # Check authorization header
    assert "Bearer " in route.calls.last.request.headers.get("Authorization", "")

@pytest.mark.asyncio
@respx.mock
async def test_call_tool_post(registry):
    # Mock create_agent which is a POST request
    route = respx.post("https://api.chatvolt.ai/agents").respond(
        status_code=201, json={"id": "new_agent"}
    )
    result = await registry.call_tool("create_agent", {"name": "Test Agent"})
    
    assert len(result) == 1
    import json
    parsed = json.loads(result[0].text)
    assert parsed == {"id": "new_agent"}
    assert route.called
    
    body = json.loads(route.calls.last.request.content)
    assert body["name"] == "Test Agent"

@pytest.mark.asyncio
@respx.mock
async def test_call_tool_path_variables(registry):
    # Mock get_agent which has a path variable {id}
    route = respx.get("https://api.chatvolt.ai/agents/123").respond(
        status_code=200, json={"id": "123", "name": "Test Agent"}
    )
    result = await registry.call_tool("get_agent", {"id": "123"})
    
    assert len(result) == 1
    import json
    parsed = json.loads(result[0].text)
    assert parsed["id"] == "123"
    assert route.called

@pytest.mark.asyncio
@respx.mock
async def test_call_tool_http_error(registry):
    # Mock returning exactly 400 Bad Request
    route = respx.get("https://api.chatvolt.ai/artifacts/search").respond(
        status_code=400, text="Bad Request"
    )
    result = await registry.call_tool("search_artifacts", {"q": "test"})
    
    assert len(result) == 1
    assert "API Error: Bad Request" in result[0].text
    assert route.called
