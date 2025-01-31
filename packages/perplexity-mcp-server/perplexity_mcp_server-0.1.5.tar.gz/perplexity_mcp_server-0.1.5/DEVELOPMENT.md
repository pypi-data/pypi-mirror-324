# Development Guide

## Project Architecture

```
perplexity-mcp-server/
├── src/
│   └── perplexity_mcp/
│       ├── __init__.py      # Package metadata and exports
│       ├── version.py       # Version information
│       ├── server.py        # MCP server implementation
│       └── run.py          # Server entry point with stdio handling
├── docs/                    # Documentation
├── tests/                   # Test files (to be implemented)
├── pyproject.toml          # Project configuration and dependencies
├── README.md              # User installation and usage guide
└── DEVELOPMENT.md         # This file - development guide
```

## Environment Setup

1. Create and activate virtual environment:
```bash
uv venv .venv
.\.venv\Scripts\activate  # Windows
source .venv/bin/activate # Unix
```

2. Install in development mode with required dependencies:
```bash
uv pip install -e .
uv pip install "mcp[cli]"  # Required for MCP development tools
```

## Development Workflow

### Local Testing

1. Set environment variables for testing:
```bash
# PowerShell
$env:PERPLEXITY_API_KEY="your-api-key"
$env:PERPLEXITY_MODEL="sonar"  # optional, defaults to sonar
$env:PYTHONPATH="path/to/project/src"  # required for local development

# Bash/CMD
export PERPLEXITY_API_KEY="your-api-key"
export PERPLEXITY_MODEL="sonar"
export PYTHONPATH="path/to/project/src"
```

2. Run the server directly:
```bash
python src/perplexity_mcp/run.py
```

3. Run with MCP Inspector for debugging:
```bash
mcp dev src/perplexity_mcp/run.py
```
This will start the MCP Inspector at http://localhost:51773 where you can monitor server communication.

### Building and Publishing

#### PyPI Setup
1. Create an account on [PyPI](https://pypi.org)
2. Create an API token in your PyPI account settings
3. Configure PyPI credentials:
   ```bash
   # Create or edit ~/.pypirc
   [pypi]
   username = __token__
   password = your-pypi-token
   ```

#### Publishing Process
1. Update version in `version.py`:
   ```python
   __version__ = "x.y.z"  # Update this
   ```

2. Clean previous builds:
   ```bash
   rm -rf dist/ build/ *.egg-info
   ```

3. Build package:
   ```bash
   python -m build
   ```

4. Upload to PyPI:
   ```bash
   twine upload dist/*
   ```

5. Verify installation:
   ```bash
   uv venv test-env
   .\test-env\Scripts\activate
   uv pip install perplexity-mcp-server
   ```

## Configuration

### Available Models
- `sonar`: Standard model (127k context)
- `sonar-pro`: Advanced model (200k context)
- `sonar-reasoning`: Chain of Thought model (127k context)

### Server Configuration
The server configuration in Claude's config file should look like:
```json
{
  "perplexity-mcp": {
    "env": {
      "PERPLEXITY_API_KEY": "xxx",
      "PERPLEXITY_MODEL": "sonar",
      "PYTHONPATH": "path/to/project/src"  # Required for local development
    },
    "command": "python",
    "args": ["path/to/project/src/perplexity_mcp/run.py"],
    "disabled": false,
    "autoApprove": []
  }
}
```

## Code Structure

### version.py
- Contains package version information
- Imported by other modules to avoid circular imports

### server.py
- MCP server implementation
- Defines available tools and prompts
- Handles Perplexity API communication
- Key components:
  - `handle_list_prompts()`: Defines available prompts
  - `handle_get_prompt()`: Generates prompts from arguments
  - `list_tools()`: Defines available tools
  - `call_tool()`: Handles tool execution
  - `call_perplexity()`: Makes API calls to Perplexity

### run.py
- Server entry point
- Handles stdio communication
- Configures logging (to stderr)
- Provides error handling and graceful shutdown

### Key Dependencies
- `mcp`: Model Context Protocol implementation
- `aiohttp`: Async HTTP client for API calls
- `pydantic`: Data validation

## Development Standards

1. Code Style:
   - Line length: 88 characters
   - Use type hints
   - Follow PEP 8
   - Use docstrings for all public functions

2. Git Workflow:
   - Create feature branches
   - Write descriptive commit messages
   - Test before pushing

3. Testing:
   - Test with MCP Inspector for debugging
   - Verify stdio communication
   - Check error handling
   - Test API integration

## Common Issues

1. API Key Issues:
   - Ensure PERPLEXITY_API_KEY is set
   - Check API key validity
   - Verify environment variables are passed correctly

2. Model Selection:
   - Default is "sonar" if not specified
   - Only use supported models
   - Check model availability in API response

3. Development Mode:
   - Always use virtual environment
   - Set PYTHONPATH correctly
   - Use MCP Inspector for debugging
   - Check stderr for logs

4. Stdio Communication:
   - Use stderr for logging (stdout is for MCP)
   - Handle keyboard interrupts gracefully
   - Check for stdio transport errors
