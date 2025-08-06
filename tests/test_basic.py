"""Test suite for the MCP client."""

import asyncio
from pathlib import Path

import pytest

from egile_mcp_client.config import (
    AIProviderConfig,
    Config,
    MCPServerConfig,
    load_config,
)


def test_config_loading():
    """Test configuration loading."""
    # Test default config
    config = Config(ai_providers={}, mcp_servers=[])
    assert config.default_ai_provider == "openai"
    assert config.web_interface.port == 8080


def test_ai_provider_config():
    """Test AI provider configuration."""
    provider_config = AIProviderConfig(api_key="test-key", model="gpt-4")
    assert provider_config.api_key == "test-key"
    assert provider_config.model == "gpt-4"
    assert provider_config.temperature == 0.7


def test_mcp_server_config():
    """Test MCP server configuration."""
    server_config = MCPServerConfig(
        name="test-server", url="http://localhost:8000", type="http"
    )
    assert server_config.name == "test-server"
    assert server_config.url == "http://localhost:8000"
    assert server_config.type == "http"


@pytest.mark.asyncio
async def test_mcp_protocol():
    """Test MCP protocol message handling."""
    from egile_mcp_client.mcp.protocol import MCPProtocol, MCPRequest

    protocol = MCPProtocol()

    # Test request creation
    request = protocol.create_request("test/method", {"param": "value"})
    assert isinstance(request, MCPRequest)
    assert request.method == "test/method"
    assert request.params == {"param": "value"}

    # Test serialization
    serialized = protocol.serialize_message(request)
    assert "test/method" in serialized

    # Test parsing
    parsed = protocol.parse_message(serialized)
    assert parsed.method == "test/method"
    assert parsed.params == {"param": "value"}


if __name__ == "__main__":
    pytest.main([__file__])
