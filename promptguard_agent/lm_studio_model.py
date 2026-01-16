"""
Custom model adapter for LM Studio using LiteLLM.

This allows ADK to use LM Studio (running on localhost:1234) as the LLM backend.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

try:
    from litellm import completion
    LITELLM_AVAILABLE = True
except ImportError:
    LITELLM_AVAILABLE = False


class LMStudioModel:
    """
    Model adapter for LM Studio using LiteLLM.
    
    LM Studio typically runs on localhost:1234 and provides an OpenAI-compatible API.
    """
    
    def __init__(
        self,
        base_url: str = "http://localhost:1234/v1",
        model_name: str = "local-model",
        api_key: str = "lm-studio",  # LM Studio doesn't require a real API key
    ):
        """
        Initialize LM Studio model adapter.
        
        Args:
            base_url: Base URL for LM Studio API (default: http://localhost:1234/v1)
            model_name: Model name to use (can be any name, LM Studio will use the loaded model)
            api_key: API key (LM Studio doesn't require a real key, but LiteLLM needs one)
        """
        if not LITELLM_AVAILABLE:
            raise ImportError(
                "LiteLLM is not installed. Install it with: pip install litellm"
            )
        
        self.base_url = base_url
        self.model_name = model_name
        self.api_key = api_key
    
    def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> str:
        """
        Generate a response using LM Studio via LiteLLM.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters
        
        Returns:
            Generated text response
        """
        # Configure LiteLLM to use LM Studio
        # LM Studio uses OpenAI-compatible API, so we use 'openai' provider
        # with custom base_url
        model = f"openai/{self.model_name}"
        
        response = completion(
            model=model,
            messages=messages,
            api_base=self.base_url,
            api_key=self.api_key,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs,
        )
        
        # Extract content from response
        if hasattr(response, 'choices') and len(response.choices) > 0:
            return response.choices[0].message.content
        elif isinstance(response, dict):
            return response.get("choices", [{}])[0].get("message", {}).get("content", "")
        else:
            return str(response)


def create_lm_studio_model(
    base_url: str = "http://localhost:1234/v1",
    model_name: str = "local-model",
) -> LMStudioModel:
    """
    Factory function to create an LM Studio model adapter.
    
    Args:
        base_url: Base URL for LM Studio (default: http://localhost:1234/v1)
        model_name: Model name (default: local-model)
    
    Returns:
        LMStudioModel instance
    """
    return LMStudioModel(base_url=base_url, model_name=model_name)

