# Architecture

This document describes the architecture and design principles of Egile MCP Client, providing insights into its modular structure, component interactions, and extensibility features.

## Overview

Egile MCP Client is designed with a modular, extensible architecture that separates concerns and enables easy customization and extension. The architecture follows these key principles:

- **Separation of Concerns**: Each module has a specific responsibility
- **Dependency Injection**: Components are loosely coupled through interfaces
- **Async-First**: Built for asynchronous operations from the ground up
- **Extensibility**: Plugin architecture for custom agents and connections
- **Type Safety**: Comprehensive type hints throughout the codebase

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interfaces                         │
├─────────────┬─────────────────┬─────────────────────────────┤
│     CLI     │   Web Interface │    Programmatic API         │
│   (Click)   │    (FastAPI)    │     (Python SDK)            │
└─────────────┴─────────────────┴─────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                     Core Layer                             │
├─────────────────────┬───────────────────────────────────────┤
│    Agent Manager    │         MCP Client Manager           │
│   (AI Providers)    │       (Server Connections)           │
└─────────────────────┴───────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                 Protocol & Transport Layer                 │
├─────────────┬─────────────┬─────────────┬─────────────────────┤
│    HTTP     │  WebSocket  │    Stdio    │     Protocol        │
│ Connection  │ Connection  │ Connection  │     Handler         │
└─────────────┴─────────────┴─────────────┴─────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                   Utilities & Support                      │
├─────────────┬─────────────┬─────────────┬─────────────────────┤
│   Config    │   Logging   │   History   │     Security        │
│  Manager    │   System    │   Manager   │     Features        │
└─────────────┴─────────────┴─────────────┴─────────────────────┘
```

## Component Architecture

### 1. User Interface Layer

#### Command Line Interface (CLI)
- **Framework**: Click
- **Location**: `egile_mcp_client/cli.py`
- **Responsibilities**:
  - Command parsing and validation
  - User interaction management
  - Output formatting
  - Error handling and user feedback

```text
# CLI Architecture
┌─────────────────┐
│   CLI Router    │
│   (click.Group) │
├─────────────────┤
│ Commands:       │
│ - agent         │
│ - direct        │
│ - tools         │
│ - web           │
│ - config        │
└─────────────────┘
```

#### Web Interface
- **Framework**: FastAPI + Jinja2
- **Location**: `egile_mcp_client/web/`
- **Components**:
  - **FastAPI App** (`app.py`): ASGI application
  - **Routes** (`routes.py`): API endpoints
  - **Templates**: HTML templates for UI
  - **Static Files**: CSS, JavaScript, assets

```text
# Web Architecture
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI App   │────│   API Routes    │────│   WebSocket     │
│                 │    │                 │    │   Handler       │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ - CORS          │    │ - /chat         │    │ - Real-time     │
│ - Middleware    │    │ - /tools        │    │   chat          │
│ - Static files  │    │ - /servers      │    │ - Server events │
│ - Templates     │    │ - /config       │    │ - Status        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

#### Programmatic API
- **Purpose**: Python SDK for integration
- **Design**: Context managers and async interfaces
- **Type Safety**: Full type hint coverage

### 2. Core Layer

#### Agent Manager
- **Location**: `egile_mcp_client/agents/`
- **Design Pattern**: Strategy Pattern
- **Responsibilities**:
  - AI provider abstraction
  - Message handling and conversion
  - Tool integration
  - Response processing

```text
# Agent Architecture
┌─────────────────┐
│   BaseAgent     │
│  (Abstract)     │
├─────────────────┤
│ + chat()        │
│ + stream_chat() │
│ + list_models() │
└─────────────────┘
         ▲
         │
┌─────────────────┬─────────────────┬─────────────────┐
│  OpenAIAgent    │ AnthropicAgent  │   XAIAgent      │
├─────────────────┼─────────────────┼─────────────────┤
│ - OpenAI API    │ - Anthropic API │ - xAI API       │
│ - GPT models    │ - Claude models │ - Grok models   │
│ - Function calls│ - Tool use      │ - Tool calling  │
└─────────────────┴─────────────────┴─────────────────┘
```

#### MCP Client Manager
- **Location**: `egile_mcp_client/mcp/`
- **Design Pattern**: Factory + Adapter Pattern
- **Components**:
  - **Client** (`client.py`): Main MCP client interface
  - **Connection Manager** (`connection.py`): Connection lifecycle
  - **Protocol Handler** (`protocol.py`): MCP protocol implementation

```text
# MCP Client Architecture
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   MCPClient     │────│ ConnectionMgr   │────│ ProtocolHandler │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ - connect()     │    │ - create_conn() │    │ - encode_msg()  │
│ - list_tools()  │    │ - manage_pool() │    │ - decode_msg()  │
│ - call_tool()   │    │ - health_check()│    │ - validate()    │
│ - disconnect()  │    │ - reconnect()   │    │ - serialize()   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 3. Protocol & Transport Layer

#### Connection Types

##### HTTP Connection
- **Use Case**: REST-like MCP servers
- **Features**:
  - Request/response pattern
  - Connection pooling
  - Retry mechanisms
  - SSL/TLS support

##### WebSocket Connection
- **Use Case**: Real-time, bidirectional communication
- **Features**:
  - Persistent connections
  - Server-initiated messages
  - Ping/pong heartbeat
  - Automatic reconnection

##### Stdio Connection
- **Use Case**: Local process communication
- **Features**:
  - Process lifecycle management
  - Environment variable handling
  - Working directory support
  - Graceful shutdown

```text
# Connection Architecture
┌─────────────────┐
│  BaseConnection │
│   (Abstract)    │
├─────────────────┤
│ + connect()     │
│ + send()        │
│ + receive()     │
│ + disconnect()  │
└─────────────────┘
         ▲
         │
┌─────────────────┬─────────────────┬─────────────────┐
│ HTTPConnection  │  WSConnection   │ StdioConnection │
├─────────────────┼─────────────────┼─────────────────┤
│ - httpx.Client  │ - websockets    │ - subprocess    │
│ - Connection    │ - Auto-reconnect│ - Process mgmt  │
│   pooling       │ - Ping/pong     │ - Env vars      │
│ - Retry logic   │ - Message queue │ - Working dir   │
└─────────────────┴─────────────────┴─────────────────┘
```

### 4. Protocol Implementation

#### MCP Protocol Handling
The client implements the Model Context Protocol specification:

```text
# Protocol Message Types
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│    Requests     │    │    Responses    │    │     Events      │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ - initialize    │    │ - success       │    │ - server_status │
│ - list_tools    │    │ - error         │    │ - tool_update   │
│ - call_tool     │    │ - progress      │    │ - notification  │
│ - list_prompts  │    │ - partial       │    │ - log_message   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

#### Message Flow
```
Client                           Server
  │                               │
  ├─── initialize ────────────────→│
  │←─── initialize_response ──────┤
  │                               │
  ├─── list_tools ───────────────→│
  │←─── tools_list ───────────────┤
  │                               │
  ├─── call_tool ────────────────→│
  │←─── tool_response ────────────┤
```

### 5. Utilities & Support Layer

#### Configuration Management
- **Location**: `egile_mcp_client/config.py`
- **Features**:
  - YAML configuration files
  - Environment variable support
  - Configuration validation
  - Hot reloading capabilities

```text
# Configuration Architecture
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  ConfigLoader   │────│   Validator     │────│   Environment   │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ - load_yaml()   │    │ - validate()    │    │ - resolve_vars()│
│ - merge_env()   │    │ - check_types() │    │ - expand_paths()│
│ - watch_files() │    │ - validate_net()│    │ - load_dotenv() │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

#### Logging System
- **Location**: `egile_mcp_client/utils/logging.py`
- **Features**:
  - Structured logging
  - Multiple output targets
  - Log rotation
  - Performance metrics

#### History Management
- **Location**: `egile_mcp_client/utils/history.py`
- **Features**:
  - Conversation persistence
  - Search capabilities
  - Export functionality
  - Privacy controls

## Data Flow

### 1. Direct Mode Flow
```
User Input → CLI/Web → MCPClient → Connection → MCP Server
                                     ↓
User Output ← CLI/Web ← Response ← Protocol ← Server Response
```

### 2. Agent Mode Flow
```
User Input → CLI/Web → AgentClient → AI Agent → Tool Selection
                                        ↓
                                   MCPClient → Connection → MCP Server
                                        ↓
                         AI Processing ← Tool Results ← Server Response
                              ↓
User Output ← CLI/Web ← Natural Language Response
```

## Extension Points

### 1. Custom Agents
Implement the `BaseAgent` interface to create custom AI agents:

```python
from egile_mcp_client.agents.base import BaseAgent

class CustomAgent(BaseAgent):
    async def chat(self, message: str, tools: List[Tool]) -> Message:
        # Custom logic here
        pass
```

### 2. Custom Connections
Implement the `BaseConnection` interface for custom transport protocols:

```python
from egile_mcp_client.mcp.connection import BaseConnection

class CustomConnection(BaseConnection):
    async def connect(self) -> None:
        # Custom connection logic
        pass
```

### 3. Middleware
Add custom middleware for request/response processing:

```python
from egile_mcp_client.middleware import BaseMiddleware

class CustomMiddleware(BaseMiddleware):
    async def process_request(self, request):
        # Pre-processing
        return request
    
    async def process_response(self, response):
        # Post-processing
        return response
```

## Security Architecture

### 1. Authentication & Authorization
- API key management
- Token-based authentication
- Role-based access control (future)

### 2. Input Validation
- Request sanitization
- Parameter validation
- Type checking
- Size limits

### 3. Network Security
- SSL/TLS enforcement
- Certificate validation
- Connection encryption
- Rate limiting

### 4. Data Protection
- Conversation encryption at rest
- PII detection and redaction
- Audit logging
- Secure key storage

## Performance Considerations

### 1. Connection Management
- Connection pooling
- Keep-alive connections
- Graceful degradation
- Circuit breaker pattern

### 2. Caching Strategy
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   L1 Cache  │    │   L2 Cache  │    │  Persistent │
│  (Memory)   │    │   (Redis)   │    │   Storage   │
├─────────────┤    ├─────────────┤    ├─────────────┤
│ - Tool defs │    │ - Responses │    │ - Config    │
│ - Server    │    │ - Sessions  │    │ - History   │
│   metadata  │    │ - User data │    │ - Logs      │
└─────────────┘    └─────────────┘    └─────────────┘
```

### 3. Async Processing
- Non-blocking I/O
- Concurrent tool calls
- Streaming responses
- Background tasks

## Error Handling Strategy

### 1. Error Hierarchy
```text
MCPException
├── MCPConnectionError
│   ├── ConnectionTimeoutError
│   ├── ConnectionRefusedError
│   └── ConnectionLostError
├── MCPProtocolError
│   ├── InvalidMessageError
│   ├── UnsupportedVersionError
│   └── ProtocolViolationError
├── MCPToolError
│   ├── ToolNotFoundError
│   ├── ToolExecutionError
│   └── ToolTimeoutError
└── MCPConfigError
    ├── ConfigValidationError
    ├── ConfigNotFoundError
    └── ConfigParseError
```

### 2. Recovery Mechanisms
- Automatic retry with exponential backoff
- Connection re-establishment
- Graceful degradation
- Fallback strategies

## Testing Architecture

### 1. Test Structure
```
tests/
├── unit/
│   ├── test_agents/
│   ├── test_mcp/
│   ├── test_config/
│   └── test_utils/
├── integration/
│   ├── test_e2e/
│   ├── test_web/
│   └── test_cli/
└── fixtures/
    ├── mock_servers/
    ├── test_configs/
    └── sample_data/
```

### 2. Testing Strategies
- **Unit Tests**: Component isolation with mocks
- **Integration Tests**: Real MCP server interactions
- **End-to-End Tests**: Full workflow testing
- **Performance Tests**: Load and stress testing

## Deployment Architecture

### 1. Packaging
- PyPI distribution
- Docker containers
- Conda packages
- Platform-specific installers

### 2. Configuration Management
- Environment-specific configs
- Secret management
- Feature flags
- A/B testing support

This architecture provides a solid foundation for building robust, scalable MCP client applications while maintaining flexibility for future enhancements and customizations.
