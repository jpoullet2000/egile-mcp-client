#!/usr/bin/env python3
"""Test xAI API to find correct model name."""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


async def test_xai_models():
    """Test different xAI model names."""
    api_key = os.getenv("XAI_API_KEY")
    if not api_key:
        print("No XAI_API_KEY found")
        return

    try:
        from openai import AsyncOpenAI

        # xAI uses OpenAI-compatible API
        client = AsyncOpenAI(api_key=api_key, base_url="https://api.x.ai/v1")

        # Test different model names
        models_to_test = [
            "grok-beta",
            "grok-2",
            "grok-2-1212",
            "grok-2-latest",
            "grok-1",
            "grok",
        ]

        for model in models_to_test:
            try:
                print(f"Testing model: {model}")
                response = await client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": "Hello"}],
                    max_tokens=10,
                )
                print(
                    f"✅ {model} works! Response: {response.choices[0].message.content}"
                )
                break
            except Exception as e:
                print(f"❌ {model} failed: {e}")

        # Also try to list models if available
        try:
            print("\\nTrying to list available models...")
            models = await client.models.list()
            print("Available models:")
            for model in models.data:
                print(f"  - {model.id}")
        except Exception as e:
            print(f"Failed to list models: {e}")

    except ImportError:
        print("OpenAI library not available")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(test_xai_models())
