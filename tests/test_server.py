import pytest

from src.server import LOG_LEVELS, handle_list_prompts, handle_list_tools, handle_set_logging_level


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


@pytest.mark.asyncio
async def test_set_logging_level_valid():
    """Test setting valid log levels."""
    for level in LOG_LEVELS:
        result = await handle_set_logging_level(level)
        assert result is not None


@pytest.mark.asyncio
async def test_set_logging_level_invalid():
    """Test that invalid log levels raise ValueError."""
    with pytest.raises(ValueError):
        await handle_set_logging_level("invalid_level")

    with pytest.raises(ValueError):
        await handle_set_logging_level("")

    with pytest.raises(ValueError):
        await handle_set_logging_level("DEBUG")
