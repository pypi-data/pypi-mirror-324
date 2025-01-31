# Development Guide

## Project Architecture

```
perplexity-mcp-server/
├── src/
│   └── perplexity_mcp/
│       ├── __init__.py      # Package exports
│       ├── version.py       # Version information
│       ├── server.py        # MCP server implementation
│       └── run.py          # Server entry point and logging
├── docs/                    # Documentation
├── tests/                   # Test files (to be implemented)
├── pyproject.toml          # Project configuration and dependencies
├── README.md              # User installation and usage guide
└── DEVELOPMENT.md         # This file - development guide
```

## Local Development Setup

1. Prerequisites:
   - Python 3.11 or higher
   - UV package manager
   - Git
   - A Perplexity API key

2. Clone and Setup:
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
uv pip install "mcp[cli]"  # Required for development tools
```

3. Configure Environment:
```bash
# PowerShell
$env:PERPLEXITY_API_KEY="your-api-key"
$env:PERPLEXITY_MODEL="sonar"  # optional
$env:PYTHONPATH="$PWD/src"     # required for local development

# Bash/CMD
export PERPLEXITY_API_KEY="your-api-key"
export PERPLEXITY_MODEL="sonar"
export PYTHONPATH="$PWD/src"
```

## Development Workflow

### Local Testing

1. Run the server directly:
```bash
python src/perplexity_mcp/run.py
```

2. Run with MCP Inspector (recommended for debugging):
```bash
mcp dev src/perplexity_mcp/run.py
```
This starts the MCP Inspector at http://localhost:51773

3. Test in Claude Desktop:
```json
{
  "perplexity-mcp": {
    "env": {
      "PERPLEXITY_API_KEY": "your-api-key",
      "PERPLEXITY_MODEL": "sonar",
      "PYTHONPATH": "absolute/path/to/project/src"
    },
    "command": "python",
    "args": ["absolute/path/to/project/src/perplexity_mcp/run.py"]
  }
}
```

### Version Management

1. Update version in `src/perplexity_mcp/version.py`:
```python
__version__ = "x.y.z"  # Add a comment about changes
```

2. Update version in `pyproject.toml`:
```toml
[project]
name = "perplexity-mcp-server"
version = "x.y.z"  # Match version.py
```

### Building and Publishing

1. Clean previous builds:
```bash
Remove-Item -Recurse -Force dist,build,*.egg-info -ErrorAction SilentlyContinue  # PowerShell
rm -rf dist/ build/ *.egg-info  # Unix
```

2. Build package:
```bash
python -m build
```

3. Upload to PyPI:
```bash
twine upload dist/*
```

4. Verify installation:
```bash
# In a new virtual environment
uv venv test-env
.\.venv\Scripts\activate
uv pip install perplexity-mcp-server
```

## Code Structure

### Key Components

1. `version.py`:
   - Single source of truth for version
   - Used by both package and server

2. `server.py`:
   - MCP server implementation
   - Perplexity API integration
   - Tool and prompt definitions

3. `run.py`:
   - Server entry point
   - Logging configuration
   - Error handling

### Dependencies

- `mcp`: Model Context Protocol
- `aiohttp`: Async HTTP client
- `pydantic`: Data validation

## Development Standards

1. Code Style:
   - Line length: 88 characters
   - Type hints required
   - Docstrings for public functions
   - Follow PEP 8

2. Git Workflow:
   - Feature branches
   - Descriptive commit messages
   - Test before pushing

3. Testing:
   - Use MCP Inspector
   - Test all models
   - Verify error handling

## Troubleshooting

1. Installation Issues:
   - Verify Python version (>=3.11)
   - Check virtual environment
   - Verify PYTHONPATH

2. Runtime Issues:
   - Check API key validity
   - Verify model selection
   - Monitor stderr for logs

3. Development Mode:
   - Use MCP Inspector
   - Check environment variables
   - Verify file paths

4. Common Errors:
   - "Module not found": Check PYTHONPATH
   - "Invalid API key": Verify environment variables
   - "Model not found": Check model name
