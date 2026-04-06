import json

import pytest
import respx

from src.server import handle_list_resources, handle_list_tools, handle_read_resource
from src.tools.loader import ToolRegistry


@pytest.fixture
def registry():
    return ToolRegistry()


class TestToolAnnotations:
    @pytest.mark.asyncio
    async def test_all_tools_have_annotations(self):
        tools = await handle_list_tools()
        for tool in tools:
            assert tool.annotations is not None, f"Tool {tool.name} missing annotations"
            assert tool.annotations.title is not None, f"Tool {tool.name} missing title"

    @pytest.mark.asyncio
    async def test_readonly_tools_have_correct_annotations(self):
        tools = await handle_list_tools()
        for tool in tools:
            if tool.name.startswith(("list_", "get_", "search_")):
                assert tool.annotations.readOnlyHint is True, f"{tool.name} should be readOnlyHint=True"
        # query_agent is NOT read-only (it sends data to an agent)
        query_tool = next(t for t in tools if t.name == "query_agent")
        assert query_tool.annotations.readOnlyHint is False

    @pytest.mark.asyncio
    async def test_destructive_tools_have_correct_annotations(self):
        tools = await handle_list_tools()
        for tool in tools:
            if tool.name.startswith("delete_"):
                assert tool.annotations.destructiveHint is True, f"{tool.name} should be destructiveHint=True"


class TestResources:
    @pytest.mark.asyncio
    async def test_list_resources(self):
        resources = await handle_list_resources()
        assert len(resources) > 0
        uris = [str(r.uri) for r in resources]
        assert "chatvolt://models" in uris
        assert "chatvolt://tools" in uris
        assert "chatvolt://prompts" in uris

    @pytest.mark.asyncio
    async def test_read_models_resource(self):
        result = await handle_read_resource("chatvolt://models")
        parsed = json.loads(result)
        assert "note" in parsed

    @pytest.mark.asyncio
    async def test_read_tools_resource(self):
        result = await handle_read_resource("chatvolt://tools")
        parsed = json.loads(result)
        assert isinstance(parsed, dict)
        assert "query_agent" in parsed
        assert "method" in parsed["query_agent"]
        assert "path" in parsed["query_agent"]

    @pytest.mark.asyncio
    async def test_read_prompts_resource(self):
        result = await handle_read_resource("chatvolt://prompts")
        parsed = json.loads(result)
        assert isinstance(parsed, dict)
        assert "create_new_agent" in parsed

    @pytest.mark.asyncio
    async def test_read_unknown_resource(self):
        with pytest.raises(ValueError):
            await handle_read_resource("chatvolt://unknown")


class TestNewTools:
    @pytest.mark.asyncio
    async def test_delete_agent_exists(self):
        tools = await handle_list_tools()
        names = [t.name for t in tools]
        assert "delete_agent" in names

    @pytest.mark.asyncio
    async def test_contacts_tools_exist(self):
        tools = await handle_list_tools()
        names = [t.name for t in tools]
        for name in [
            "list_contacts",
            "get_contact",
            "create_contact",
            "update_contact",
            "delete_contact",
            "get_contact_conversations",
        ]:
            assert name in names, f"Missing contact tool: {name}"

    @pytest.mark.asyncio
    async def test_dispatches_tools_exist(self):
        tools = await handle_list_tools()
        names = [t.name for t in tools]
        for name in ["list_dispatches", "get_dispatch", "create_dispatch", "update_dispatch", "delete_dispatch"]:
            assert name in names, f"Missing dispatch tool: {name}"

    @pytest.mark.asyncio
    async def test_blacklist_tools_exist(self):
        tools = await handle_list_tools()
        names = [t.name for t in tools]
        for name in ["list_blacklist", "add_to_blacklist", "remove_from_blacklist"]:
            assert name in names, f"Missing blacklist tool: {name}"

    @pytest.mark.asyncio
    async def test_artifact_tools_complete(self):
        tools = await handle_list_tools()
        names = [t.name for t in tools]
        assert "delete_artifact" in names, "Missing delete_artifact tool"


class TestNewToolCalls:
    @pytest.mark.asyncio
    @respx.mock
    async def test_delete_agent(self, registry):
        route = respx.delete("https://api.chatvolt.ai/agents/123").respond(status_code=200, json={"deleted": True})
        result = await registry.call_tool("delete_agent", {"id": "123"})
        assert len(result) == 1
        parsed = json.loads(result[0].text)
        assert parsed == {"deleted": True}
        assert route.called

    @pytest.mark.asyncio
    @respx.mock
    async def test_delete_artifact(self, registry):
        route = respx.delete("https://api.chatvolt.ai/artifacts/art_123").respond(
            status_code=200, json={"deleted": True}
        )
        result = await registry.call_tool("delete_artifact", {"id": "art_123"})
        assert len(result) == 1
        parsed = json.loads(result[0].text)
        assert parsed == {"deleted": True}
        assert route.called

    @pytest.mark.asyncio
    @respx.mock
    async def test_list_contacts(self, registry):
        route = respx.get("https://api.chatvolt.ai/contacts").respond(status_code=200, json={"contacts": []})
        result = await registry.call_tool("list_contacts", {})
        assert len(result) == 1
        parsed = json.loads(result[0].text)
        assert parsed == {"contacts": []}
        assert route.called

    @pytest.mark.asyncio
    @respx.mock
    async def test_create_contact(self, registry):
        route = respx.post("https://api.chatvolt.ai/contacts").respond(status_code=201, json={"id": "c1"})
        result = await registry.call_tool("create_contact", {"firstName": "John", "phoneNumber": "5511999999999"})
        assert len(result) == 1
        parsed = json.loads(result[0].text)
        assert parsed == {"id": "c1"}
        assert route.called
        body = json.loads(route.calls.last.request.content)
        assert body["firstName"] == "John"

    @pytest.mark.asyncio
    @respx.mock
    async def test_list_dispatches(self, registry):
        route = respx.get("https://api.chatvolt.ai/dispatches").respond(status_code=200, json={"dispatches": []})
        result = await registry.call_tool("list_dispatches", {})
        assert len(result) == 1
        parsed = json.loads(result[0].text)
        assert parsed == {"dispatches": []}
        assert route.called

    @pytest.mark.asyncio
    @respx.mock
    async def test_create_dispatch(self, registry):
        route = respx.post("https://api.chatvolt.ai/dispatches").respond(status_code=201, json={"id": "d1"})
        result = await registry.call_tool("create_dispatch", {"name": "Test", "agentId": "a1", "message": "Hello"})
        assert len(result) == 1
        parsed = json.loads(result[0].text)
        assert parsed == {"id": "d1"}
        assert route.called

    @pytest.mark.asyncio
    @respx.mock
    async def test_list_blacklist(self, registry):
        route = respx.get("https://api.chatvolt.ai/agents/a1/blacklist").respond(
            status_code=200, json={"blacklist": []}
        )
        result = await registry.call_tool("list_blacklist", {"agentId": "a1"})
        assert len(result) == 1
        parsed = json.loads(result[0].text)
        assert parsed == {"blacklist": []}
        assert route.called


class TestStructuredErrors:
    @pytest.mark.asyncio
    async def test_not_found_returns_structured_error(self, registry):
        result = await registry.call_tool("nonexistent", {})
        parsed = json.loads(result[0].text)
        assert parsed["error"] is True
        assert parsed["status"] == 404
        assert "message" in parsed

    @pytest.mark.asyncio
    @respx.mock
    async def test_http_error_returns_structured_error(self, registry):
        respx.get("https://api.chatvolt.ai/artifacts/search").respond(status_code=500, text="Server Error")
        result = await registry.call_tool("search_artifacts", {"q": "test"})
        parsed = json.loads(result[0].text)
        assert parsed["error"] is True
        assert parsed["status"] == 500
        assert "message" in parsed

    @pytest.mark.asyncio
    async def test_file_not_found_returns_structured_error(self, registry):
        result = await registry.call_tool(
            "upload_artifact_media", {"file_path": "/nonexistent/file.txt", "artifact_id": "a1"}
        )
        parsed = json.loads(result[0].text)
        assert parsed["error"] is True
        assert parsed["status"] == 400
