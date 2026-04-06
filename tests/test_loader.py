import json

import pytest
import respx

from src.tools.loader import ToolRegistry


@pytest.fixture
def registry():
    return ToolRegistry()


@pytest.mark.asyncio
@respx.mock
async def test_call_tool_not_found(registry):
    result = await registry.call_tool("nonexistent_tool", {})
    assert len(result) == 1
    parsed = json.loads(result[0].text)
    assert parsed["error"] is True
    assert parsed["status"] == 404
    assert "not found" in parsed["message"]


@pytest.mark.asyncio
@respx.mock
async def test_call_tool_get(registry):
    route = respx.get("https://api.chatvolt.ai/artifacts/search").respond(status_code=200, json={"results": []})
    result = await registry.call_tool("search_artifacts", {"q": "test"})

    assert len(result) == 1
    parsed = json.loads(result[0].text)
    assert parsed == {"results": []}
    assert route.called
    assert route.calls.last.request.url.query == b"q=test"
    assert "Bearer " in route.calls.last.request.headers.get("Authorization", "")


@pytest.mark.asyncio
@respx.mock
async def test_call_tool_post(registry):
    route = respx.post("https://api.chatvolt.ai/agents").respond(status_code=201, json={"id": "new_agent"})
    result = await registry.call_tool("create_agent", {"name": "Test Agent"})

    assert len(result) == 1
    parsed = json.loads(result[0].text)
    assert parsed == {"id": "new_agent"}
    assert route.called

    body = json.loads(route.calls.last.request.content)
    assert body["name"] == "Test Agent"


@pytest.mark.asyncio
@respx.mock
async def test_call_tool_path_variables(registry):
    route = respx.get("https://api.chatvolt.ai/agents/123").respond(
        status_code=200, json={"id": "123", "name": "Test Agent"}
    )
    result = await registry.call_tool("get_agent", {"id": "123"})

    assert len(result) == 1
    parsed = json.loads(result[0].text)
    assert parsed["id"] == "123"
    assert route.called


@pytest.mark.asyncio
@respx.mock
async def test_call_tool_http_error(registry):
    route = respx.get("https://api.chatvolt.ai/artifacts/search").respond(status_code=400, text="Bad Request")
    result = await registry.call_tool("search_artifacts", {"q": "test"})

    assert len(result) == 1
    parsed = json.loads(result[0].text)
    assert parsed["error"] is True
    assert parsed["status"] == 400
    assert parsed["message"] == "Bad Request"
    assert route.called
