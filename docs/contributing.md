# Contributing to Egile MCP Client

Thank you for your interest in contributing to Egile MCP Client! This guide will help you get started with contributing to the project.

## Getting Started

### Prerequisites

- **Python 3.10+**: Ensure you have Python 3.10 or higher installed
- **Poetry**: We use Poetry for dependency management
- **Git**: For version control and contributing changes

### Development Setup

1. **Fork and Clone the Repository**
   ```bash
   # Fork the repository on GitHub first, then clone your fork
   git clone https://github.com/YOUR_USERNAME/egile-mcp-client.git
   cd egile-mcp-client
   
   # Add the upstream repository
   git remote add upstream https://github.com/jpoullet2000/egile-mcp-client.git
   ```

2. **Install Development Dependencies**
   ```bash
   # Install Poetry if you haven't already
   curl -sSL https://install.python-poetry.org | python3 -
   
   # Install project dependencies
   poetry install
   
   # Activate the virtual environment
   poetry shell
   ```

3. **Install Pre-commit Hooks**
   ```bash
   # Install pre-commit hooks for code quality
   pre-commit install
   ```

4. **Verify Setup**
   ```bash
   # Run tests to ensure everything is working
   pytest
   
   # Check code formatting
   black --check .
   
   # Check linting
   flake8
   
   # Check type hints
   mypy egile_mcp_client/
   ```

## Development Workflow

### 1. Create a Feature Branch

```bash
# Update your main branch
git checkout main
git pull upstream main

# Create a new feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/bug-description
```

### 2. Make Your Changes

- Write clear, concise code
- Follow the existing code style
- Add or update tests for your changes
- Update documentation as needed
- Add type hints to all new code

### 3. Test Your Changes

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=egile_mcp_client --cov-report=html

# Run specific test files
pytest tests/test_your_changes.py

# Run integration tests
pytest tests/integration/
```

### 4. Code Quality Checks

```bash
# Format code with Black
black .

# Sort imports with isort
isort .

# Check linting with flake8
flake8

# Check type hints with mypy
mypy egile_mcp_client/

# Run all pre-commit hooks
pre-commit run --all-files
```

### 5. Commit Your Changes

```bash
# Stage your changes
git add .

# Commit with a descriptive message
git commit -m "feat: add support for custom connection types"

# Or for bug fixes
git commit -m "fix: handle connection timeout in WebSocket client"
```

#### Commit Message Format

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `style:` for formatting changes
- `refactor:` for code refactoring
- `test:` for adding tests
- `chore:` for maintenance tasks

### 6. Push and Create Pull Request

```bash
# Push your changes to your fork
git push origin feature/your-feature-name

# Create a pull request on GitHub
# Include a clear description of your changes
```

## Code Style Guidelines

### Python Code Style

We follow [PEP 8](https://pep8.org/) with some modifications:

- **Line Length**: 88 characters (Black default)
- **Quotes**: Use double quotes for strings
- **Imports**: Organize imports with isort
- **Type Hints**: All public functions must have type hints

### Example Code Style

```python
"""Module docstring describing the purpose."""

from typing import Dict, List, Optional, Union
import asyncio

from egile_mcp_client.protocol import Message, Tool


class ExampleClass:
    """Class docstring with clear description.
    
    Attributes:
        attribute_name: Description of the attribute.
    """
    
    def __init__(self, name: str, config: Dict[str, str]) -> None:
        """Initialize the example class.
        
        Args:
            name: The name of the instance.
            config: Configuration dictionary.
        """
        self.name = name
        self._config = config
    
    async def async_method(
        self,
        parameter: str,
        optional_param: Optional[int] = None
    ) -> List[str]:
        """Async method with proper type hints.
        
        Args:
            parameter: Required string parameter.
            optional_param: Optional integer parameter.
            
        Returns:
            List of processed strings.
            
        Raises:
            ValueError: If parameter is invalid.
        """
        if not parameter:
            raise ValueError("Parameter cannot be empty")
        
        # Implementation here
        return [parameter]
```

### Documentation Style

- Use **Google-style docstrings**
- Include type information in docstrings
- Provide clear examples in docstrings
- Document all public APIs

## Testing Guidelines

### Test Structure

```
tests/
├── unit/                   # Unit tests
│   ├── test_agents/
│   ├── test_mcp/
│   ├── test_config/
│   └── test_utils/
├── integration/           # Integration tests
│   ├── test_e2e/
│   ├── test_web/
│   └── test_cli/
└── fixtures/              # Test fixtures and data
    ├── mock_servers/
    ├── test_configs/
    └── sample_data/
```

### Writing Tests

#### Unit Tests

```python
import pytest
from unittest.mock import AsyncMock, MagicMock

from egile_mcp_client.mcp.client import MCPClient


class TestMCPClient:
    """Test cases for MCPClient."""
    
    @pytest.fixture
    async def mock_client(self):
        """Create a mock MCP client for testing."""
        config = MagicMock()
        client = MCPClient(config)
        client._connection = AsyncMock()
        return client
    
    async def test_connect_success(self, mock_client):
        """Test successful connection to MCP server."""
        # Arrange
        mock_client._connection.connect.return_value = None
        
        # Act
        await mock_client.connect("test_server")
        
        # Assert
        mock_client._connection.connect.assert_called_once()
        assert mock_client.is_connected()
    
    async def test_connect_failure(self, mock_client):
        """Test connection failure handling."""
        # Arrange
        mock_client._connection.connect.side_effect = ConnectionError()
        
        # Act & Assert
        with pytest.raises(ConnectionError):
            await mock_client.connect("test_server")
```

#### Integration Tests

```python
import pytest
from egile_mcp_client import MCPClient, Config


class TestMCPClientIntegration:
    """Integration tests for MCP client."""
    
    @pytest.fixture
    def test_config(self):
        """Load test configuration."""
        return Config.load("tests/fixtures/test_config.yaml")
    
    async def test_real_server_interaction(self, test_config):
        """Test interaction with a real MCP server."""
        client = MCPClient(test_config)
        
        try:
            await client.connect("test_server")
            tools = await client.list_tools()
            assert len(tools) > 0
        finally:
            await client.disconnect()
```

### Test Fixtures

Create reusable test fixtures:

```python
# conftest.py
import pytest
from unittest.mock import AsyncMock

@pytest.fixture
async def mock_mcp_connection():
    """Mock MCP connection for testing."""
    connection = AsyncMock()
    connection.is_connected.return_value = True
    connection.send.return_value = {"result": "success"}
    return connection

@pytest.fixture
def sample_config():
    """Sample configuration for testing."""
    return {
        "mcp_servers": [
            {
                "name": "test_server",
                "url": "http://localhost:8000",
                "type": "http"
            }
        ],
        "default_ai_provider": "openai"
    }
```

## Adding New Features

### 1. New Agent Providers

To add support for a new AI provider:

1. **Create the agent class**:
   ```python
   # egile_mcp_client/agents/new_provider_agent.py
   from egile_mcp_client.agents.base import BaseAgent
   
   class NewProviderAgent(BaseAgent):
       async def chat(self, message: str, tools: List[Tool]) -> Message:
           # Implementation here
           pass
   ```

2. **Register the agent**:
   ```python
   # egile_mcp_client/agents/__init__.py
   from .new_provider_agent import NewProviderAgent
   
   AGENT_REGISTRY = {
       "openai": OpenAIAgent,
       "anthropic": AnthropicAgent,
       "xai": XAIAgent,
       "new_provider": NewProviderAgent,  # Add here
   }
   ```

3. **Add configuration schema**:
   ```python
   # egile_mcp_client/config.py
   class NewProviderConfig(BaseModel):
       api_key: str
       model: str
       # Other provider-specific settings
   ```

4. **Write comprehensive tests**:
   ```python
   # tests/unit/test_agents/test_new_provider_agent.py
   class TestNewProviderAgent:
       # Test all methods and edge cases
       pass
   ```

### 2. New Connection Types

To add support for a new connection type:

1. **Create the connection class**:
   ```python
   # egile_mcp_client/mcp/connection.py
   class NewConnection(BaseConnection):
       async def connect(self) -> None:
           # Implementation
           pass
       
       async def send(self, message: dict) -> dict:
           # Implementation
           pass
   ```

2. **Register the connection**:
   ```python
   # egile_mcp_client/mcp/connection.py
   CONNECTION_REGISTRY = {
       "http": HTTPConnection,
       "websocket": WebSocketConnection,
       "stdio": StdioConnection,
       "new_type": NewConnection,  # Add here
   }
   ```

### 3. New CLI Commands

To add new CLI commands:

1. **Add the command**:
   ```python
   # egile_mcp_client/cli.py
   @app.command()
   def new_command(
       parameter: str = typer.Argument(..., help="Parameter description")
   ):
       """New command description."""
       # Implementation
       pass
   ```

2. **Add tests**:
   ```python
   # tests/unit/test_cli.py
   def test_new_command():
       # Test the new command
       pass
   ```

## Documentation

### Updating Documentation

When adding new features or making changes:

1. **Update docstrings** in the code
2. **Update API documentation** if needed
3. **Update user guides** for new features
4. **Add examples** for new functionality

### Building Documentation Locally

```bash
# Install documentation dependencies
pip install sphinx sphinx-rtd-theme myst-parser

# Build documentation
cd docs
make html

# View documentation
open _build/html/index.html
```

## Pull Request Guidelines

### Before Submitting

- [ ] All tests pass locally
- [ ] Code is properly formatted (Black, isort)
- [ ] Linting passes (flake8)
- [ ] Type checking passes (mypy)
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated (for significant changes)

### Pull Request Template

When creating a pull request, include:

```markdown
## Description
Brief description of the changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring
- [ ] Performance improvement

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests pass locally
```

### Review Process

1. **Automated Checks**: CI/CD pipeline runs automatically
2. **Code Review**: Maintainers review the code
3. **Feedback**: Address any requested changes
4. **Approval**: Once approved, the PR will be merged

## Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Follow the project's code of conduct

### Getting Help

- **Documentation**: Check the docs first
- **GitHub Issues**: Search existing issues
- **Discussions**: Use GitHub Discussions for questions
- **Community**: Join our community channels

### Reporting Issues

When reporting bugs or requesting features:

1. **Search existing issues** first
2. **Use the issue template**
3. **Provide detailed information**:
   - Python version
   - Operating system
   - Steps to reproduce
   - Expected vs actual behavior
   - Error messages/logs

### Security Issues

For security-related issues:
- **Do not** create public issues
- Email security concerns to: security@example.com
- Include detailed information about the vulnerability

## Release Process

### Versioning

We follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Changelog

All significant changes are documented in `CHANGELOG.md`:
- Follow [Keep a Changelog](https://keepachangelog.com/) format
- Include changes in the "Unreleased" section
- Categorize changes: Added, Changed, Deprecated, Removed, Fixed, Security

Thank you for contributing to Egile MCP Client! Your contributions help make this project better for everyone.
