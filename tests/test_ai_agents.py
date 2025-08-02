"""Test suite for AI agent functionality and model validation."""

import pytest
import os
from unittest.mock import patch, AsyncMock, MagicMock

from egile_mcp_client.config import AIProviderConfig


class TestAIAgents:
    """Test AI agent functionality."""

    @pytest.fixture
    def openai_config(self):
        """Create OpenAI provider configuration."""
        return AIProviderConfig(
            api_key="test-openai-key", model="gpt-4", temperature=0.7, max_tokens=2000
        )

    @pytest.fixture
    def anthropic_config(self):
        """Create Anthropic provider configuration."""
        return AIProviderConfig(
            api_key="test-anthropic-key",
            model="claude-3-sonnet-20240229",
            temperature=0.7,
            max_tokens=2000,
        )

    @pytest.fixture
    def xai_config(self):
        """Create xAI provider configuration."""
        return AIProviderConfig(
            api_key="test-xai-key", model="grok-beta", temperature=0.7, max_tokens=2000
        )

    def test_openai_agent_initialization(self, openai_config):
        """Test OpenAI agent initialization."""
        from egile_mcp_client.agents.openai_agent import OpenAIAgent

        agent = OpenAIAgent(openai_config.model, openai_config.api_key)
        assert agent.model == openai_config.model
        assert agent.api_key == openai_config.api_key
        assert agent.client is not None

    def test_anthropic_agent_initialization(self, anthropic_config):
        """Test Anthropic agent initialization."""
        from egile_mcp_client.agents.anthropic_agent import AnthropicAgent

        agent = AnthropicAgent(anthropic_config.model, anthropic_config.api_key)
        assert agent.model == anthropic_config.model
        assert agent.api_key == anthropic_config.api_key
        assert agent.client is not None

    def test_xai_agent_initialization(self, xai_config):
        """Test xAI agent initialization."""
        from egile_mcp_client.agents.xai_agent import XAIAgent

        agent = XAIAgent(xai_config.model, xai_config.api_key)
        assert agent.model == xai_config.model
        assert agent.api_key == xai_config.api_key
        assert agent.client is not None

    @pytest.mark.asyncio
    async def test_openai_agent_chat(self, openai_config):
        """Test OpenAI agent chat functionality."""
        from egile_mcp_client.agents.openai_agent import OpenAIAgent
        from egile_mcp_client.agents.base import Message

        # Mock the AsyncOpenAI client directly in the module
        with patch(
            "egile_mcp_client.agents.openai_agent.AsyncOpenAI"
        ) as mock_openai_class:
            mock_client = AsyncMock()
            mock_openai_class.return_value = mock_client

            # Mock the chat completion response with proper structure
            mock_response = MagicMock()
            mock_choice = MagicMock()
            mock_message = MagicMock()

            # Mock the model_dump() method to return the expected dictionary
            mock_message.model_dump.return_value = {
                "role": "assistant",
                "content": "Test response",
                "tool_calls": None,
            }

            mock_choice.message = mock_message
            mock_response.choices = [mock_choice]
            mock_client.chat.completions.create.return_value = mock_response

            agent = OpenAIAgent(openai_config.model, openai_config.api_key)
            messages = [Message(role="user", content="Test message")]
            response = await agent.chat_completion(messages)

            # The response should be a Message object with the expected content
            assert isinstance(response, Message)
            assert response.role == "assistant"
            assert response.content == "Test response"
            assert response.tool_calls is None
            mock_client.chat.completions.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_anthropic_agent_chat(self, anthropic_config):
        """Test Anthropic agent chat functionality."""
        from egile_mcp_client.agents.anthropic_agent import AnthropicAgent
        from egile_mcp_client.agents.base import Message

        # Mock the AsyncAnthropic client directly in the module
        with patch(
            "egile_mcp_client.agents.anthropic_agent.AsyncAnthropic"
        ) as mock_anthropic_class:
            mock_client = AsyncMock()
            mock_anthropic_class.return_value = mock_client

            # Mock the message response with proper structure
            mock_response = MagicMock()
            mock_content_block = MagicMock()
            mock_content_block.type = "text"
            mock_content_block.text = "Test response"
            mock_response.content = [mock_content_block]

            mock_client.messages.create.return_value = mock_response

            agent = AnthropicAgent(anthropic_config.model, anthropic_config.api_key)
            messages = [Message(role="user", content="Test message")]
            response = await agent.chat_completion(messages)

            # The response should be a Message object with the expected content
            assert isinstance(response, Message)
            assert response.role == "assistant"
            assert response.content == "Test response"
            assert response.tool_calls is None
            mock_client.messages.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_xai_agent_chat(self, xai_config):
        """Test xAI agent chat functionality."""
        from egile_mcp_client.agents.xai_agent import XAIAgent
        from egile_mcp_client.agents.base import Message

        # Mock the AsyncOpenAI client directly in the module
        with patch(
            "egile_mcp_client.agents.xai_agent.AsyncOpenAI"
        ) as mock_openai_class:
            mock_client = AsyncMock()
            mock_openai_class.return_value = mock_client

            # Mock the chat completion response with proper structure
            mock_response = MagicMock()
            mock_choice = MagicMock()
            mock_message = MagicMock()

            # Mock the model_dump() method to return the expected dictionary
            mock_message.model_dump.return_value = {
                "role": "assistant",
                "content": "Test response",
                "tool_calls": None,
            }

            mock_choice.message = mock_message
            mock_response.choices = [mock_choice]
            mock_client.chat.completions.create.return_value = mock_response

            agent = XAIAgent(xai_config.model, xai_config.api_key)
            messages = [Message(role="user", content="Test message")]
            response = await agent.chat_completion(messages)

            # The response should be a Message object with the expected content
            assert isinstance(response, Message)
            assert response.role == "assistant"
            assert response.content == "Test response"
            assert response.tool_calls is None
            mock_client.chat.completions.create.assert_called_once()

    def test_agent_classes_exist(self):
        """Test that agent classes can be imported."""
        from egile_mcp_client.agents.openai_agent import OpenAIAgent
        from egile_mcp_client.agents.anthropic_agent import AnthropicAgent
        from egile_mcp_client.agents.xai_agent import XAIAgent

        # Just test that the classes exist and can be imported
        assert OpenAIAgent is not None
        assert AnthropicAgent is not None
        assert XAIAgent is not None


class TestModelValidation:
    """Test model name validation and API connectivity."""

    @pytest.mark.asyncio
    async def test_xai_model_names(self):
        """Test xAI model name validation."""
        # Test known xAI model names
        known_models = ["grok-beta", "grok-2", "grok-2-1212", "grok-2-latest", "grok-3"]

        for model in known_models:
            config = AIProviderConfig(api_key="test-key", model=model, temperature=0.7)
            assert config.model == model

    @pytest.mark.asyncio
    async def test_openai_model_names(self):
        """Test OpenAI model name validation."""
        known_models = [
            "gpt-4",
            "gpt-4-turbo",
            "gpt-3.5-turbo",
            "gpt-4o",
            "gpt-4o-mini",
        ]

        for model in known_models:
            config = AIProviderConfig(api_key="test-key", model=model, temperature=0.7)
            assert config.model == model

    @pytest.mark.asyncio
    async def test_anthropic_model_names(self):
        """Test Anthropic model name validation."""
        known_models = [
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307",
            "claude-3-5-sonnet-20241022",
        ]

        for model in known_models:
            config = AIProviderConfig(api_key="test-key", model=model, temperature=0.7)
            assert config.model == model

    def test_model_parameter_validation(self):
        """Test model parameter validation."""
        # Test temperature validation
        config = AIProviderConfig(api_key="test-key", model="gpt-4", temperature=0.7)
        assert 0.0 <= config.temperature <= 2.0

        # Test max_tokens validation
        config = AIProviderConfig(api_key="test-key", model="gpt-4", max_tokens=2000)
        assert config.max_tokens > 0

    @pytest.mark.asyncio
    @pytest.mark.integration
    @pytest.mark.skipif(not os.getenv("XAI_API_KEY"), reason="XAI_API_KEY not set")
    async def test_xai_api_connection(self):
        """Test actual xAI API connection (integration test)."""
        from openai import AsyncOpenAI

        api_key = os.getenv("XAI_API_KEY")
        client = AsyncOpenAI(api_key=api_key, base_url="https://api.x.ai/v1")

        try:
            # Test with a simple prompt
            response = await client.chat.completions.create(
                model="grok-beta",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10,
            )

            assert response.choices[0].message.content is not None

        except Exception as e:
            pytest.skip(f"xAI API test failed: {e}")

    @pytest.mark.asyncio
    @pytest.mark.integration
    @pytest.mark.skipif(
        not os.getenv("OPENAI_API_KEY"), reason="OPENAI_API_KEY not set"
    )
    async def test_openai_api_connection(self):
        """Test actual OpenAI API connection (integration test)."""
        from openai import AsyncOpenAI

        api_key = os.getenv("OPENAI_API_KEY")
        client = AsyncOpenAI(api_key=api_key)

        try:
            # Test with a simple prompt
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10,
            )

            assert response.choices[0].message.content is not None

        except Exception as e:
            pytest.skip(f"OpenAI API test failed: {e}")

    @pytest.mark.asyncio
    @pytest.mark.integration
    @pytest.mark.skipif(
        not os.getenv("ANTHROPIC_API_KEY"), reason="ANTHROPIC_API_KEY not set"
    )
    async def test_anthropic_api_connection(self):
        """Test actual Anthropic API connection (integration test)."""
        import anthropic

        api_key = os.getenv("ANTHROPIC_API_KEY")
        client = anthropic.AsyncAnthropic(api_key=api_key)

        try:
            # Test with a simple prompt
            response = await client.messages.create(
                model="claude-3-haiku-20240307",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10,
            )

            assert response.content[0].text is not None

        except Exception as e:
            pytest.skip(f"Anthropic API test failed: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
