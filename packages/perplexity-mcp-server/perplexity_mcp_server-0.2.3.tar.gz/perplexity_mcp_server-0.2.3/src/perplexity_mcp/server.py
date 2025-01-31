"""MCP server implementation."""
import asyncio
import aiohttp
import os
import ssl
import certifi
import logging

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
            name="perplexity_reasoning",
            description="Search the web and use reasoning and show citations using Perplexity AI. Optionally filter results by recency if specified.",
            arguments=[
                types.PromptArgument(
                    name="query",
                    description="The search query to find information about",
                    required=True,
                ),
                types.PromptArgument(
                    name="recency",
                    description="Optional: Filter results by time period. Only specify when recent information is needed. Options: 'day' (last 24h), 'week' (last 7 days), 'month' (last 30 days), 'year' (last 365 days).",
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
    if name != "perplexity_reasoning":
        raise ValueError(f"Unknown prompt: {name}")

    query = (arguments or {}).get("query", "")
    recency = (arguments or {}).get("recency")
    messages = [
        types.PromptMessage(
            role="user",
            content=types.TextContent(
                type="text",
                text=f"Find information about: {query}",
            ),
        )
    ]
    
    if recency is not None:
        messages.append(
            types.PromptMessage(
                role="user",
                content=types.TextContent(
                    type="text",
                    text=f"Only include results from the last {recency}",
                ),
            )
        )
    
    return types.GetPromptResult(
        description=f"Search the web for information about: {query}",
        messages=messages,
    )

@server.list_tools()
async def list_tools() -> list[types.Tool]:
    """List available tools."""
    return [
        types.Tool(
            name="perplexity_reasoning",
            description="Search the web using Perplexity AI. Optionally filter results by recency if specified.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    },
                    "recency": {
                        "type": "string",
                        "enum": ["day", "week", "month", "year"],
                        "description": "Optional: Filter results by time period. Only specify when recent information is needed."
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
    if name == "perplexity_reasoning":
        query = arguments["query"]
        recency = arguments.get("recency")
        content, citations = await call_perplexity(query, recency)
        # Format citations with numbers
        numbered_citations = [f"[{i+1}] {citation}" for i, citation in enumerate(citations)]
        content_with_citations = content
        if citations:
            content_with_citations += "\n\nSources:\n" + "\n".join(numbered_citations)
        response = [types.TextContent(type="text", text=content_with_citations)]
        return response
    raise ValueError(f"Tool not found: {name}")

async def call_perplexity(query: str, recency: str) -> tuple[str, list[str]]:
    """Call Perplexity API."""
    url = "https://api.perplexity.ai/chat/completions"

    payload = {
        "model": os.getenv("PERPLEXITY_MODEL", "sonar"),
        "messages": [
            {"role": "system", "content": "Be precise and concise."},
            {"role": "user", "content": query},
        ],
        "max_tokens": "8000",
        "temperature": 0.2,
        "top_p": 0.9,
        "return_images": False,
        "return_related_questions": False,
        **({"search_recency_filter": recency} if recency is not None else {}),
        "top_k": 0,
        "stream": False,
        "presence_penalty": 0,
        "frequency_penalty": 1,
    }

    headers = {
        "Authorization": f"Bearer {os.getenv('PERPLEXITY_API_KEY')}",
        "Content-Type": "application/json",
    }

    # Create SSL context with system certificates
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    
    # Configure client session with SSL context
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
        try:
            async with session.post(url, json=payload, headers=headers) as response:
                response.raise_for_status()
                data = await response.json()
                content = data["choices"][0]["message"]["content"]
                citations = data.get("citations", [])
                return content, citations
        except aiohttp.ClientError as e:
            logger = logging.getLogger(__name__)
            logger.error(f"Error calling Perplexity API: {str(e)}")
            raise
