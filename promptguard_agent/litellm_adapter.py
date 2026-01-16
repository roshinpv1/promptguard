"""
LiteLLM adapter for ADK to use LM Studio.

This creates a custom model adapter that ADK can use with LiteLLM.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

try:
    from litellm import completion
    LITELLM_AVAILABLE = True
except ImportError:
    LITELLM_AVAILABLE = False


def setup_litellm_for_lm_studio(
    base_url: str = "http://localhost:1234/v1",
    api_key: str = "lm-studio",
) -> None:
    """
    Configure LiteLLM environment variables for LM Studio.
    
    Args:
        base_url: Base URL for LM Studio API
        api_key: API key (LM Studio doesn't require a real key)
    """
    os.environ["OPENAI_API_BASE"] = base_url
    os.environ["OPENAI_API_KEY"] = api_key


def create_lm_studio_model_string(model_name: str = "local-model") -> str:
    """
    Create a model string for LiteLLM that points to LM Studio.
    
    Args:
        model_name: Name of the model (can be any name)
    
    Returns:
        Model string in format: openai/{model_name}
    """
    return f"openai/{model_name}"


def test_lm_studio_connection(
    base_url: str = "http://localhost:1234/v1",
    model_name: str = "local-model",
) -> bool:
    """
    Test connection to LM Studio.
    
    Args:
        base_url: Base URL for LM Studio
        model_name: Model name to test
    
    Returns:
        True if connection successful, False otherwise
    """
    if not LITELLM_AVAILABLE:
        return False
    
    try:
        setup_litellm_for_lm_studio(base_url)
        model_string = create_lm_studio_model_string(model_name)
        
        response = completion(
            model=model_string,
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5,
        )
        return True
    except Exception as e:
        print(f"LM Studio connection test failed: {e}")
        return False

