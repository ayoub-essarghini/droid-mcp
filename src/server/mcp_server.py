import asyncio

import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server

from src.infrastructure import adb_manager
from src.tools import android_tools

# Create the MCP Server instance
server = Server("droid-mcp")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    Exposes available Android tools to the AI Agent.
    The Agent reads these descriptions to decide which tool to use.
    """
    return [
        types.Tool(
            name=tool.name,
            description=tool.description,
            inputSchema=tool.arguments_schema,
        )
        for tool in android_tools
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handles tool execution requests from the AI Agent.
    Orchestrates the flow between the Agent request and our Tool logic.
    """
    # Find the tool in our registry
    tool = next((t for t in android_tools if t.name == name), None)

    if not tool:
        raise ValueError(f"Tool not found: {name}")

    # Ensure device is connected before execution
    if not adb_manager.device:
        adb_manager.connect()

    # Execute the tool
    result = await tool.run(**(arguments or {}))

    # Format the response back to the MCP standard
    return [
        types.TextContent(
            type="text", text=f"{result.message}\nData: {result.data if result.data else 'None'}"
        )
    ]


async def main():
    """
    Entry point for the MCP server using Standard Input/Output (stdio).
    This allows the AI Desktop client to spawn this server as a subprocess.
    """
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="droid-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
