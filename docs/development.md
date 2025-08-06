# Development Guide

This guide provides comprehensive information about the Egile MCP Client project structure, implementation details, and development workflow.

## Project Overview

The Egile MCP Client is a comprehensive Python client for interacting with Model Context Protocol (MCP) servers. It provides dual operation modes and supports multiple AI providers.

## Key Features

### Dual Operation Modes
- **Direct Mode**: Connect directly to MCP servers and use their tools/resources
- **Agent Mode**: Use AI agents (OpenAI, Anthropic, or xAI) that can interact with MCP servers

### Multiple Interfaces
- **Command Line Interface**: Full-featured CLI using Click
- **Web Interface**: FastAPI-based web application with chat interface
- **Python API**: Direct programmatic access to all functionality

### AI Provider Support
- **OpenAI**: GPT models including GPT-4, GPT-3.5-turbo
- **Anthropic**: Claude models including Claude-3.5-sonnet, Claude-3-haiku
- **xAI**: Grok models including grok-beta

### MCP Protocol Support
- **Transport Layers**: HTTP, WebSocket, and stdio connections
- **Full Protocol**: Tools, resources, prompts, and notifications
- **Async Operations**: Non-blocking operations with proper error handling

## Project Structure

```
egile-mcp-client/
├── egile_mcp_client/              # Main package
│   ├── __init__.py                # Package initialization
│   ├── config.py                  # Configuration management
│   ├── cli.py                     # Command line interface
│   ├── mcp/                       # MCP protocol implementation
│   │   ├── __init__.py
│   │   ├── client.py             # High-level MCP client
│   │   ├── connection.py         # Transport layer implementations
│   │   └── protocol.py           # MCP protocol message handling
│   ├── agents/                    # AI agent implementations
│   │   ├── __init__.py
│   │   ├── base.py               # Base agent interface
│   │   ├── openai_agent.py       # OpenAI implementation
│   │   ├── anthropic_agent.py    # Anthropic implementation
│   │   └── xai_agent.py          # xAI Grok implementation
│   ├── web/                       # Web interface
│   │   ├── __init__.py
│   │   ├── app.py                # FastAPI application
│   │   ├── routes.py             # API routes and WebSocket handling
│   │   ├── static/               # CSS, JavaScript assets
│   │   └── templates/            # HTML templates
│   │       └── index.html        # Main web interface
│   └── utils/                     # Utility modules
│       ├── __init__.py
│       ├── history.py            # Conversation history management
│       └── logging.py            # Logging configuration
├── tests/                         # Test suite
├── docs/                          # Documentation (Sphinx)
├── config.yaml                    # Configuration file
├── config.example.yaml            # Example configuration
├── simple_mcp_server.py          # Test MCP server
└── pyproject.toml                # Project configuration
```

## Key Implementation Details

### MCP Protocol Support

The client implements the full Model Context Protocol specification:
- **Initialization**: Server capability discovery and version negotiation
- **Tools**: Dynamic tool discovery and execution
- **Resources**: Access to server-provided resources
- **Prompts**: Template-based prompt handling
- **Transport**: Support for HTTP, WebSocket, and stdio connections

### AI Agent Integration

Each AI provider is implemented as a separate agent class:
- **Base Agent**: Abstract interface defining common methods
- **Provider-Specific**: Optimized implementations for each AI service
- **Tool Integration**: Automatic conversion of MCP tools to agent function calls
- **Streaming**: Support for real-time response streaming

### Web Interface

The web interface provides:
- **Real-time Chat**: WebSocket-based chat interface
- **Conversation History**: Persistent session management
- **Server Management**: Dynamic server connection/disconnection
- **Tool Visualization**: Display of available tools and their usage

### Configuration Management

Flexible configuration system:
- **YAML Files**: Human-readable configuration format
- **Environment Variables**: Override configuration with env vars
- **Validation**: Comprehensive configuration validation
- **Hot Reloading**: Support for runtime configuration updates

## Development Workflow

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/jpoullet2000/egile-mcp-client.git
cd egile-mcp-client

# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Install pre-commit hooks
poetry run pre-commit install

# Run tests
poetry run pytest
```

### Code Quality

The project maintains high code quality standards:

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking
- **bandit**: Security analysis
- **pytest**: Testing framework

### Testing Strategy

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test complete user workflows
- **Mock Servers**: Use test MCP servers for reliable testing

## Architecture Patterns

### Async/Await Design

The entire codebase is built around async/await patterns:
- Non-blocking I/O operations
- Concurrent connection handling
- Efficient resource utilization

### Factory Pattern

Connection creation uses factory patterns:
- **ConnectionFactory**: Creates appropriate connection types
- **AgentFactory**: Instantiates AI agents based on provider
- **Extensible**: Easy to add new connection types and providers

### Strategy Pattern

AI agents implement the strategy pattern:
- **BaseAgent**: Common interface
- **Provider Implementations**: Specific strategies for each AI service
- **Runtime Selection**: Choose provider at runtime

### Observer Pattern

Event handling uses observer patterns:
- **Connection Events**: Monitor connection state changes
- **Message Events**: Handle incoming MCP messages
- **Error Events**: Centralized error handling

## Extension Points

### Adding New AI Providers

1. Create new agent class inheriting from `BaseAgent`
2. Implement required methods (`chat`, `stream_chat`, `list_models`)
3. Register in agent factory
4. Add configuration support

### Adding New Transport Types

1. Create new connection class inheriting from `BaseConnection`
2. Implement transport-specific methods
3. Register in connection factory
4. Update configuration schema

### Adding New Tools

Tools are automatically discovered from MCP servers, but you can:
1. Create custom tool wrappers
2. Add tool-specific validation
3. Implement tool result formatting

## Performance Considerations

### Connection Pooling

- HTTP connections use connection pooling
- WebSocket connections support auto-reconnection
- Stdio connections manage process lifecycle

### Memory Management

- Conversation history has configurable limits
- Streaming responses minimize memory usage
- Async operations prevent blocking

### Error Handling

Comprehensive error handling strategy:
- **Graceful Degradation**: Continue operation when possible
- **Retry Logic**: Automatic retry for transient failures
- **User Feedback**: Clear error messages for users
- **Logging**: Detailed logging for debugging

## Deployment Options

### Local Installation

```bash
pip install egile-mcp-client
```

### Docker Deployment

```bash
docker run -v $(pwd)/config.yaml:/app/config.yaml egile-mcp-client
```

### Web Service Deployment

```bash
egile-mcp-client web --host 0.0.0.0 --port 8080
```

## Contributing

See [contributing.md](contributing.md) for detailed contribution guidelines.

## Troubleshooting

See [troubleshooting.md](troubleshooting.md) for common issues and solutions.
