# Troubleshooting Guide

This guide helps you resolve common issues you might encounter when using Egile MCP Client.

## Installation Issues

### Python Version Compatibility

**Problem**: Getting errors about Python version compatibility.

**Solution**:
```bash
# Check your Python version
python --version

# Egile MCP Client requires Python 3.10+
# If you have an older version, install Python 3.10+ or use pyenv
pyenv install 3.11.0
pyenv local 3.11.0
```

### Poetry Installation Issues

**Problem**: Poetry commands not working or poetry not found.

**Solution**:
```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH (add to your shell profile)
export PATH="$HOME/.local/bin:$PATH"

# Verify installation
poetry --version
```

### Dependency Conflicts

**Problem**: Conflicting dependencies during installation.

**Solution**:
```bash
# Clear Poetry cache
poetry cache clear pypi --all

# Update lock file
poetry lock --no-update

# Install with verbose output to see what's happening
poetry install -vvv
```

## Configuration Issues

### Invalid Configuration File

**Problem**: "Configuration validation failed" error.

**Solutions**:

1. **Check YAML syntax**:
   ```bash
   # Use a YAML validator
   python -c "import yaml; yaml.safe_load(open('config.yaml'))"
   ```

2. **Validate configuration**:
   ```bash
   egile-mcp-client config validate
   ```

3. **Use the example configuration**:
   ```bash
   cp config.example.yaml config.yaml
   # Edit config.yaml with your settings
   ```

### Environment Variables Not Loading

**Problem**: Environment variables not being recognized.

**Solutions**:

1. **Check variable names**:
   ```bash
   # Ensure correct naming
   export OPENAI_API_KEY="your-key"
   export ANTHROPIC_API_KEY="your-key"
   
   # Verify they're set
   echo $OPENAI_API_KEY
   ```

2. **Use .env file**:
   ```bash
   # Create .env file in project root
   echo "OPENAI_API_KEY=your-key" > .env
   echo "ANTHROPIC_API_KEY=your-key" >> .env
   ```

3. **Check file permissions**:
   ```bash
   chmod 600 .env
   chmod 600 config.yaml
   ```

### API Key Issues

**Problem**: "No API key found" or authentication errors.

**Solutions**:

1. **Verify API key format**:
   - OpenAI: starts with `sk-`
   - Anthropic: starts with `sk-ant-`
   - xAI: check xAI documentation for format

2. **Test API key**:
   ```bash
   # Test OpenAI key
   curl -H "Authorization: Bearer $OPENAI_API_KEY" \
        https://api.openai.com/v1/models
   
   # Test Anthropic key
   curl -H "Authorization: Bearer $ANTHROPIC_API_KEY" \
        https://api.anthropic.com/v1/messages
   ```

3. **Check key permissions**:
   - Ensure the API key has necessary permissions
   - Check account billing status
   - Verify rate limits

## Connection Issues

### MCP Server Connection Failed

**Problem**: Cannot connect to MCP server.

**Diagnostic Steps**:

1. **Check server status**:
   ```bash
   # For HTTP servers
   curl -I http://localhost:8000/health
   
   # For WebSocket servers
   wscat -c ws://localhost:8001
   
   # Check if process is running
   ps aux | grep mcp-server
   ```

2. **Verify configuration**:
   ```bash
   egile-mcp-client tools --server server_name
   egile-mcp-client config show
   ```

3. **Check network connectivity**:
   ```bash
   # Test basic connectivity
   telnet localhost 8000
   
   # Check firewall rules
   sudo ufw status
   ```

### WebSocket Connection Issues

**Problem**: WebSocket connections dropping or failing.

**Solutions**:

1. **Increase timeout values**:
   ```yaml
   # In config.yaml
   mcp_servers:
     - name: "ws_server"
       url: "ws://localhost:8001"
       type: "websocket"
       ping_interval: 30
       ping_timeout: 10
       timeout: 60
   ```

2. **Check proxy settings**:
   ```bash
   # Disable proxy for WebSocket connections
   unset http_proxy
   unset https_proxy
   ```

3. **Enable debug logging**:
   ```bash
   export MCP_LOG_LEVEL=DEBUG
   egile-mcp-client direct --server ws_server
   ```

### Stdio Connection Issues

**Problem**: Local stdio servers not starting or responding.

**Solutions**:

1. **Check command path**:
   ```yaml
   # Use absolute paths
   mcp_servers:
     - name: "local_server"
       command: ["/usr/bin/python", "/full/path/to/server.py"]
       type: "stdio"
   ```

2. **Verify permissions**:
   ```bash
   # Make sure the script is executable
   chmod +x /path/to/server.py
   
   # Check if Python can import required modules
   /usr/bin/python -c "import server_module"
   ```

3. **Check working directory**:
   ```yaml
   mcp_servers:
     - name: "local_server"
       command: ["python", "server.py"]
       type: "stdio"
       working_directory: "/path/to/server/directory"
   ```

## Runtime Issues

### High Memory Usage

**Problem**: Client consuming too much memory.

**Solutions**:

1. **Limit conversation history**:
   ```yaml
   web_interface:
     max_history_messages: 100  # Reduce from default 1000
   ```

2. **Enable garbage collection**:
   ```python
   import gc
   gc.collect()  # Force garbage collection
   ```

3. **Use connection pooling limits**:
   ```yaml
   performance:
     connection_pool_size: 5  # Reduce pool size
     max_concurrent_requests: 3
   ```

### Slow Response Times

**Problem**: Slow responses from AI agents or MCP servers.

**Solutions**:

1. **Optimize timeout settings**:
   ```yaml
   ai_providers:
     openai:
       timeout: 30  # Reduce timeout
   
   mcp_servers:
     - timeout: 15  # Reduce server timeout
   ```

2. **Enable caching**:
   ```yaml
   performance:
     cache:
       enabled: true
       ttl: 300
       max_size: 1000
   ```

3. **Use concurrent requests**:
   ```python
   # In programmatic usage
   import asyncio
   
   async def concurrent_calls():
       tasks = [
           client.call_tool("tool1", params1),
           client.call_tool("tool2", params2)
       ]
       results = await asyncio.gather(*tasks)
       return results
   ```

### Tool Execution Errors

**Problem**: MCP tools failing to execute or returning errors.

**Diagnostic Steps**:

1. **Test tool directly**:
   ```bash
   egile-mcp-client tools test --server server_name --tool tool_name --args '{}'
   ```

2. **Check tool parameters**:
   ```bash
   egile-mcp-client tools describe --server server_name --tool tool_name
   ```

3. **Validate JSON parameters**:
   ```bash
   # Use a JSON validator
   echo '{"param": "value"}' | python -m json.tool
   ```

## Web Interface Issues

### Port Already in Use

**Problem**: Web interface fails to start with "Port already in use" error.

**Solutions**:

1. **Use a different port**:
   ```bash
   egile-mcp-client web --port 8081
   ```

2. **Kill process using the port**:
   ```bash
   # Find process using port 8080
   lsof -i :8080
   
   # Kill the process
   kill -9 <PID>
   ```

3. **Change default port in config**:
   ```yaml
   web_interface:
     port: 8081
   ```

### WebSocket Connection Failed in Browser

**Problem**: Browser console shows WebSocket connection errors.

**Solutions**:

1. **Check CORS settings**:
   ```yaml
   web_interface:
     enable_cors: true
     cors_origins:
       - "http://localhost:3000"
       - "https://yourdomain.com"
   ```

2. **Use correct WebSocket URL**:
   ```javascript
   // In browser console, check the WebSocket URL
   new WebSocket('ws://localhost:8080/ws')
   ```

3. **Check browser security settings**:
   - Some browsers block WebSocket connections over HTTP
   - Try using HTTPS or disable security restrictions for development

## Performance Issues

### Memory Leaks

**Problem**: Memory usage continuously increasing.

**Solutions**:

1. **Check for unclosed connections**:
   ```python
   # Always use context managers
   async with MCPClient(config) as client:
       # Client will automatically clean up
       pass
   ```

2. **Monitor connection pools**:
   ```bash
   egile-mcp-client monitor --server server_name
   ```

3. **Enable debug logging to track resources**:
   ```bash
   export MCP_LOG_LEVEL=DEBUG
   egile-mcp-client web
   ```

### High CPU Usage

**Problem**: Client using too much CPU.

**Solutions**:

1. **Reduce polling frequency**:
   ```yaml
   web_interface:
     polling_interval: 5000  # Increase from default
   ```

2. **Limit concurrent operations**:
   ```yaml
   performance:
     max_concurrent_requests: 2
   ```

3. **Profile the application**:
   ```bash
   python -m cProfile -o profile.stats -m egile_mcp_client.cli web
   ```

## Debugging Tips

### Enable Debug Mode

```bash
# Set debug log level
export MCP_LOG_LEVEL=DEBUG

# Enable verbose output
egile-mcp-client --verbose chat

# Check logs
tail -f logs/egile_mcp_client.log
```

### Common Debug Commands

```bash
# Test configuration
egile-mcp-client config validate
egile-mcp-client config show

# Test server connections
egile-mcp-client tools --server server_name

# List all available tools
egile-mcp-client tools

# Check system status
egile-mcp-client status
egile-mcp-client version
```

### Log Analysis

```bash
# Filter logs by level
grep "ERROR" logs/egile_mcp_client.log

# Show recent errors
tail -n 50 logs/egile_mcp_client.log | grep ERROR

# Monitor logs in real-time
tail -f logs/egile_mcp_client.log | grep -E "(ERROR|WARNING)"
```

## Getting Additional Help

### Before Reporting Issues

1. **Update to latest version**:
   ```bash
   pip install --upgrade egile-mcp-client
   ```

2. **Check known issues**:
   - Review GitHub issues
   - Check changelog for recent fixes

3. **Gather debug information**:
   ```bash
   egile-mcp-client debug-info > debug.txt
   ```

### Creating Bug Reports

Include the following information:

- **Environment details**: OS, Python version, client version
- **Configuration**: Sanitized config file (remove API keys)
- **Steps to reproduce**: Exact commands and inputs
- **Expected vs actual behavior**
- **Error messages**: Full error output and logs
- **Debug information**: Output from debug commands

### Community Resources

- **Documentation**: https://egile-mcp-client.readthedocs.io
- **GitHub Issues**: https://github.com/jpoullet2000/egile-mcp-client/issues
- **Discussions**: https://github.com/jpoullet2000/egile-mcp-client/discussions
