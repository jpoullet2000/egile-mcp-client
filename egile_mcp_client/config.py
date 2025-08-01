"""Configuration management for the MCP client."""

import os
import yaml
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


@dataclass
class AIProviderConfig:
    """Configuration for AI providers."""

    api_key: str
    model: str
    temperature: float = 0.7
    max_tokens: int = 2000


@dataclass
class MCPServerConfig:
    """Configuration for MCP servers."""

    name: str
    url: Optional[str] = None
    command: Optional[List[str]] = None
    type: str = "http"  # http, websocket, stdio
    description: Optional[str] = None


@dataclass
class WebInterfaceConfig:
    """Configuration for web interface."""

    host: str = "localhost"
    port: int = 8080
    title: str = "Egile MCP Client"
    max_history_messages: int = 1000


@dataclass
class LoggingConfig:
    """Configuration for logging."""

    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file: Optional[str] = None


@dataclass
class HistoryConfig:
    """Configuration for conversation history."""

    storage_type: str = "file"
    file_path: str = "data/conversation_history.json"
    max_conversations: int = 100


@dataclass
class Config:
    """Main configuration class."""

    ai_providers: Dict[str, AIProviderConfig]
    mcp_servers: List[MCPServerConfig]
    default_ai_provider: str = "openai"
    default_mcp_server: Optional[str] = None
    web_interface: WebInterfaceConfig = None
    logging: LoggingConfig = None
    history: HistoryConfig = None

    def __post_init__(self):
        if self.web_interface is None:
            self.web_interface = WebInterfaceConfig()
        if self.logging is None:
            self.logging = LoggingConfig()
        if self.history is None:
            self.history = HistoryConfig()


def load_config(config_path: Optional[Path] = None) -> Config:
    """Load configuration from file or environment variables."""
    # Load environment variables from .env file if available
    if load_dotenv is not None:
        # Look for .env file in current directory first
        env_path = Path(".env")
        if env_path.exists():
            print(f"Loading .env from: {env_path.absolute()}")
            load_dotenv(env_path)
        else:
            # Try to find .env file relative to this config file
            config_dir = Path(__file__).parent.parent
            env_path = config_dir / ".env"
            if env_path.exists():
                print(f"Loading .env from: {env_path.absolute()}")
                load_dotenv(env_path)
            else:
                # Try to load any .env file found
                print("No .env file found, trying default load_dotenv()")
                load_dotenv()

    if config_path is None:
        # Look for config in current directory, then in ~/.egile-mcp-client/
        candidates = [
            Path("config.yaml"),
            Path("config.yml"),
            Path.home() / ".egile-mcp-client" / "config.yaml",
            Path.home() / ".egile-mcp-client" / "config.yml",
        ]

        for candidate in candidates:
            if candidate.exists():
                config_path = candidate
                break

    config_data = {}

    if config_path and config_path.exists():
        with open(config_path, "r") as f:
            config_data = yaml.safe_load(f) or {}

    # Override with environment variables
    env_overrides = {}

    # AI provider keys from environment
    for provider in ["openai", "anthropic", "xai"]:
        env_key = f"{provider.upper()}_API_KEY"
        model_env_key = f"{provider.upper()}_MODEL"

        if env_key in os.environ or model_env_key in os.environ:
            if "ai_providers" not in env_overrides:
                env_overrides["ai_providers"] = {}
            if provider not in env_overrides["ai_providers"]:
                env_overrides["ai_providers"][provider] = {}

            if env_key in os.environ:
                env_overrides["ai_providers"][provider]["api_key"] = os.environ[env_key]
            if model_env_key in os.environ:
                env_overrides["ai_providers"][provider]["model"] = os.environ[
                    model_env_key
                ]

    # Merge configuration (deep merge for ai_providers)
    merged_config = config_data.copy()

    if "ai_providers" in env_overrides:
        if "ai_providers" not in merged_config:
            merged_config["ai_providers"] = {}

        for provider_name, env_provider_config in env_overrides["ai_providers"].items():
            if provider_name in merged_config["ai_providers"]:
                # Merge with existing config
                merged_config["ai_providers"][provider_name].update(env_provider_config)
            else:
                # New provider from environment only
                merged_config["ai_providers"][provider_name] = env_provider_config

    # Apply other environment overrides
    for key, value in env_overrides.items():
        if key != "ai_providers":
            merged_config[key] = value

    # Parse configuration
    ai_providers = {}
    for name, provider_data in merged_config.get("ai_providers", {}).items():
        ai_providers[name] = AIProviderConfig(**provider_data)

    mcp_servers = []
    for server_data in merged_config.get("mcp_servers", []):
        mcp_servers.append(MCPServerConfig(**server_data))

    web_interface = WebInterfaceConfig(**merged_config.get("web_interface", {}))
    logging_config = LoggingConfig(**merged_config.get("logging", {}))
    history_config = HistoryConfig(**merged_config.get("history", {}))

    return Config(
        ai_providers=ai_providers,
        mcp_servers=mcp_servers,
        default_ai_provider=merged_config.get("default_ai_provider", "openai"),
        default_mcp_server=merged_config.get("default_mcp_server"),
        web_interface=web_interface,
        logging=logging_config,
        history=history_config,
    )


def get_mcp_server_config(
    config: Config, server_name: str
) -> Optional[MCPServerConfig]:
    """Get configuration for a specific MCP server."""
    for server in config.mcp_servers:
        if server.name == server_name:
            return server
    return None


def get_ai_provider_config(
    config: Config, provider_name: str
) -> Optional[AIProviderConfig]:
    """Get configuration for a specific AI provider."""
    return config.ai_providers.get(provider_name)
