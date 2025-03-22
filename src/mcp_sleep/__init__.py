import asyncio
import logging
import os
import sys

import click
from dotenv import load_dotenv

__version__ = "0.1.0"

logger = logging.getLogger("mcp-sleep")


@click.command()
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Increase verbosity (can be used multiple times)",
)
@click.option(
    "--env-file", type=click.Path(exists=True, dir_okay=False),
    help="Path to .env file"
)
@click.option(
    "--timeout",
    default="60",
    help="Maximun time in seconds that the MCP server will wait for",
)
@click.option(
    "--transport",
    type=click.Choice(["stdio", "sse"]),
    default="stdio",
    help="Transport type (stdio or sse)",
)
@click.option(
    "--port",
    default=8000,
    help="Port to listen on for SSE transport",
)
def main(
    verbose: bool,
    env_file: str | None,
    transport: str,
    timeout: int,
    port: int,
) -> None:
    """MCP Sleep Server

    """
    # Configure logging based on verbosity
    logging_level = logging.INFO
    if verbose == 1:
        logging_level = logging.INFO
    elif verbose >= 2:
        logging_level = logging.DEBUG

    logging.basicConfig(level=logging_level, stream=sys.stderr)

    # Load environment variables from file if specified, otherwise try default .env   # noqa: E501
    if env_file:
        logger.debug(f"Loading environment from file: {env_file}")
        load_dotenv(env_file)
    else:
        logger.debug("Attempting to load environment from default .env file")
        load_dotenv()

    # Set environment variables from command line arguments if provided
    if timeout:
        os.environ["MCP_SLEEP_TIMEOUT"] = timeout

    from . import server as server

    # Run the server with specified transport
    asyncio.run(server.run_server(transport=transport, port=port))


__all__ = ["main", "server", "__version__"]
