"""Main entry point for running the server directly."""
import asyncio
import logging
import sys
import os

from .server import server, main

def cli():
    """CLI entry point for perplexity-mcp"""
    logging.basicConfig(level=logging.INFO)

    API_KEY = os.getenv("PERPLEXITY_API_KEY")
    if not API_KEY:
        print(
            "Error: PERPLEXITY_API_KEY environment variable is required",
            file=sys.stderr,
        )
        sys.exit(1)

    asyncio.run(main())

if __name__ == "__main__":
    cli()
