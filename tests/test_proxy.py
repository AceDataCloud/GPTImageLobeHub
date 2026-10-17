from unittest.mock import AsyncMock

import pytest
from mcp.types import CallToolResult, TextContent, Tool

from gpt_image_lobehub import ALLOWED_TOOLS, focused_tools, proxy_call, validate_call


def tool(name):
    return Tool(name=name, inputSchema={"type": "object", "properties": {"model": {
        "type": "string", "enum": ["gpt-image-1", "gpt-image-2", "nano-banana", "dall-e-3"],
        "default": "gpt-image-1",
    }}})


def test_filters_unrelated_tools_and_models_without_mutating_dependency_schema():
    raw = [tool(name) for name in ALLOWED_TOOLS] + [tool("openai_chat_completion")]
    selected = focused_tools(raw)
    assert {entry.name for entry in selected} == ALLOWED_TOOLS
    image = next(entry for entry in selected if entry.name == "openai_generate_image")
    assert image.inputSchema["properties"]["model"]["enum"] == ["gpt-image-1", "gpt-image-2"]
    assert "default" not in image.inputSchema["properties"]["model"]
    assert "model" in image.inputSchema["required"]
    assert "nano-banana" in raw[0].inputSchema["properties"]["model"]["enum"]


@pytest.mark.parametrize("name,arguments", [
    ("openai_chat_completion", {}),
    ("openai_generate_image", {"model": "nano-banana"}),
    ("openai_edit_image", {"model": "dall-e-3"}),
    ("openai_edit_image", {}),
])
def test_rejects_other_services_without_silent_fallback(name, arguments):
    with pytest.raises(ValueError):
        validate_call(name, arguments)


def test_dependency_drift_fails_closed():
    with pytest.raises(ValueError):
        focused_tools([tool("openai_generate_image")])


@pytest.mark.asyncio
async def test_preserves_same_task_id_and_upstream_pending_or_error_result():
    result = CallToolResult(content=[TextContent(type="text", text="pending; keep same task ID")], isError=False)
    upstream = AsyncMock()
    upstream.call_tool.return_value = result
    assert await proxy_call(upstream, "openai_get_task", {"id": "existing-id"}) is result
    upstream.call_tool.assert_awaited_once_with("openai_get_task", {"id": "existing-id"})
    result.isError = True
    assert (await proxy_call(upstream, "openai_get_task", {"id": "existing-id"})).isError
