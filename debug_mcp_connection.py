#!/usr/bin/env python3
"""Debug script to test MCP server stdio connection."""

import json
import subprocess
import sys
import uuid


def test_mcp_server():
    """Test the MCP server directly via stdio."""
    print("Starting MCP server...")

    # Start the server process
    process = subprocess.Popen(
        ["python", "simple_mcp_server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=0,
    )

    print("Server started, sending initialize request...")

    # Create initialize request
    request = {
        "jsonrpc": "2.0",
        "id": str(uuid.uuid4()),
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}, "resources": {}, "prompts": {}},
            "clientInfo": {"name": "test-client", "version": "1.0.0"},
        },
    }

    # Send request
    request_json = json.dumps(request)
    print(f"Sending: {request_json}")

    process.stdin.write(request_json + "\n")
    process.stdin.flush()

    # Read response
    print("Waiting for response...")
    try:
        response_line = process.stdout.readline()
        if response_line:
            print(f"Received: {response_line.strip()}")
            response = json.loads(response_line.strip())

            if "result" in response:
                print("✅ Initialize successful!")

                # Send initialized notification
                notification = {"jsonrpc": "2.0", "method": "initialized", "params": {}}

                notification_json = json.dumps(notification)
                print(f"Sending notification: {notification_json}")

                process.stdin.write(notification_json + "\n")
                process.stdin.flush()

                # Test tools/list
                tools_request = {
                    "jsonrpc": "2.0",
                    "id": str(uuid.uuid4()),
                    "method": "tools/list",
                    "params": {},
                }

                tools_json = json.dumps(tools_request)
                print(f"Sending tools request: {tools_json}")

                process.stdin.write(tools_json + "\n")
                process.stdin.flush()

                # Read tools response
                tools_response_line = process.stdout.readline()
                if tools_response_line:
                    print(f"Tools response: {tools_response_line.strip()}")
                    tools_response = json.loads(tools_response_line.strip())
                    if "result" in tools_response:
                        tools = tools_response["result"].get("tools", [])
                        print(f"✅ Found {len(tools)} tools:")
                        for tool in tools:
                            print(f"  - {tool['name']}: {tool['description']}")

            else:
                print(f"❌ Initialize failed: {response}")
        else:
            print("❌ No response received")

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        # Check for stderr output
        stderr_output = process.stderr.read()
        if stderr_output:
            print(f"Server stderr: {stderr_output}")

        # Cleanup
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()

        print("Server terminated")


if __name__ == "__main__":
    test_mcp_server()
