#!/usr/bin/env python3
"""Test script for debugging config loading."""

import os
from pathlib import Path

print("=== Testing Environment Variable Loading ===")

# Test 1: Check if .env file exists
env_file = Path(".env")
print(f".env file exists: {env_file.exists()}")
if env_file.exists():
    print(f".env file content:")
    with open(env_file) as f:
        print(f.read())

# Test 2: Test dotenv loading
print("\n=== Testing dotenv loading ===")
try:
    from dotenv import load_dotenv

    print("Before load_dotenv:")
    print(f"OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY', 'Not set')}")

    load_dotenv()
    print("After load_dotenv:")
    print(f"OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY', 'Not set')}")
    print(f"ANTHROPIC_API_KEY: {os.getenv('ANTHROPIC_API_KEY', 'Not set')}")
    print(f"XAI_API_KEY: {os.getenv('XAI_API_KEY', 'Not set')}")
except Exception as e:
    print(f"Error loading dotenv: {e}")

# Test 3: Test config loading
print("\n=== Testing config loading ===")
try:
    from egile_mcp_client.config import load_config

    print("Starting config load...")
    config = load_config()
    print("Config loaded successfully!")
    print(f"AI providers: {list(config.ai_providers.keys())}")

    for name, provider in config.ai_providers.items():
        print(f"{name}: api_key={provider.api_key[:20]}..., model={provider.model}")

except Exception as e:
    print(f"Error loading config: {e}")
    import traceback

    traceback.print_exc()
