"""Server entry point."""
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

def cli():
    """CLI entry point for perplexity-mcp-server"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        stream=sys.stderr
    )

    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        logging.info("Server stopped by user")
    except Exception as e:
        logging.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    cli()
