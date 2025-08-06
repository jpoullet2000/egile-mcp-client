# Configuration

This guide covers all configuration options for Egile MCP Client, from basic setup to advanced customization.

## Configuration Files

Egile MCP Client uses a hierarchical configuration system:

1. **config.yaml** - Main configuration file
2. **.env** - Environment variables (optional)
3. **Environment variables** - Runtime overrides
4. **Command-line arguments** - Highest priority

## Configuration File Structure

### Complete Configuration Example

```yaml
# AI Providers (for agent mode)
ai_providers:
  openai:
    api_key: "your-openai-api-key-here"
    model: "gpt-4"
    temperature: 0.7
    max_tokens: 2000
    base_url: null  # Optional: custom OpenAI-compatible endpoint
    timeout: 30
  
  anthropic:
    api_key: "your-anthropic-api-key-here"
    model: "claude-3-sonnet-20240229"
    temperature: 0.7
    max_tokens: 2000
    timeout: 30
  
  xai:
    api_key: "your-xai-api-key-here"
    model: "grok-beta"
    temperature: 0.7
    max_tokens: 2000
    timeout: 30

# MCP Servers configuration
mcp_servers:
  # HTTP server example
  - name: "web_search"
    url: "http://localhost:8000"
    type: "http"
    description: "Web search MCP server"
    headers:
      Authorization: "Bearer your-token"
      Custom-Header: "value"
    timeout: 30
    retry_attempts: 3
  
  # Stdio server example
  - name: "local_tools"
    command: ["python", "/path/to/server/main.py"]
    type: "stdio"
    description: "Local tools server"
    working_directory: "/path/to/server"
    environment:
      TOOL_CONFIG: "/path/to/config"
      DEBUG: "true"
  
  # WebSocket server example
  - name: "realtime_data"
    url: "ws://localhost:8001"
    type: "websocket"
    description: "Real-time data server"
    headers:
      Authentication: "Bearer token"
    ping_interval: 20
    ping_timeout: 10

# Default settings
default_ai_provider: "openai"
default_mcp_server: "web_search"

# Web interface configuration
web_interface:
  host: "localhost"
  port: 8080
  title: "Egile MCP Client"
  max_history_messages: 1000
  enable_cors: true
  cors_origins: 
    - "http://localhost:3000"
    - "https://yourdomain.com"
  static_files_dir: "static"
  templates_dir: "templates"

# Logging configuration
logging:
  level: "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: "logs/egile_mcp_client.log"
  max_file_size: "10MB"
  backup_count: 5
  console_output: true

# Security settings
security:
  max_request_size: "10MB"
  rate_limit:
    enabled: true
    requests_per_minute: 60
  allowed_hosts:
    - "localhost"
    - "127.0.0.1"

# Performance settings
performance:
  connection_pool_size: 10
  request_timeout: 30
  max_concurrent_requests: 5
  cache:
    enabled: true
    ttl: 300  # seconds
    max_size: 1000

# Feature flags
features:
  conversation_history: true
  auto_save_conversations: true
  tool_validation: true
  async_tool_calls: true
```

## AI Providers Configuration

### OpenAI Configuration

```yaml
ai_providers:
  openai:
    api_key: "${OPENAI_API_KEY}"  # Environment variable reference
    model: "gpt-4-turbo-preview"
    temperature: 0.7
    max_tokens: 4000
    top_p: 1.0
    frequency_penalty: 0.0
    presence_penalty: 0.0
    base_url: null  # For OpenAI-compatible APIs
    organization: null  # Optional organization ID
    timeout: 60
```

**Available Models:**
- `gpt-4-turbo-preview`
- `gpt-4`
- `gpt-3.5-turbo`
- Custom models for compatible APIs

### Anthropic Configuration

```yaml
ai_providers:
  anthropic:
    api_key: "${ANTHROPIC_API_KEY}"
    model: "claude-3-opus-20240229"
    temperature: 0.7
    max_tokens: 4000
    top_p: 1.0
    timeout: 60
```

**Available Models:**
- `claude-3-opus-20240229`
- `claude-3-sonnet-20240229` 
- `claude-3-haiku-20240307`

### xAI Configuration

```yaml
ai_providers:
  xai:
    api_key: "${XAI_API_KEY}"
    model: "grok-beta"
    temperature: 0.7
    max_tokens: 4000
    timeout: 60
```

## MCP Servers Configuration

### HTTP Servers

```yaml
mcp_servers:
  - name: "api_server"
    url: "https://api.example.com/mcp"
    type: "http"
    description: "External API server"
    headers:
      Authorization: "Bearer ${API_TOKEN}"
      User-Agent: "EgileMCPClient/0.1.0"
    timeout: 30
    retry_attempts: 3
    verify_ssl: true
```

### Stdio Servers

```yaml
mcp_servers:
  - name: "local_server"
    command: ["python", "-m", "my_mcp_server"]
    type: "stdio"
    description: "Local Python server"
    working_directory: "/path/to/server"
    environment:
      PYTHONPATH: "/custom/path"
      CONFIG_FILE: "config.json"
    timeout: 60
```

### WebSocket Servers

```yaml
mcp_servers:
  - name: "ws_server"
    url: "wss://secure.example.com/mcp"
    type: "websocket"
    description: "Secure WebSocket server"
    headers:
      Origin: "https://yourdomain.com"
    ping_interval: 30
    ping_timeout: 10
    max_message_size: 1048576  # 1MB
```

## Environment Variables

You can override any configuration value using environment variables:

```bash
# AI Provider settings
export OPENAI_API_KEY="your-key"
export ANTHROPIC_API_KEY="your-key"
export XAI_API_KEY="your-key"

# Default settings
export MCP_DEFAULT_AI_PROVIDER="anthropic"
export MCP_DEFAULT_SERVER="local_tools"

# Web interface
export MCP_WEB_HOST="0.0.0.0"
export MCP_WEB_PORT="9000"

# Logging
export MCP_LOG_LEVEL="DEBUG"
export MCP_LOG_FILE="custom.log"

# Custom config file location
export MCP_CLIENT_CONFIG="/custom/path/config.yaml"
```

## .env File Support

Create a `.env` file in your project directory:

```bash
# .env file
OPENAI_API_KEY=your-openai-key-here
ANTHROPIC_API_KEY=your-anthropic-key-here
MCP_LOG_LEVEL=DEBUG
MCP_WEB_PORT=8080
```

## Configuration Validation

The client validates your configuration on startup. Common validation errors:

### Missing Required Fields
```
Error: ai_providers.openai.api_key is required when using OpenAI
```

### Invalid Values
```
Error: web_interface.port must be between 1 and 65535
```

### Server Configuration Issues
```
Error: mcp_servers[0].url is not a valid URL
```

## Dynamic Configuration

### Runtime Configuration Updates

Some settings can be updated at runtime:

```python
from egile_mcp_client.config import Config

config = Config.load()
config.logging.level = "DEBUG"
config.save()
```

### Configuration Reloading

The web interface supports configuration reloading:

```bash
# Send SIGHUP to reload configuration
kill -HUP $(pgrep -f "egile-mcp-client web")
```

## Security Considerations

### API Key Security

1. **Never commit API keys to version control**
2. **Use environment variables or .env files**
3. **Restrict file permissions**:
   ```bash
   chmod 600 config.yaml
   chmod 600 .env
   ```

### Network Security

```yaml
security:
  # Restrict allowed hosts
  allowed_hosts:
    - "localhost"
    - "your-domain.com"
  
  # Enable rate limiting
  rate_limit:
    enabled: true
    requests_per_minute: 100
  
  # Set maximum request sizes
  max_request_size: "5MB"
```

### SSL/TLS Configuration

```yaml
mcp_servers:
  - name: "secure_server"
    url: "https://secure.example.com/mcp"
    type: "http"
    verify_ssl: true
    ssl_cert_path: "/path/to/cert.pem"
    ssl_key_path: "/path/to/key.pem"
```

## Configuration Profiles

You can maintain multiple configuration profiles:

```bash
# Development profile
egile-mcp-client --config config.dev.yaml agent

# Production profile  
egile-mcp-client --config config.prod.yaml web

# Testing profile
egile-mcp-client --config config.test.yaml direct
```

## Troubleshooting Configuration

### Validate Configuration

```bash
# Check configuration syntax
egile-mcp-client config validate

# Show current configuration
egile-mcp-client config show

# Test server connections (test connectivity by listing tools)
egile-mcp-client tools
```

### Common Issues

1. **YAML Syntax Errors**: Use a YAML validator
2. **Environment Variable Issues**: Check variable names and values
3. **File Permissions**: Ensure configuration files are readable
4. **Network Connectivity**: Test server URLs independently

### Debug Mode

Enable debug mode for detailed configuration information:

```bash
export MCP_LOG_LEVEL=DEBUG
egile-mcp-client --config config.yaml agent
```

This will show:
- Configuration loading process
- Environment variable resolution
- Server connection attempts
- Detailed error messages
