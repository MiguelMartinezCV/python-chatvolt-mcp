import pytest
from src.server import handle_list_tools, handle_call_tool, handle_list_prompts

@pytest.mark.asyncio
async def test_server_tools_list():
    tools = await handle_list_tools()
    # The tools list should contain tools from our registry
    assert len(tools) > 0
    names = [t.name for t in tools]
    assert "query_agent" in names

@pytest.mark.asyncio
async def test_server_prompts_list():
    prompts = await handle_list_prompts()
    # We should have prompts available
    assert len(prompts) > 0
    names = [p.name for p in prompts]
    assert "create_new_agent" in names

