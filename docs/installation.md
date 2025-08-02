# Installation

This guide will help you install and set up Egile MCP Client on your system.

## Requirements

- **Python**: 3.10 or higher
- **Operating System**: Linux, macOS, or Windows
- **Memory**: At least 512MB RAM (more recommended for AI agent mode)
- **Network**: Internet connection for AI provider APIs (optional for direct mode)

## Installation Methods

### Option 1: Install from PyPI (Recommended)

```bash
# Install the latest stable version
pip install egile-mcp-client

# Or install with specific extras
pip install "egile-mcp-client[web,dev]"
```

### Option 2: Install from Source

#### Using Poetry (Recommended for Development)

```bash
# Clone the repository
git clone https://github.com/jpoullet2000/egile-mcp-client.git
cd egile-mcp-client

# Install Poetry if you haven't already
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies and the package
poetry install

# Activate the virtual environment
poetry shell
```

#### Using pip

```bash
# Clone the repository
git clone https://github.com/jpoullet2000/egile-mcp-client.git
cd egile-mcp-client

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

## Verify Installation

After installation, verify that the client is working correctly:

```bash
# Check the version
egile-mcp-client --version

# Show help
egile-mcp-client --help
```

You should see output similar to:
```
Egile MCP Client v0.1.0
Usage: egile-mcp-client [OPTIONS] COMMAND [ARGS]...
```

## Next Steps

1. **Configure the client**: See {doc}`configuration` for detailed setup instructions
2. **Quick start**: Follow the {doc}`quickstart` guide for your first interaction
3. **Set up AI providers**: Configure your API keys for OpenAI, Anthropic, or xAI

## Dependencies

The client requires several Python packages that are automatically installed:

### Core Dependencies
- **click**: Command-line interface framework
- **httpx**: HTTP client for async requests
- **websockets**: WebSocket client support
- **pydantic**: Data validation and settings management
- **pyyaml**: YAML configuration file support
- **rich**: Rich terminal output formatting
- **typer**: Modern CLI framework

### AI Provider Dependencies
- **openai**: OpenAI API client
- **anthropic**: Anthropic API client

### Web Interface Dependencies
- **fastapi**: Modern web framework
- **uvicorn**: ASGI server
- **jinja2**: Template engine
- **aiofiles**: Async file operations
- **sse-starlette**: Server-sent events support

### Development Dependencies (Optional)
- **pytest**: Testing framework
- **pytest-asyncio**: Async testing support
- **pytest-cov**: Coverage reporting
- **black**: Code formatting
- **flake8**: Code linting
- **mypy**: Type checking

## Troubleshooting

### Common Issues

#### Import Errors
If you encounter import errors, ensure your virtual environment is activated:
```bash
# Poetry users
poetry shell

# pip/venv users
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Permission Errors
On some systems, you might need to use `--user` flag:
```bash
pip install --user egile-mcp-client
```

#### Python Version Issues
Ensure you're using Python 3.10 or higher:
```bash
python --version
# Should show Python 3.10.x or higher
```

#### Network Issues
If you're behind a corporate firewall, you might need to configure proxy settings:
```bash
pip install --proxy http://proxy.company.com:port egile-mcp-client
```

### Getting Help

If you encounter issues not covered here:

1. Check the [GitHub Issues](https://github.com/jpoullet2000/egile-mcp-client/issues)
2. Review the {doc}`troubleshooting` section
3. Create a new issue with detailed information about your setup and the error
