# Perplexity MCP Server

A Model Context Protocol (MCP) server that provides web search functionality using [Perplexity AI's](https://www.perplexity.ai/) API. Works with the [Anthropic](https://www.anthropic.com/news/model-context-protocol) Claude desktop client.

## Features

- Web search using Perplexity AI
- Recency filtering (day/week/month/year)
- Multiple model support (sonar/sonar-pro/sonar-reasoning)
- Citations support for search results

## Installation

### Prerequisites

1. Python 3.11 or higher
2. [UV](https://github.com/astral-sh/uv) package manager:
```bash
# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### User Installation (PyPI)

For users who want to use the MCP server:

```bash
uv pip install perplexity-mcp-server
```

### Developer Installation (Local)

For developers who want to modify the server:

```bash
# Clone the repository
git clone https://github.com/felores/perplexity-mcp-server.git
cd perplexity-mcp-server

# Create and activate virtual environment
uv venv .venv
.\.venv\Scripts\activate  # Windows
source .venv/bin/activate # Unix

# Install in development mode
uv pip install -e .
```

## Configuration

### Claude Desktop Setup

1. Get your API key from [Perplexity AI](https://www.perplexity.ai/)

2. Edit Claude's config file:
- Windows: `%APPDATA%/Claude/claude_desktop_config.json`
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

#### For Users (PyPI Installation)
```json
{
  "perplexity-mcp": {
    "env": {
      "PERPLEXITY_API_KEY": "your-api-key-here",
      "PERPLEXITY_MODEL": "sonar"
    },
    "command": "uv",
    "args": ["run", "perplexity-mcp-server"]
  }
}
```

#### For Developers (Local Installation)
```json
{
  "perplexity-mcp": {
    "env": {
      "PERPLEXITY_API_KEY": "your-api-key-here",
      "PERPLEXITY_MODEL": "sonar",
      "PYTHONPATH": "path/to/your/project/src"
    },
    "command": "python",
    "args": ["path/to/your/project/src/perplexity_mcp/run.py"]
  }
}
```

### Available Models

- `sonar`: Standard model (127k context)
- `sonar-pro`: Advanced model (200k context)
- `sonar-reasoning`: Chain of Thought model (127k context)

If no model is specified, defaults to `sonar`.

## Usage

1. Open Claude desktop client
2. Try a prompt like: "Search the web for recent news about AI"
3. Click "Allow for this chat" when prompted

## Development

For development instructions, see [DEVELOPMENT.md](DEVELOPMENT.md)
