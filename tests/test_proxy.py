"""Consumer compatibility and isolation checks for the real shared profile."""

import json
import os
import sys
import subprocess
from unittest.mock import AsyncMock

import httpx
import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from gpt_image_lobehub import launch_configuration, main

EXPECTED_TOOLS = {
    "gpt_image_generate", "gpt_image_edit", "gpt_image_get_task",
    "gpt_image_list_tasks", "gpt_image_list_models",
}


def test_launch_fixes_profile_and_strips_ambient_secrets(monkeypatch):
    monkeypatch.setattr("gpt_image_lobehub.shutil.which", lambda _: "/venv/bin/mcp-openai-pro")
    command, arguments, environment = launch_configuration({
        "PATH": "/venv/bin", "ACEDATACLOUD_API_TOKEN": "dummy",
        "OPENAI_REQUEST_TIMEOUT": "9", "PYPI_TOKEN": "must-not-inherit",
        "PYTHONPATH": "/untrusted", "PYTHON_DOTENV_DISABLED": "0",
    })
    assert command == arguments[0]
    assert arguments[1:] == ["--profile", "gpt-image", "--transport", "stdio"]
    assert environment == {"PATH": "/venv/bin", "ACEDATACLOUD_API_TOKEN": "dummy",
                           "OPENAI_REQUEST_TIMEOUT": "9", "PYTHON_DOTENV_DISABLED": "1"}


def test_missing_connector_key_fails_before_starting(monkeypatch):
    monkeypatch.setattr("gpt_image_lobehub.shutil.which", lambda _: "/bin/mcp-openai-pro")
    with pytest.raises(RuntimeError, match="ACEDATACLOUD_API_TOKEN"):
        launch_configuration({})


def test_profile_override_is_rejected(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["gpt-image-lobehub", "--profile", "all"])
    with pytest.raises(SystemExit) as raised:
        main()
    assert raised.value.code == 2


@pytest.fixture
def shared_server(monkeypatch):
    monkeypatch.setenv("ACEDATACLOUD_API_TOKEN", "dummy-local-tests")
    monkeypatch.setenv("ACEDATACLOUD_API_BASE_URL", "http://127.0.0.1:9")
    monkeypatch.setenv("PYTHON_DOTENV_DISABLED", "1")
    from gpt_image_tools import create_server
    return create_server()


@pytest.mark.asyncio
async def test_actual_shared_profile_has_five_tools_and_explicit_image_models(shared_server):
    tools = await shared_server.list_tools()
    assert {tool.name for tool in tools} == EXPECTED_TOOLS
    for tool in tools:
        if tool.name in {"gpt_image_generate", "gpt_image_edit"}:
            schema = tool.inputSchema
            assert "model" in schema["required"]
            assert "default" not in schema["properties"]["model"]
            assert all(value.startswith("gpt-image-") and ":reverse" not in value
                       for value in schema["properties"]["model"]["enum"])


@pytest.mark.parametrize("status", [401, 403, 429, 500])
@pytest.mark.asyncio
async def test_real_profile_keeps_safe_shared_error_metadata(shared_server, monkeypatch, status):
    from core.exceptions import OpenAIAPIError
    from gpt_image_tools import GPT_IMAGE_MODELS
    from tools.image_tools import client
    raw = "secret sk-sensitive https://internal.invalid/supplier"
    request = AsyncMock(side_effect=OpenAIAPIError(raw, code="supplier_internal", status_code=status,
                                                request_id="request-123"))
    monkeypatch.setattr(client, "images_generations_async", request)
    content, structured = await shared_server.call_tool("gpt_image_generate", {
        "prompt": "local mock only", "model": GPT_IMAGE_MODELS[0],
    })
    result = json.loads(content[0].text)
    assert result["status_code"] == status
    assert result["request_id"] == "request-123"
    assert raw not in content[0].text and "supplier_internal" not in content[0].text
    assert structured["result"] == content[0].text
    request.assert_awaited_once()


@pytest.mark.asyncio
async def test_real_profile_network_error_has_no_fabricated_http_status(shared_server, monkeypatch):
    from tools.tasks_tools import client
    request = AsyncMock(side_effect=httpx.ConnectError("private diagnostic"))
    monkeypatch.setattr(client, "tasks", request)
    content, _ = await shared_server.call_tool("gpt_image_get_task", {"id": "same-test-id"})
    result = json.loads(content[0].text)
    assert result["status_code"] is None and result["code"] == "network_error"
    assert "private diagnostic" not in content[0].text
    request.assert_awaited_once_with(action="retrieve", id="same-test-id")


@pytest.mark.asyncio
async def test_installed_launcher_real_stdio_information_only():
    env = {key: value for key, value in os.environ.items() if key in {"PATH", "HOME", "LANG", "TMPDIR"}}
    env.update(ACEDATACLOUD_API_TOKEN="dummy-info-only", ACEDATACLOUD_API_BASE_URL="http://127.0.0.1:9",
               PYTHON_DOTENV_DISABLED="1")
    async with stdio_client(StdioServerParameters(command="gpt-image-lobehub", env=env)) as (read, write):
        async with ClientSession(read, write) as session:
            initialized = await session.initialize()
            assert initialized.serverInfo.name == "GPT Image by Ace Data Cloud"
            assert {tool.name for tool in (await session.list_tools()).tools} == EXPECTED_TOOLS
            result = await session.call_tool("gpt_image_list_models", {})
            assert not result.isError
            models = json.loads(result.content[0].text)["models"]
            assert models and all(value.startswith("gpt-image-") for value in models)


def test_supported_dotenv_really_ignores_project_file(tmp_path):
    (tmp_path / ".env").write_text("ACEDATACLOUD_API_BASE_URL=http://127.0.0.1:1\nUNTRUSTED_DOTENV_VALUE=must-not-load\n")
    _, _, environment = launch_configuration({"PATH": os.environ["PATH"],
                                              "ACEDATACLOUD_API_TOKEN": "dummy-test"})
    result = subprocess.check_output([
        sys.executable, "-c",
        "from dotenv import load_dotenv; import os; load_dotenv('.env'); "
        "print(os.getenv('UNTRUSTED_DOTENV_VALUE', 'unset')); "
        "print(os.getenv('ACEDATACLOUD_API_BASE_URL', 'unset'))",
    ], cwd=tmp_path, env=environment, text=True)
    assert result.splitlines() == ["unset", "unset"]
