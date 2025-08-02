API Reference
=============

This section provides comprehensive API documentation for Egile MCP Client's programmatic interface.

.. note::
   The API documentation is automatically generated from the source code. 
   All classes and functions include detailed docstrings with examples.

Core Classes
------------

MCPClient
~~~~~~~~~

The main client class for direct MCP server interactions.

Example Usage::

    from egile_mcp_client import MCPClient, Config

    # Initialize client
    config = Config.load("config.yaml")
    client = MCPClient(config)

    # Connect to server
    await client.connect("server_name")

    # List available tools
    tools = await client.list_tools()

    # Call a tool
    result = await client.call_tool("search", {"query": "example"})

    # Disconnect
    await client.disconnect()

AgentClient
~~~~~~~~~~~

Client class for AI agent-enhanced interactions.

Example Usage::

    from egile_mcp_client import AgentClient, Config
    from egile_mcp_client.agents import OpenAIAgent

    # Create agent
    agent = OpenAIAgent(api_key="your-key", model="gpt-4")

    # Initialize client
    config = Config.load()
    client = AgentClient(config, agent)

    # Chat with agent
    response = await client.chat("Help me search for information")
    print(response.content)

Agent Classes
-------------

BaseAgent
~~~~~~~~~

Abstract base class for all AI agents.

OpenAIAgent
~~~~~~~~~~~

OpenAI-powered agent implementation.

AnthropicAgent
~~~~~~~~~~~~~~

Anthropic Claude-powered agent implementation.

XAIAgent
~~~~~~~~

xAI Grok-powered agent implementation.

Connection Classes
------------------

BaseConnection
~~~~~~~~~~~~~~

Abstract base class for MCP server connections.

HTTPConnection
~~~~~~~~~~~~~~

HTTP-based MCP server connection.

WebSocketConnection
~~~~~~~~~~~~~~~~~~~

WebSocket-based MCP server connection.

StdioConnection
~~~~~~~~~~~~~~~

Stdio-based MCP server connection for local processes.

Context Managers
----------------

All client classes support async context manager protocol::

    # MCPClient context manager
    async with MCPClient(config) as client:
        await client.connect("server_name")
        # Client automatically disconnects on exit

    # AgentClient context manager  
    async with AgentClient(config, agent) as client:
        response = await client.chat("Hello")
        # Client automatically cleans up on exit

Examples
--------

Complete Integration Example::

    import asyncio
    from egile_mcp_client import Config, AgentClient
    from egile_mcp_client.agents import OpenAIAgent

    async def main():
        # Load configuration
        config = Config.load("config.yaml")
        
        # Create custom agent
        agent = OpenAIAgent(
            api_key="your-api-key",
            model="gpt-4",
            temperature=0.5
        )
        
        # Create agent client
        async with AgentClient(config, agent) as client:
            # Interactive conversation
            while True:
                user_input = input("You: ")
                if user_input.lower() in ['exit', 'quit']:
                    break
                    
                response = await client.chat(user_input)
                print(f"Assistant: {response.content}")

    if __name__ == "__main__":
        asyncio.run(main())

Custom Agent Example::

    from egile_mcp_client.agents.base import BaseAgent
    from egile_mcp_client.protocol import Message, Tool

    class CustomAgent(BaseAgent):
        async def chat(
            self,
            message: str,
            tools: List[Tool],
            history: List[Message]
        ) -> Message:
            # Custom agent logic
            # Use tools as needed
            # Return Message object
            return Message(
                role="assistant",
                content="Custom response",
                tool_calls=[]
            )

Type Definitions
----------------

Common type aliases used throughout the API::

    from typing import Dict, List, Any, Optional, Union

    # Common type aliases
    ServerName = str
    ToolName = str
    ProviderName = str
    ModelName = str
    ConversationId = str

    # Tool parameters and results
    ToolParameters = Dict[str, Any]
    ToolResponse = Dict[str, Any]

    # Configuration types
    ServerConfig = Dict[str, Any]
    ProviderConfig = Dict[str, Any]

For detailed API documentation with full method signatures and parameters, please refer to the source code docstrings or generate the full API documentation using Sphinx autodoc.
