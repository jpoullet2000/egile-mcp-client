#!/usr/bin/env python3
"""
Simple test MCP server for testing the client.
This demonstrates a basic MCP server that the client can connect to.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional


# Mock MCP server for testing
class SimpleMCPServer:
    def __init__(self):
        self.tools = [
            {
                "name": "get_current_time",
                "description": "Get the current date and time",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "format": {
                            "type": "string",
                            "description": "Time format (iso, readable, timestamp)",
                            "default": "iso",
                        }
                    },
                },
            },
            {
                "name": "calculate",
                "description": "Perform basic arithmetic calculations",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description": "Mathematical expression to evaluate (e.g., '2 + 3 * 4')",
                        }
                    },
                    "required": ["expression"],
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
                            "description": "Message to echo back",
                        }
                    },
                    "required": ["message"],
                },
            },
        ]

        self.resources = [
            {
                "uri": "memory://system_info",
                "name": "System Information",
                "description": "Basic system information",
                "mimeType": "application/json",
            },
            {
                "uri": "memory://server_status",
                "name": "Server Status",
                "description": "Current server status and statistics",
                "mimeType": "application/json",
            },
        ]

        self.prompts = [
            {
                "name": "greeting",
                "description": "Generate a personalized greeting",
                "arguments": [
                    {
                        "name": "name",
                        "description": "Name of the person to greet",
                        "required": True,
                    }
                ],
            }
        ]

    def handle_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Handle an MCP request and return a response, or None for notifications."""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")

        # Handle notifications (no id field)
        if request_id is None:
            if method == "initialized":
                # This is a notification that initialization is complete
                return None
            else:
                # Unknown notification - just ignore it
                return None

        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}, "resources": {}, "prompts": {}},
                    "serverInfo": {"name": "simple-test-server", "version": "1.0.0"},
                },
            }

        elif method == "tools/list":
            return {"jsonrpc": "2.0", "id": request_id, "result": {"tools": self.tools}}

        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})

            if tool_name == "get_current_time":
                format_type = arguments.get("format", "iso")
                now = datetime.now()

                if format_type == "iso":
                    time_str = now.isoformat()
                elif format_type == "readable":
                    time_str = now.strftime("%Y-%m-%d %H:%M:%S")
                elif format_type == "timestamp":
                    time_str = str(now.timestamp())
                else:
                    time_str = now.isoformat()

                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": f"Current time ({format_type}): {time_str}",
                            }
                        ]
                    },
                }

            elif tool_name == "calculate":
                expression = arguments.get("expression", "")
                try:
                    # Simple and safe evaluation for basic math
                    allowed_chars = set("0123456789+-*/.() ")
                    if all(c in allowed_chars for c in expression):
                        result = eval(expression)
                        return {
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "result": {
                                "content": [
                                    {"type": "text", "text": f"{expression} = {result}"}
                                ]
                            },
                        }
                    else:
                        raise ValueError("Invalid characters in expression")
                except Exception as e:
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {"code": -32602, "message": f"Calculation error: {e}"},
                    }

            elif tool_name == "echo":
                message = arguments.get("message", "")
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{"type": "text", "text": f"Echo: {message}"}]
                    },
                }

            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"},
                }

        elif method == "resources/list":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {"resources": self.resources},
            }

        elif method == "resources/read":
            uri = params.get("uri")

            if uri == "memory://system_info":
                import platform

                system_info = {
                    "platform": platform.platform(),
                    "python_version": platform.python_version(),
                    "architecture": platform.architecture()[0],
                }
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "contents": [
                            {
                                "uri": uri,
                                "mimeType": "application/json",
                                "text": json.dumps(system_info, indent=2),
                            }
                        ]
                    },
                }

            elif uri == "memory://server_status":
                status = {
                    "status": "running",
                    "uptime": "just started",
                    "requests_handled": 0,
                    "timestamp": datetime.now().isoformat(),
                }
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "contents": [
                            {
                                "uri": uri,
                                "mimeType": "application/json",
                                "text": json.dumps(status, indent=2),
                            }
                        ]
                    },
                }

            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32602, "message": f"Resource not found: {uri}"},
                }

        elif method == "prompts/list":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {"prompts": self.prompts},
            }

        elif method == "prompts/get":
            name = params.get("name")
            arguments = params.get("arguments", {})

            if name == "greeting":
                person_name = arguments.get("name", "friend")
                prompt_text = f"Generate a warm and personalized greeting for {person_name}. Make it friendly and welcoming."

                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "description": f"Greeting prompt for {person_name}",
                        "messages": [
                            {
                                "role": "user",
                                "content": {"type": "text", "text": prompt_text},
                            }
                        ],
                    },
                }

            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32602, "message": f"Unknown prompt: {name}"},
                }

        else:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32601, "message": f"Unknown method: {method}"},
            }


def stdio_server():
    """Run the MCP server over stdio."""
    import sys

    server = SimpleMCPServer()

    while True:
        try:
            # Read line from stdin
            line = sys.stdin.readline()
            if not line:
                break

            line = line.strip()
            if not line:
                continue

            # Parse JSON request
            request = json.loads(line)

            # Handle request
            response = server.handle_request(request)

            # Send response only if there is one (requests, not notifications)
            if response is not None:
                print(json.dumps(response), flush=True)

        except json.JSONDecodeError as e:
            # Send error response
            error_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": f"Parse error: {e}"},
            }
            print(json.dumps(error_response), flush=True)
        except Exception as e:
            # Send error response
            error_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32603, "message": f"Internal error: {e}"},
            }
            print(json.dumps(error_response), flush=True)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("Simple MCP Test Server")
        print("Usage: python simple_mcp_server.py")
        print("Communicates over stdio using JSON-RPC protocol")
        sys.exit(0)

    # Setup logging to stderr so it doesn't interfere with stdio
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stderr)],
    )

    logging.info("Starting Simple MCP Server over stdio")

    try:
        stdio_server()
    except KeyboardInterrupt:
        logging.info("Server stopped")
    except Exception as e:
        logging.error(f"Server error: {e}")
        sys.exit(1)
