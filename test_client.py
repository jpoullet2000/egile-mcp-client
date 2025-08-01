#!/usr/bin/env python3
"""Debug script to test the full MCP client connection."""

import asyncio
import logging
from egile_mcp_client.config import load_config
from egile_mcp_client.mcp.client import MCPClient

# Enable debug logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


async def test_client_connection():
    """Test the MCP client connection."""
    print("Loading config...")
    config = load_config()

    print("Creating MCP client...")
    client = MCPClient(config)

    try:
        print("Attempting to connect to simple_test_server...")
        await client.connect_to_server("simple_test_server")
        print("✅ Connected successfully!")

        print("Listing tools...")
        tools = await client.list_tools("simple_test_server")
        print(f"✅ Found {len(tools)} tools:")
        for tool in tools:
            print(f"  - {tool.name}: {tool.description}")

        print("Testing tool call...")
        result = await client.call_tool("simple_test_server", "get_current_time", {})
        print(f"✅ Tool result: {result}")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()
    finally:
        print("Disconnecting...")
        await client.disconnect_all()
        print("Disconnected")


if __name__ == "__main__":
    asyncio.run(test_client_connection())
