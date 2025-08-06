"""MCP client implementation providing high-level interface to MCP servers."""

import asyncio
import logging
from typing import Any, Dict, List, Optional, Union

from ..config import Config, MCPServerConfig
from .connection import (
    HTTPMCPConnection,
    MCPConnection,
    StdioMCPConnection,
    WebSocketMCPConnection,
)
from .protocol import (
    MCPProtocol,
    MCPRequest,
    MCPResponse,
    PromptInfo,
    ResourceInfo,
    ToolInfo,
)

logger = logging.getLogger(__name__)


class MCPClient:
    """High-level MCP client for interacting with MCP servers."""

    def __init__(self, config: Config):
        self.config = config
        self.protocol = MCPProtocol()
        self.connections: Dict[str, MCPConnection] = {}
        self.initialized_servers: set = set()

    def _create_connection(self, server_config: MCPServerConfig) -> MCPConnection:
        """Create appropriate connection type based on server configuration."""
        if server_config.type == "http":
            if not server_config.url:
                raise ValueError(f"HTTP server {server_config.name} requires URL")
            return HTTPMCPConnection(server_config.url)
        elif server_config.type == "websocket":
            if not server_config.url:
                raise ValueError(f"WebSocket server {server_config.name} requires URL")
            return WebSocketMCPConnection(server_config.url)
        elif server_config.type == "stdio":
            if not server_config.command:
                raise ValueError(f"Stdio server {server_config.name} requires command")
            return StdioMCPConnection(server_config.command)
        else:
            raise ValueError(f"Unsupported server type: {server_config.type}")

    async def connect_to_server(self, server_name: str) -> None:
        """Connect to a specific MCP server."""
        server_config = None
        for config in self.config.mcp_servers:
            if config.name == server_name:
                server_config = config
                break

        if not server_config:
            raise ValueError(f"Server {server_name} not found in configuration")

        if server_name in self.connections:
            logger.warning(f"Already connected to server {server_name}")
            return

        try:
            connection = self._create_connection(server_config)
            await connection.connect()
            self.connections[server_name] = connection

            # Initialize the server
            await self._initialize_server(server_name)

            logger.info(f"Successfully connected to MCP server: {server_name}")

        except Exception as e:
            logger.error(f"Failed to connect to server {server_name}: {e}")
            raise

    async def disconnect_from_server(self, server_name: str) -> None:
        """Disconnect from a specific MCP server."""
        if server_name not in self.connections:
            logger.warning(f"Not connected to server {server_name}")
            return

        try:
            await self.connections[server_name].disconnect()
            del self.connections[server_name]
            self.initialized_servers.discard(server_name)
            logger.info(f"Disconnected from MCP server: {server_name}")
        except Exception as e:
            logger.error(f"Error disconnecting from server {server_name}: {e}")

    async def disconnect_all(self) -> None:
        """Disconnect from all MCP servers."""
        for server_name in list(self.connections.keys()):
            await self.disconnect_from_server(server_name)

    async def _initialize_server(self, server_name: str) -> None:
        """Initialize connection with an MCP server."""
        if server_name not in self.connections:
            raise ValueError(f"Not connected to server {server_name}")

        connection = self.connections[server_name]

        # Send initialization request
        init_request = self.protocol.create_initialize_request(
            {"name": "egile-mcp-client", "version": "0.1.0"}
        )

        try:
            response = await connection.send_request(init_request)

            if response.error:
                raise RuntimeError(f"Initialization failed: {response.error}")

            # Send initialized notification
            initialized_notification = self.protocol.create_notification("initialized")
            await connection.send_notification(initialized_notification)

            self.initialized_servers.add(server_name)
            logger.info(f"Initialized server {server_name}")

        except Exception as e:
            logger.error(f"Failed to initialize server {server_name}: {e}")
            raise

    async def list_tools(self, server_name: str) -> List[ToolInfo]:
        """List available tools from an MCP server."""
        if server_name not in self.connections:
            await self.connect_to_server(server_name)

        connection = self.connections[server_name]
        request = self.protocol.create_list_tools_request()

        try:
            response = await connection.send_request(request)

            if response.error:
                raise RuntimeError(f"Failed to list tools: {response.error}")

            tools = []
            if response.result and "tools" in response.result:
                for tool_data in response.result["tools"]:
                    tools.append(
                        ToolInfo(
                            name=tool_data.get("name", ""),
                            description=tool_data.get("description", ""),
                            input_schema=tool_data.get("inputSchema", {}),
                        )
                    )

            return tools

        except Exception as e:
            logger.error(f"Error listing tools from {server_name}: {e}")
            raise

    async def call_tool(
        self, server_name: str, tool_name: str, arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Call a tool on an MCP server."""
        if server_name not in self.connections:
            await self.connect_to_server(server_name)

        connection = self.connections[server_name]
        request = self.protocol.create_call_tool_request(tool_name, arguments)

        try:
            response = await connection.send_request(request)

            if response.error:
                raise RuntimeError(f"Tool call failed: {response.error}")

            return response.result or {}

        except Exception as e:
            logger.error(f"Error calling tool {tool_name} on {server_name}: {e}")
            raise

    async def list_resources(self, server_name: str) -> List[ResourceInfo]:
        """List available resources from an MCP server."""
        if server_name not in self.connections:
            await self.connect_to_server(server_name)

        connection = self.connections[server_name]
        request = self.protocol.create_list_resources_request()

        try:
            response = await connection.send_request(request)

            if response.error:
                raise RuntimeError(f"Failed to list resources: {response.error}")

            resources = []
            if response.result and "resources" in response.result:
                for resource_data in response.result["resources"]:
                    resources.append(
                        ResourceInfo(
                            uri=resource_data.get("uri", ""),
                            name=resource_data.get("name", ""),
                            description=resource_data.get("description"),
                            mime_type=resource_data.get("mimeType"),
                        )
                    )

            return resources

        except Exception as e:
            logger.error(f"Error listing resources from {server_name}: {e}")
            raise

    async def read_resource(self, server_name: str, uri: str) -> Dict[str, Any]:
        """Read a resource from an MCP server."""
        if server_name not in self.connections:
            await self.connect_to_server(server_name)

        connection = self.connections[server_name]
        request = self.protocol.create_read_resource_request(uri)

        try:
            response = await connection.send_request(request)

            if response.error:
                raise RuntimeError(f"Failed to read resource: {response.error}")

            return response.result or {}

        except Exception as e:
            logger.error(f"Error reading resource {uri} from {server_name}: {e}")
            raise

    async def list_prompts(self, server_name: str) -> List[PromptInfo]:
        """List available prompts from an MCP server."""
        if server_name not in self.connections:
            await self.connect_to_server(server_name)

        connection = self.connections[server_name]
        request = self.protocol.create_list_prompts_request()

        try:
            response = await connection.send_request(request)

            if response.error:
                raise RuntimeError(f"Failed to list prompts: {response.error}")

            prompts = []
            if response.result and "prompts" in response.result:
                for prompt_data in response.result["prompts"]:
                    prompts.append(
                        PromptInfo(
                            name=prompt_data.get("name", ""),
                            description=prompt_data.get("description", ""),
                            arguments=prompt_data.get("arguments"),
                        )
                    )

            return prompts

        except Exception as e:
            logger.error(f"Error listing prompts from {server_name}: {e}")
            raise

    async def get_prompt(
        self, server_name: str, name: str, arguments: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Get a prompt from an MCP server."""
        if server_name not in self.connections:
            await self.connect_to_server(server_name)

        connection = self.connections[server_name]
        request = self.protocol.create_get_prompt_request(name, arguments)

        try:
            response = await connection.send_request(request)

            if response.error:
                raise RuntimeError(f"Failed to get prompt: {response.error}")

            return response.result or {}

        except Exception as e:
            logger.error(f"Error getting prompt {name} from {server_name}: {e}")
            raise

    def get_connected_servers(self) -> List[str]:
        """Get list of currently connected server names."""
        return list(self.connections.keys())

    def is_connected(self, server_name: str) -> bool:
        """Check if connected to a specific server."""
        return (
            server_name in self.connections
            and self.connections[server_name].is_connected
        )
