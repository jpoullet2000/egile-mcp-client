"""Test suite for the MCP client functionality."""

import pytest
from unittest.mock import patch

from egile_mcp_client.config import Config, MCPServerConfig
from egile_mcp_client.mcp.client import MCPClient
from egile_mcp_client.mcp.protocol import MCPProtocol, MCPResponse, ToolInfo


class MockMCPConnection:
    """Mock MCP connection for testing."""

    def __init__(self, server_name: str = "test_server"):
        self.server_name = server_name
        self.connected = False
        self.initialized = False

    async def connect(self):
        """Mock connect method."""
        self.connected = True

    async def disconnect(self):
        """Mock disconnect method."""
        self.connected = False

    async def send_notification(self, notification):
        """Mock send_notification method."""
        # For mocking purposes, just accept notifications
        pass

    async def send_request(self, request):
        """Mock send_request method."""
        if not self.connected:
            raise ConnectionError("Not connected")

        # Mock responses based on request method
        if request.method == "initialize":
            self.initialized = True
            return MCPResponse(
                jsonrpc="2.0",
                id=request.id,
                result={
                    "protocolVersion": "1.0.0",
                    "capabilities": {"tools": True, "resources": True, "prompts": True},
                    "serverInfo": {"name": self.server_name, "version": "1.0.0"},
                },
            )
        elif request.method == "tools/list":
            return MCPResponse(
                jsonrpc="2.0",
                id=request.id,
                result={
                    "tools": [
                        {
                            "name": "get_current_time",
                            "description": "Get the current date and time",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "format": {
                                        "type": "string",
                                        "description": "Time format",
                                        "default": "iso",
                                    }
                                },
                            },
                        },
                        {
                            "name": "echo",
                            "description": "Echo back the input message",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "message": {
                                        "type": "string",
                                        "description": "Message to echo",
                                    }
                                },
                                "required": ["message"],
                            },
                        },
                    ]
                },
            )
        elif request.method == "tools/call":
            tool_name = request.params.get("name")
            if tool_name == "get_current_time":
                return MCPResponse(
                    jsonrpc="2.0",
                    id=request.id,
                    result={
                        "content": [{"type": "text", "text": "2024-01-01T12:00:00Z"}]
                    },
                )
            elif tool_name == "echo":
                message = request.params.get("arguments", {}).get("message", "")
                return MCPResponse(
                    jsonrpc="2.0",
                    id=request.id,
                    result={"content": [{"type": "text", "text": f"Echo: {message}"}]},
                )

        # Default error response
        return MCPResponse(
            jsonrpc="2.0",
            id=request.id,
            error={"code": -32601, "message": "Method not found"},
        )


@pytest.fixture
def test_config():
    """Create a test configuration."""
    return Config(
        ai_providers={},
        mcp_servers=[
            MCPServerConfig(
                name="test_server",
                command=["python", "test_server.py"],
                type="stdio",
                description="Test server",
            ),
            MCPServerConfig(
                name="http_server",
                url="http://localhost:8000",
                type="http",
                description="HTTP test server",
            ),
        ],
        default_ai_provider="openai",
        default_mcp_server="test_server",
    )


@pytest.fixture
def mcp_client(test_config):
    """Create a test MCP client."""
    return MCPClient(test_config)


class TestMCPClient:
    """Test cases for MCPClient class."""

    def test_client_initialization(self, mcp_client, test_config):
        """Test MCP client initialization."""
        assert mcp_client.config == test_config
        assert isinstance(mcp_client.protocol, MCPProtocol)
        assert mcp_client.connections == {}
        assert mcp_client.initialized_servers == set()

    def test_create_connection_stdio(self, mcp_client):
        """Test creating stdio connection."""
        server_config = MCPServerConfig(
            name="test_stdio", command=["python", "test.py"], type="stdio"
        )

        with patch("egile_mcp_client.mcp.client.StdioMCPConnection") as mock_stdio:
            mcp_client._create_connection(server_config)
            mock_stdio.assert_called_once_with(["python", "test.py"])

    def test_create_connection_http(self, mcp_client):
        """Test creating HTTP connection."""
        server_config = MCPServerConfig(
            name="test_http", url="http://localhost:8000", type="http"
        )

        with patch("egile_mcp_client.mcp.client.HTTPMCPConnection") as mock_http:
            mcp_client._create_connection(server_config)
            mock_http.assert_called_once_with("http://localhost:8000")

    def test_create_connection_websocket(self, mcp_client):
        """Test creating WebSocket connection."""
        server_config = MCPServerConfig(
            name="test_ws", url="ws://localhost:8001", type="websocket"
        )

        with patch("egile_mcp_client.mcp.client.WebSocketMCPConnection") as mock_ws:
            mcp_client._create_connection(server_config)
            mock_ws.assert_called_once_with("ws://localhost:8001")

    def test_create_connection_invalid_type(self, mcp_client):
        """Test creating connection with invalid type."""
        server_config = MCPServerConfig(name="test_invalid", type="invalid")

        with pytest.raises(ValueError, match="Unsupported server type"):
            mcp_client._create_connection(server_config)

    def test_create_connection_missing_url(self, mcp_client):
        """Test creating HTTP connection without URL."""
        server_config = MCPServerConfig(name="test_http", type="http")

        with pytest.raises(ValueError, match="HTTP server test_http requires URL"):
            mcp_client._create_connection(server_config)

    def test_create_connection_missing_command(self, mcp_client):
        """Test creating stdio connection without command."""
        server_config = MCPServerConfig(name="test_stdio", type="stdio")

        with pytest.raises(
            ValueError, match="Stdio server test_stdio requires command"
        ):
            mcp_client._create_connection(server_config)

    @pytest.mark.asyncio
    async def test_connect_to_server_success(self, mcp_client):
        """Test successful server connection."""
        mock_connection = MockMCPConnection("test_server")

        with patch.object(
            mcp_client, "_create_connection", return_value=mock_connection
        ):
            await mcp_client.connect_to_server("test_server")

            assert "test_server" in mcp_client.connections
            assert mock_connection.connected
            assert mock_connection.initialized
            assert "test_server" in mcp_client.initialized_servers

    @pytest.mark.asyncio
    async def test_connect_to_server_not_found(self, mcp_client):
        """Test connecting to non-existent server."""
        with pytest.raises(
            ValueError, match="Server nonexistent not found in configuration"
        ):
            await mcp_client.connect_to_server("nonexistent")

    @pytest.mark.asyncio
    async def test_connect_to_server_already_connected(self, mcp_client):
        """Test connecting to already connected server."""
        mock_connection = MockMCPConnection("test_server")
        mock_connection.connected = True
        mcp_client.connections["test_server"] = mock_connection

        # Should not raise an error, just return early
        await mcp_client.connect_to_server("test_server")
        assert "test_server" in mcp_client.connections

    @pytest.mark.asyncio
    async def test_disconnect_from_server(self, mcp_client):
        """Test disconnecting from server."""
        mock_connection = MockMCPConnection("test_server")
        mock_connection.connected = True
        mcp_client.connections["test_server"] = mock_connection
        mcp_client.initialized_servers.add("test_server")

        await mcp_client.disconnect_from_server("test_server")

        assert "test_server" not in mcp_client.connections
        assert "test_server" not in mcp_client.initialized_servers
        assert not mock_connection.connected

    @pytest.mark.asyncio
    async def test_disconnect_from_server_not_connected(self, mcp_client):
        """Test disconnecting from non-connected server."""
        # Should not raise an error
        await mcp_client.disconnect_from_server("nonexistent")

    @pytest.mark.asyncio
    async def test_disconnect_all(self, mcp_client):
        """Test disconnecting from all servers."""
        mock_connection1 = MockMCPConnection("server1")
        mock_connection2 = MockMCPConnection("server2")

        mock_connection1.connected = True
        mock_connection2.connected = True

        mcp_client.connections["server1"] = mock_connection1
        mcp_client.connections["server2"] = mock_connection2
        mcp_client.initialized_servers.update(["server1", "server2"])

        await mcp_client.disconnect_all()

        assert len(mcp_client.connections) == 0
        assert len(mcp_client.initialized_servers) == 0
        assert not mock_connection1.connected
        assert not mock_connection2.connected

    @pytest.mark.asyncio
    async def test_list_tools_success(self, mcp_client):
        """Test listing tools from a server."""
        mock_connection = MockMCPConnection("test_server")
        mock_connection.connected = True
        mock_connection.initialized = True
        mcp_client.connections["test_server"] = mock_connection

        tools = await mcp_client.list_tools("test_server")

        assert len(tools) == 2
        assert tools[0].name == "get_current_time"
        assert tools[0].description == "Get the current date and time"
        assert tools[1].name == "echo"
        assert tools[1].description == "Echo back the input message"

    @pytest.mark.asyncio
    async def test_list_tools_not_connected(self, mcp_client):
        """Test listing tools from non-connected server (should auto-connect)."""
        # Since list_tools auto-connects, we need to mock the creation of connection
        # but make it fail to simulate a connection that can't be established
        with patch.object(
            mcp_client,
            "_create_connection",
            side_effect=RuntimeError("Connection failed"),
        ):
            with pytest.raises(RuntimeError, match="Connection failed"):
                await mcp_client.list_tools("test_server")

    @pytest.mark.asyncio
    async def test_call_tool_success(self, mcp_client):
        """Test calling a tool successfully."""
        mock_connection = MockMCPConnection("test_server")
        mock_connection.connected = True
        mock_connection.initialized = True
        mcp_client.connections["test_server"] = mock_connection

        result = await mcp_client.call_tool("test_server", "get_current_time", {})

        assert "content" in result
        assert len(result["content"]) == 1
        assert result["content"][0]["type"] == "text"
        assert result["content"][0]["text"] == "2024-01-01T12:00:00Z"

    @pytest.mark.asyncio
    async def test_call_tool_with_arguments(self, mcp_client):
        """Test calling a tool with arguments."""
        mock_connection = MockMCPConnection("test_server")
        mock_connection.connected = True
        mock_connection.initialized = True
        mcp_client.connections["test_server"] = mock_connection

        result = await mcp_client.call_tool(
            "test_server", "echo", {"message": "Hello, World!"}
        )

        assert "content" in result
        assert result["content"][0]["text"] == "Echo: Hello, World!"

    @pytest.mark.asyncio
    async def test_call_tool_not_connected(self, mcp_client):
        """Test calling tool on non-connected server (should auto-connect)."""
        # Since call_tool auto-connects, we need to mock the creation of connection
        # but make it fail to simulate a connection that can't be established
        with patch.object(
            mcp_client,
            "_create_connection",
            side_effect=RuntimeError("Connection failed"),
        ):
            with pytest.raises(RuntimeError, match="Connection failed"):
                await mcp_client.call_tool("test_server", "get_current_time", {})

    @pytest.mark.asyncio
    async def test_get_connected_servers(self, mcp_client):
        """Test getting list of connected servers."""
        mock_connection1 = MockMCPConnection("server1")
        mock_connection2 = MockMCPConnection("server2")

        mcp_client.connections["server1"] = mock_connection1
        mcp_client.connections["server2"] = mock_connection2

        connected_servers = mcp_client.get_connected_servers()

        assert set(connected_servers) == {"server1", "server2"}

    def test_get_server_config(self, mcp_client):
        """Test getting server configuration."""
        # Find the server config from the client's config
        config = None
        for server_config in mcp_client.config.mcp_servers:
            if server_config.name == "test_server":
                config = server_config
                break

        assert config is not None
        assert config.name == "test_server"
        assert config.type == "stdio"
        assert config.command == ["python", "test_server.py"]

    def test_get_server_config_not_found(self, mcp_client):
        """Test getting configuration for non-existent server."""
        config = None
        for server_config in mcp_client.config.mcp_servers:
            if server_config.name == "nonexistent":
                config = server_config
                break
        assert config is None


class TestMCPClientIntegration:
    """Integration tests for MCP client with mock server."""

    @pytest.mark.asyncio
    async def test_full_client_workflow(self, mcp_client):
        """Test complete client workflow: connect, list tools, call tool, disconnect."""
        mock_connection = MockMCPConnection("test_server")

        with patch.object(
            mcp_client, "_create_connection", return_value=mock_connection
        ):
            # Connect to server
            await mcp_client.connect_to_server("test_server")
            assert "test_server" in mcp_client.connections

            # List tools
            tools = await mcp_client.list_tools("test_server")
            assert len(tools) == 2
            assert any(tool.name == "get_current_time" for tool in tools)

            # Call tool
            result = await mcp_client.call_tool("test_server", "get_current_time", {})
            assert "content" in result

            # Disconnect
            await mcp_client.disconnect_from_server("test_server")
            assert "test_server" not in mcp_client.connections

    @pytest.mark.asyncio
    async def test_multiple_server_connections(self, test_config):
        """Test connecting to multiple servers."""
        # Add another server to config
        test_config.mcp_servers.append(
            MCPServerConfig(
                name="server2", command=["python", "server2.py"], type="stdio"
            )
        )

        client = MCPClient(test_config)
        mock_connection1 = MockMCPConnection("test_server")
        mock_connection2 = MockMCPConnection("server2")

        def mock_create_connection(server_config):
            if server_config.name == "test_server":
                return mock_connection1
            elif server_config.name == "server2":
                return mock_connection2
            else:
                raise ValueError(f"Unknown server: {server_config.name}")

        with patch.object(
            client, "_create_connection", side_effect=mock_create_connection
        ):
            # Connect to both servers
            await client.connect_to_server("test_server")
            await client.connect_to_server("server2")

            assert len(client.connections) == 2
            assert "test_server" in client.connections
            assert "server2" in client.connections

            # Disconnect all
            await client.disconnect_all()
            assert len(client.connections) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
