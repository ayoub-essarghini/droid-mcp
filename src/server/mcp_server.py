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

@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    return [
        types.Prompt(
            name="auto_pilot",
            description="The Ultimate Zero-Effort Developer Agent. Builds and tests autonomously.",
            arguments=[
                types.PromptArgument(
                    name="app_idea",
                    description="Describe the app you want to build in a short sentence.",
                    required=True
                )
            ]
        )
    ]

# This is the master prompt that guides the AI Agent to autonomously build and test.
@server.get_prompt()
async def handle_get_prompt(name: str, arguments: dict[str, str] | None) -> types.GetPromptResult:
    if name == "auto_pilot":
        app_idea = (arguments or {}).get("app_idea", "A simple test app")
        master_prompt = f"""You are a Senior Android Architect building an app autonomously.
The user wants to watch your development journey, including how you handle bugs.

YOUR MISSION: {app_idea}

YOUR WORKFLOW:
1. CODE FAST: Build the first version quickly. Don't over-engineer it.
2. DEPLOY & TEST: Deploy to the emulator and interact with it using your Droid MCP tools.
3. THE "THINKING ALOUD" PROTOCOL (CRITICAL):
   - Whenever you run a command, read the screen, or check logs, you MUST narrate your
     thought process to the user.
   - Example: "I just clicked the 'Play' button. Let me check the crash logs to see if
     the state crashed..."
   - Example: "Ah! I see a NullPointerException in the logcat. I forgot to initialize
     the ViewModel. Let me open MainActivity.kt and fix it."
4. FIX & RE-TEST: If you find an error, explain what caused it, use your file editing
   tools to patch it, and rebuild the app.
5. PUSH THE LIMITS: Once the basic app works, purposefully rotate the screen or
   spam-click buttons (using tap_screen quickly) to try and break your own app.
   If it breaks, fix it!

Do not ask the user for help. You are a genius developer—prove it by debugging your own code!"""

        return types.GetPromptResult(
            description="Autonomous Developer Prompt",
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=master_prompt
                    )
                )
            ]
        )

    raise ValueError(f"Unknown prompt: {name}")

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
