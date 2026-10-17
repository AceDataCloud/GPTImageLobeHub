"""A focused tool surface over Ace's existing MCP; no API implementation here."""

import asyncio
import copy
import json
import os
import shutil

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.server.lowlevel import Server
from mcp.server.stdio import stdio_server
from mcp.types import CallToolResult, TextContent, Tool

ALLOWED_TOOLS = frozenset(
    {"openai_generate_image", "openai_edit_image", "openai_get_task", "openai_list_image_models"}
)
IMAGE_TOOLS = frozenset({"openai_generate_image", "openai_edit_image"})


def focused_tools(tools: list[Tool]) -> list[Tool]:
    """Keep the dependency's real schemas, restricting images to GPT Image."""
    selected = []
    for tool in tools:
        if tool.name not in ALLOWED_TOOLS:
            continue
        data = tool.model_dump(mode="json", exclude_none=True)
        if tool.name in IMAGE_TOOLS:
            operation = "Generate" if tool.name == "openai_generate_image" else "Edit"
            data["description"] = (
                f"{operation} GPT Image images through Ace Data Cloud. Select an explicit supported "
                "GPT Image model and check its current price. Submit once, keep the returned task_id, "
                "and query openai_get_task using that value as id until terminal success or failure. "
                "No substitute model is selected."
            )
            schema = data["inputSchema"]
            model = copy.deepcopy(schema.get("properties", {}).get("model", {}))
            models = [value for value in model.get("enum", []) if value.startswith("gpt-image-")]
            if not models:
                raise ValueError("Pinned Ace MCP no longer exposes GPT Image enum values")
            model["enum"] = models
            # Editing's upstream default is DALL-E. Do not silently substitute a
            # paid GPT Image model: make the user's model selection explicit.
            model.pop("default", None)
            model["description"] = "GPT Image model ID supported by this installed Ace MCP."
            schema["properties"]["model"] = model
            schema["required"] = list(dict.fromkeys([*schema.get("required", []), "model"]))
        elif tool.name == "openai_list_image_models":
            data["description"] = (
                "List this adapter's GPT Image model IDs from the pinned dependency schema. "
                "No API generation request; model entitlement and prices must be checked separately."
            )
        selected.append(Tool.model_validate(data))
    if {tool.name for tool in selected} != ALLOWED_TOOLS:
        raise ValueError("Pinned Ace MCP is missing a required image/query tool")
    return selected


def validate_call(name: str, arguments: dict) -> None:
    if name not in ALLOWED_TOOLS:
        raise ValueError("Only GPT Image generation, editing, model information and task query are exposed")
    if name in IMAGE_TOOLS:
        model = arguments.get("model")
        if not isinstance(model, str) or not model.startswith("gpt-image-"):
            raise ValueError("Select a supported gpt-image-* model; no substitute model is used")


async def proxy_call(session: ClientSession, name: str, arguments: dict) -> CallToolResult:
    validate_call(name, arguments)
    # Return the original result, including error flag, text and structured content.
    return await session.call_tool(name, arguments)


async def serve() -> None:
    command = shutil.which("mcp-openai-pro")
    if not command:
        raise RuntimeError("Install the pinned mcp-openai-pro dependency first")
    environment = {
        key: value
        for key, value in os.environ.items()
        if key in {"PATH", "HOME", "LANG", "TMPDIR", "SSL_CERT_FILE", "SSL_CERT_DIR",
                   "ACEDATACLOUD_API_TOKEN", "ACEDATACLOUD_API_BASE_URL", "OPENAI_REQUEST_TIMEOUT"}
    }
    token = environment.get("ACEDATACLOUD_API_TOKEN")
    if not token:
        raise RuntimeError("ACEDATACLOUD_API_TOKEN is required; use a service API Token from Ace Applications")
    # Credentials come from explicit connector env, never an ambient project .env.
    environment["PYTHON_DOTENV_DISABLED"] = "1"
    async with stdio_client(StdioServerParameters(command=command, env=environment)) as (read, write):
        async with ClientSession(read, write) as upstream:
            await upstream.initialize()
            tools = focused_tools((await upstream.list_tools()).tools)
            server = Server("GPT Image by Ace Data Cloud", version="0.1.0")

            @server.list_tools()
            async def list_tools() -> list[Tool]:
                return tools

            @server.call_tool()
            async def call_tool(name: str, arguments: dict) -> CallToolResult:
                if name == "openai_list_image_models":
                    # Information is derived from the dependency schema, not a
                    # handwritten model list, so no paid API request is needed.
                    models = next(tool for tool in tools if tool.name == "openai_generate_image")
                    model_schema = models.inputSchema["properties"]["model"]
                    text = json.dumps({
                        "models": model_schema["enum"], "model_selection_required": True,
                        "source": "Pinned mcp-openai-pro schema; verify service entitlement and current pricing",
                    })
                    # The dependency's FastMCP string tool declares
                    # outputSchema={result:string}; preserve that contract.
                    return CallToolResult(content=[TextContent(type="text", text=text)],
                                          structuredContent={"result": text})
                return await proxy_call(upstream, name, arguments)

            async with stdio_server() as (incoming, outgoing):
                await server.run(incoming, outgoing, server.create_initialization_options())


def main() -> None:
    asyncio.run(serve())
