"""MCP server implementation."""
import asyncio
import aiohttp
import os

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server

from .version import __version__

# Create server instance
server = Server("perplexity-mcp")

@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    """List available prompts."""
    return [
        types.Prompt(
            name="perplexity_search_web",
            description="Search the web using Perplexity AI and filter results by recency",
            arguments=[
                types.PromptArgument(
                    name="query",
                    description="The search query to find information about",
                    required=True,
                ),
                types.PromptArgument(
                    name="recency",
                    description="Filter results by how recent they are. Options: 'day' (last 24h), 'week' (last 7 days), 'month' (last 30 days), 'year' (last 365 days). Defaults to 'month'.",
                    required=False,
                ),
            ],
        )
    ]

@server.get_prompt()
async def handle_get_prompt(
    name: str, arguments: dict[str, str] | None
) -> types.GetPromptResult:
    """Generate a prompt by combining arguments with server state."""
    if name != "perplexity_search_web":
        raise ValueError(f"Unknown prompt: {name}")

    query = (arguments or {}).get("query", "")
    recency = (arguments or {}).get("recency", "month")
    return types.GetPromptResult(
        description=f"Search the web for information about: {query}",
        messages=[
            types.PromptMessage(
                role="user",
                content=types.TextContent(
                    type="text",
                    text=f"Find recent information about: {query}",
                ),
            ),
            types.PromptMessage(
                role="user",
                content=types.TextContent(
                    type="text",
                    text=f"Only include results from the last {recency}",
                ),
            ),
        ],
    )

@server.list_tools()
async def list_tools() -> list[types.Tool]:
    """List available tools."""
    return [
        types.Tool(
            name="perplexity_search_web",
            description="Search the web using Perplexity AI with recency filtering",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "recency": {
                        "type": "string",
                        "enum": ["day", "week", "month", "year"],
                        "default": "month",
                    },
                },
                "required": ["query"],
            },
        )
    ]

@server.call_tool()
async def call_tool(
    name: str, arguments: dict
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool calls."""
    if name == "perplexity_search_web":
        query = arguments["query"]
        recency = arguments.get("recency", "month")
        result = await call_perplexity(query, recency)
        return [types.TextContent(type="text", text=str(result))]
    raise ValueError(f"Tool not found: {name}")

async def call_perplexity(query: str, recency: str) -> str:
    """Call Perplexity API."""
    url = "https://api.perplexity.ai/chat/completions"

    payload = {
        "model": os.getenv("PERPLEXITY_MODEL", "sonar"),
        "messages": [
            {"role": "system", "content": "Be precise and concise."},
            {"role": "user", "content": query},
        ],
        "max_tokens": "512",
        "temperature": 0.2,
        "top_p": 0.9,
        "return_images": False,
        "return_related_questions": False,
        "search_recency_filter": recency,
        "top_k": 0,
        "stream": False,
        "presence_penalty": 0,
        "frequency_penalty": 1,
    }

    headers = {
        "Authorization": f"Bearer {os.getenv('PERPLEXITY_API_KEY')}",
        "Content-Type": "application/json",
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            response.raise_for_status()
            data = await response.json()
            return data["choices"][0]["message"]["content"]

async def main():
    """Run the MCP server."""
    API_KEY = os.getenv("PERPLEXITY_API_KEY")
    if not API_KEY:
        raise ValueError("PERPLEXITY_API_KEY environment variable is required")

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="perplexity-mcp-server",
                server_version=__version__,
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )
