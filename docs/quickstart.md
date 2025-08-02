# Quick Start Guide

This guide will get you up and running with Egile MCP Client in just a few minutes.

## Prerequisites

Before starting, make sure you have:
- Installed Egile MCP Client (see {doc}`installation`)
- A text editor for configuration files
- (Optional) API keys for AI providers if using agent mode

## Step 1: Basic Configuration

Create a configuration file to get started:

```bash
# Copy the example configuration
cp config.example.yaml config.yaml

# Edit the configuration file
nano config.yaml  # or your preferred editor
```

### Minimal Configuration

For a quick start, you can use this minimal configuration:

```yaml
# Minimal config.yaml
mcp_servers:
  - name: "test_server"
    url: "http://localhost:8000"
    type: "http"
    description: "Test MCP server"

default_ai_provider: "openai"
web_interface:
  host: "localhost"
  port: 8080

logging:
  level: "INFO"
```

## Step 2: Choose Your Mode

Egile MCP Client supports two main operation modes:

### Direct Mode
Connect directly to MCP servers without AI assistance.

### Agent Mode
Use AI agents that can intelligently interact with MCP tools.

## Step 3: Your First Interaction

### Option A: Direct Mode (Simplest)

```bash
# List available tools from a server
egile-mcp-client tools --server test_server

# Connect directly to interact with tools
egile-mcp-client direct --server test_server
```

### Option B: Agent Mode (AI-Enhanced)

First, set up your AI provider API key:

```bash
# Set environment variable (recommended)
export OPENAI_API_KEY="your-api-key-here"

# Or add to config.yaml:
# ai_providers:
#   openai:
#     api_key: "your-api-key-here"
```

Then start the agent:

```bash
# Start interactive chat with AI agent
egile-mcp-client chat --mode agent --provider openai
```

### Option C: Web Interface (Most User-Friendly)

```bash
# Start the web server
egile-mcp-client web

# Open your browser to http://localhost:8080
```

## Step 4: Example Interactions

### Direct Mode Example

```bash
$ egile-mcp-client direct --server test_server
Connected to test_server
Available tools: search, summarize, calculate

> search query="Python MCP examples"
Searching for: Python MCP examples
Results: [search results would appear here]

> exit
```

### Agent Mode Example

```console
$ egile-mcp-client chat --mode agent --provider openai
Starting chat with OpenAI agent...

You: Can you help me search for information about machine learning?
Assistant: I'll help you search for machine learning information using the available tools.

[The AI agent would use MCP tools to search and provide results]

You: exit
```

### Web Interface Example

1. Open http://localhost:8080 in your browser
2. Select "Agent Mode" and choose your AI provider
3. Type: "Help me find information about Python programming"
4. The AI agent will use available MCP tools to assist you

## Step 5: Understanding the Results

### Tool Responses
When using direct mode, you'll see raw tool responses from the MCP server.

### AI Agent Responses
In agent mode, the AI processes tool results and provides natural language responses.

### Web Interface
The web interface shows both the conversation flow and underlying tool calls.

## Next Steps

Now that you have the basics working:

1. **Explore Configuration**: See {doc}`configuration` for advanced settings
2. **Learn More Commands**: Check {doc}`usage` for comprehensive examples  
3. **Set Up Multiple Servers**: Configure additional MCP servers
4. **Customize AI Behavior**: Adjust AI provider settings and prompts
5. **Try Different Interfaces**: Experiment with CLI, web, and programmatic APIs

## Common First-Time Issues

### No MCP Server Available
If you don't have an MCP server running:
```bash
# The client will show: "No servers configured or available"
# Solution: Set up a test MCP server or use a public one
```

### API Key Issues
For agent mode:
```bash
# Error: "No API key found for provider"
# Solution: Set environment variable or update config.yaml
export OPENAI_API_KEY="your-key-here"
```

### Connection Errors
```bash
# Error: "Connection refused"
# Solution: Ensure MCP server is running and accessible
curl http://localhost:8000/health  # Test server connectivity
```

## Quick Reference

### Key Commands
```bash
# Show help
egile-mcp-client --help

# List configured servers
egile-mcp-client servers

# Test connection to a server
egile-mcp-client test --server server_name

# Start web interface
egile-mcp-client web

# Direct mode interaction
egile-mcp-client direct --server server_name

# Agent mode chat
egile-mcp-client chat --mode agent --provider openai
```

### Configuration Files
- `config.yaml` - Main configuration
- `.env` - Environment variables (optional)
- `logs/` - Application logs

### Environment Variables
- `OPENAI_API_KEY` - OpenAI API key
- `ANTHROPIC_API_KEY` - Anthropic API key  
- `XAI_API_KEY` - xAI API key
- `MCP_CLIENT_CONFIG` - Custom config file path

You're now ready to explore the full capabilities of Egile MCP Client!
