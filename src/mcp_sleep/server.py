import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any, Sequence
from mcp import Tool
from mcp.server import Server
from mcp.types import TextContent

from .sleep import SleepFetcher


# Configure logging
logger = logging.getLogger("mcp-sleep")


@dataclass
class AppContext:
    """Application context for MCP Sleep."""
    sleep: SleepFetcher | None = None


@asynccontextmanager
async def server_lifespan(server: Server) -> AsyncIterator[AppContext]:
    """Initialize and clean up application resources."""
    try:
        # Initialize services
        sleep = SleepFetcher()

        # Log the startup information
        logger.info("Starting MCP Sleep server")

        # Provide context to the application
        yield AppContext(sleep=sleep)
    finally:
        # Cleanup resources if needed
        pass


# Create server instance
app = Server("mcp-sleep", lifespan=server_lifespan)


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available Sleep tools."""
    tools = []
    ctx = app.request_context.lifespan_context

    # Add Sleep tools if Sleep is configured
    if ctx:
        tools.extend(
            [
                Tool(
                    name="sleep",
                    description="If you need to wait for a few seconds to continue with the task you are performing .",  # noqa: E501
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "seconds": {
                                "type": "number",
                                "minimum": 0,
                                "maximum": ctx.sleep.config.timeout,
                                "description": "seconds it will take me to tell you to continue."  # noqa: E501
                            }
                        },
                        "required": ["seconds"],
                    },
                ),
            ]
        )
    return tools


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent]:
    """Handle tool calls for Sleep."""
    ctx = app.request_context.lifespan_context
    try:
        if name == "sleep":
            if not ctx:
                raise ValueError("Sleep is not configured.")
            seconds = arguments.get("seconds")
            if not seconds:
                raise ValueError("Seconds is required.")

            if seconds > int(ctx.sleep.config.timeout):
                return [
                    TextContent(
                        type="text",
                        text=f"My configuration does not allow me to make you wait more than {ctx.sleep.config.timeout} seconds",  # noqa: E501
                    )
                ]
            # Sleep seconds value
            await ctx.sleep.wait(seconds)

            return [
                TextContent(
                    type="text",
                    text=f"You can continue to do your task after you've been waiting {seconds} seconds",  # noqa: E501
                )
            ]

        raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        logger.error(f"Tool execution error: {str(e)}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def run_server(transport: str = "stdio", port: int = 8000) -> None:
    """Run the MCP Sleep server with the specified transport."""
    if transport == "sse":
        from mcp.server.sse import SseServerTransport
        from starlette.applications import Starlette
        from starlette.requests import Request
        from starlette.routing import Mount, Route

        sse = SseServerTransport("/messages/")

        async def handle_sse(request: Request) -> None:
            async with sse.connect_sse(
                request.scope, request.receive, request._send
            ) as streams:
                await app.run(
                    streams[0], streams[1], app.create_initialization_options()
                )

        starlette_app = Starlette(
            debug=True,
            routes=[
                Route("/sse", endpoint=handle_sse),
                Mount("/messages/", app=sse.handle_post_message),
            ],
        )

        import uvicorn

        # Set up uvicorn config
        config = uvicorn.Config(starlette_app, host="0.0.0.0", port=port)  # noqa: S104,E501
        server = uvicorn.Server(config)
        # Use server.serve() instead of run() to stay in the same event loop
        await server.serve()
    else:
        from mcp.server.stdio import stdio_server

        async with stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream, write_stream, app.create_initialization_options()
            )
