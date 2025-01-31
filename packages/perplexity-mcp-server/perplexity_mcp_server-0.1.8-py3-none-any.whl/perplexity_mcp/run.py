"""Entry point for MCP server."""
import asyncio
import logging
import sys
import os

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions
import mcp.server.stdio

from perplexity_mcp.server import server
from perplexity_mcp.version import __version__

logger = logging.getLogger(__name__)

async def run_server():
    """Run the server."""
    logger.info("Starting Perplexity MCP server...")
    
    API_KEY = os.getenv("PERPLEXITY_API_KEY")
    if not API_KEY:
        raise ValueError("PERPLEXITY_API_KEY environment variable is required")
    logger.info("API key found")

    # Set up stdio server
    logger.info("Initializing stdio server...")
    try:
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            logger.info("Stdio server initialized")
            
            # Run server with stdio streams
            logger.info("Running server...")
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="perplexity-mcp",
                    server_version=__version__,
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )
    except Exception as e:
        logger.exception("Error in stdio server")
        raise

def main():
    """Main entry point."""
    # Configure logging to stderr since stdout is used for MCP communication
    root_logger = logging.getLogger()
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.DEBUG)

    # Disable other loggers
    for name in logging.root.manager.loggerDict:
        if name != __name__:
            logging.getLogger(name).setLevel(logging.WARNING)

    logger.info("Starting main...")

    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down...")
    except Exception as e:
        logger.exception("Error running server")
        sys.exit(1)

if __name__ == "__main__":
    main()
