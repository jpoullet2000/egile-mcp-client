# Usage Guide

This comprehensive guide covers all the ways you can use Egile MCP Client, from basic command-line operations to advanced programmatic usage.

## Overview

Egile MCP Client provides three main interfaces:

1. **Command Line Interface (CLI)** - For terminal-based interactions
2. **Web Interface** - For browser-based interactions
3. **Programmatic API** - For integration into other applications

## Command Line Interface

### Quick Reference

```bash
# Main commands
egile-mcp-client direct --server SERVER_NAME     # Direct MCP server interaction
egile-mcp-client agent --provider PROVIDER       # AI agent mode
egile-mcp-client tools [--server SERVER_NAME]    # List available tools
egile-mcp-client web                              # Start web interface

# Configuration management
egile-mcp-client config validate                  # Validate configuration
egile-mcp-client config show                      # Show current configuration
egile-mcp-client config test-servers              # Test server connections

# Options
egile-mcp-client --config PATH                    # Use custom config file
egile-mcp-client --verbose                        # Enable verbose logging
egile-mcp-client --help                           # Show help
```

### Basic Commands

```bash
# Show help
egile-mcp-client --help

# Show help
egile-mcp-client --help

# List configured servers and validate configuration
egile-mcp-client config show
egile-mcp-client config validate
egile-mcp-client config test-servers
```

### Direct Mode

Connect directly to MCP servers without AI assistance:

```bash
# List available tools from all servers
egile-mcp-client tools

# List tools from a specific server
egile-mcp-client tools --server server_name

# Interactive direct mode
egile-mcp-client direct --server server_name
```

#### Direct Mode Examples

```bash
# List tools from all configured servers
$ egile-mcp-client tools
Available tools from web_search:
- search: Search the web for information
- summarize: Summarize web content
- extract: Extract specific data from web pages

# Interactive session
$ egile-mcp-client direct --server web_search
Connected to web_search server
Type 'help' for available commands, 'exit' to quit

> tools
Available tools: search, summarize, extract

> call search {"query": "Python MCP tutorial", "limit": 5}
{
  "results": [
    {
      "title": "Getting Started with MCP",
      "url": "https://example.com/mcp-tutorial",
      "snippet": "Learn how to build MCP servers..."
    }
  ]
}

> exit
```

### Agent Mode

Use AI agents that can intelligently interact with MCP tools:

```bash
# Interactive chat with AI agent
egile-mcp-client agent --provider openai

# Chat with specific model
egile-mcp-client agent --provider anthropic --model claude-3-opus
```

#### Agent Mode Examples

```console
# Start interactive chat
$ egile-mcp-client agent --provider openai
Starting chat with OpenAI (gpt-4)...
Connected to servers: web_search, local_tools

You: Can you help me research renewable energy trends?
Assistant: I'll help you research renewable energy trends. Let me search for the latest information.

[Using web_search tool to search for "renewable energy trends 2024"]

Based on my search, here are the key renewable energy trends:

1. **Solar Power Growth**: Solar installations continue to grow at record pace
2. **Energy Storage**: Battery technology improvements making renewables more viable
3. **Grid Integration**: Smart grid technologies enabling better renewable integration

You: What about wind energy specifically?
Assistant: [Searches for wind energy trends and provides detailed analysis]

# One-shot query example
### Web Interface

Start the web server for browser-based interactions:

```bash
# Start with default settings
egile-mcp-client web

# Custom host and port
egile-mcp-client web --host 0.0.0.0 --port 9000

# Development mode with auto-reload
egile-mcp-client web --reload --debug
```

#### Web Interface Features

1. **Interactive Chat**: Real-time conversation with AI agents
2. **Server Management**: Switch between MCP servers
3. **Tool Explorer**: Browse and test available tools
4. **Conversation History**: Persistent chat history
5. **Configuration Editor**: Modify settings through web UI

#### Accessing the Web Interface

1. Start the server: `egile-mcp-client web`
2. Open browser to `http://localhost:8080`
3. Select your preferred mode (Direct or Agent)
4. Choose AI provider (for Agent mode)
5. Start chatting!

### Advanced CLI Usage

#### Configuration Management

```bash
# Use custom configuration file
egile-mcp-client --config /path/to/config.yaml chat

# Override configuration with environment variables
MCP_DEFAULT_PROVIDER=anthropic egile-mcp-client agent

# Validate and test configuration
egile-mcp-client config validate
egile-mcp-client config test-servers

# Show current configuration
egile-mcp-client config show
```

#### Server Management

```bash
# List available tools from all servers
egile-mcp-client tools

# List tools from specific server
egile-mcp-client tools --server web_search

# Show configuration
egile-mcp-client config show

# Validate configuration
egile-mcp-client config validate
```

#### Tool Management

```bash
# List tools from all servers
egile-mcp-client tools list

# Get detailed tool information
egile-mcp-client tools describe --server web_search --tool search

# Test a tool call
egile-mcp-client tools test --server web_search --tool search --args '{"query": "test"}'
```

#### Conversation History

```bash
# List conversation history
egile-mcp-client history list

# Show specific conversation
egile-mcp-client history show --id conversation_123

# Export conversation
egile-mcp-client history export --id conversation_123 --format json

# Clear history
egile-mcp-client history clear
```

## Programmatic API

### Basic Usage

```python
from egile_mcp_client import MCPClient, Config

# Load configuration
config = Config.load("config.yaml")

# Create client
client = MCPClient(config)

# Connect to a server
await client.connect("web_search")

# List available tools
tools = await client.list_tools()
print(f"Available tools: {[tool.name for tool in tools]}")

# Call a tool
result = await client.call_tool("search", {"query": "Python tutorials"})
print(result)

# Disconnect
await client.disconnect()
```

### Agent Integration

```python
from egile_mcp_client import AgentClient
from egile_mcp_client.agents import OpenAIAgent

# Create agent
agent = OpenAIAgent(
    api_key="your-api-key",
    model="gpt-4",
    temperature=0.7
)

# Create agent client
client = AgentClient(config, agent)

# Start conversation
response = await client.chat("Help me search for machine learning resources")
print(response.content)

# Continue conversation
response = await client.chat("What about deep learning specifically?")
print(response.content)
```

### Custom Agents

```python
from egile_mcp_client.agents.base import BaseAgent
from egile_mcp_client.protocol import Message

class CustomAgent(BaseAgent):
    async def chat(self, message: str, tools: List[Tool]) -> Message:
        # Custom agent logic here
        # Use available MCP tools
        # Return Message object
        pass

# Use custom agent
agent = CustomAgent()
client = AgentClient(config, agent)
```

### Async Context Manager

```python
from egile_mcp_client import MCPClient

async def main():
    config = Config.load()
    
    async with MCPClient(config) as client:
        await client.connect("web_search")
        
        # Client will automatically disconnect when exiting context
        result = await client.call_tool("search", {"query": "async Python"})
        return result

# Run with asyncio
import asyncio
result = asyncio.run(main())
```

### Streaming Responses

```python
async def stream_chat():
    async with AgentClient(config, agent) as client:
        async for chunk in client.stream_chat("Tell me about renewable energy"):
            print(chunk.content, end="", flush=True)
        print()  # New line at end
```

### Error Handling

```python
from egile_mcp_client.exceptions import (
    MCPConnectionError,
    MCPToolError,
    MCPTimeoutError
)

try:
    result = await client.call_tool("search", {"query": "test"})
except MCPConnectionError:
    print("Failed to connect to MCP server")
except MCPToolError as e:
    print(f"Tool execution failed: {e}")
except MCPTimeoutError:
    print("Request timed out")
```

## Integration Examples

### Flask Application

```python
from flask import Flask, request, jsonify
from egile_mcp_client import AgentClient, Config
from egile_mcp_client.agents import OpenAIAgent

app = Flask(__name__)

# Initialize client
config = Config.load()
agent = OpenAIAgent(api_key="your-key")
client = AgentClient(config, agent)

@app.route('/chat', methods=['POST'])
async def chat():
    message = request.json['message']
    response = await client.chat(message)
    return jsonify({'response': response.content})

if __name__ == '__main__':
    app.run()
```

### FastAPI Application

```python
from fastapi import FastAPI
from pydantic import BaseModel
from egile_mcp_client import AgentClient, Config
from egile_mcp_client.agents import AnthropicAgent

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    provider: str = "anthropic"

@app.post("/chat")
async def chat(request: ChatRequest):
    config = Config.load()
    agent = AnthropicAgent(api_key="your-key")
    
    async with AgentClient(config, agent) as client:
        response = await client.chat(request.message)
        return {"response": response.content}
```

### Jupyter Notebook

```python
# Cell 1: Setup
import asyncio
from egile_mcp_client import AgentClient, Config
from egile_mcp_client.agents import OpenAIAgent

config = Config.load()
agent = OpenAIAgent(api_key="your-key")
client = AgentClient(config, agent)

# Cell 2: Chat function
async def chat(message):
    response = await client.chat(message)
    return response.content

# Cell 3: Interactive chat
message = "Help me analyze this dataset"
response = await chat(message)
print(response)
```

## Performance Tips

### Connection Pooling

```python
# Use connection pooling for multiple requests
config = Config.load()
config.performance.connection_pool_size = 10

client = MCPClient(config)
```

### Concurrent Requests

```python
import asyncio

async def concurrent_requests():
    tasks = [
        client.call_tool("search", {"query": f"topic {i}"})
        for i in range(10)
    ]
    results = await asyncio.gather(*tasks)
    return results
```

## Troubleshooting

### Connection Issues

```bash
# Test server connectivity by listing tools
egile-mcp-client tools --server server_name

# Validate configuration
egile-mcp-client config validate
```

### Debug Mode

```bash
# Enable debug logging
export MCP_LOG_LEVEL=DEBUG
egile-mcp-client agent

# Or in configuration
logging:
  level: DEBUG
```

### Common Error Messages

1. **"No servers configured"**: Check your config.yaml file
2. **"Connection refused"**: Ensure MCP server is running
3. **"API key not found"**: Set environment variables or update config
4. **"Tool not found"**: Check tool name and server connection
5. **"Timeout"**: Increase timeout values in configuration

### Performance Issues

```bash
# Monitor performance
egile-mcp-client monitor --server server_name

# Check resource usage
egile-mcp-client stats

# Profile tool calls
egile-mcp-client profile --tool tool_name
```
