from __future__ import annotations

import json
from typing import Any, Dict, Optional

import httpx

from promptshield.targets.base import Target


class APITarget(Target):
    """Target adapter for external LLM APIs (OpenAI, Anthropic, Azure, etc.)."""

    def __init__(
        self,
        api_url: str,
        model_id: str,
        api_key: Optional[str] = None,
        api_type: str = "openai",
        headers: Optional[Dict[str, str]] = None,
    ):
        self.api_url = api_url
        self.model_id = model_id
        self.api_key = api_key
        self.api_type = api_type
        self.headers = headers or {}
        self.client = httpx.AsyncClient(timeout=30.0)

    def _build_openai_request(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """Build OpenAI-compatible request."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        return {
            "model": self.model_id,
            "messages": messages,
            "temperature": 0.7,
        }

    def _build_anthropic_request(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """Build Anthropic-compatible request."""
        request: Dict[str, Any] = {
            "model": self.model_id,
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system_prompt:
            request["system"] = system_prompt
        return request

    def _build_azure_request(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """Build Azure OpenAI-compatible request."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        return {
            "messages": messages,
            "temperature": 0.7,
        }

    def _build_custom_request(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """Build custom API request (assumes OpenAI-like format)."""
        return self._build_openai_request(prompt, system_prompt)

    async def generate_async(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generate a response from the external API.
        
        Note: This is async, but the base Target interface is sync.
        For now, we'll use a sync wrapper with httpx.
        """
        # Build request based on API type
        if self.api_type == "openai":
            request_data = self._build_openai_request(prompt, system_prompt)
        elif self.api_type == "anthropic":
            request_data = self._build_anthropic_request(prompt, system_prompt)
        elif self.api_type == "azure":
            request_data = self._build_azure_request(prompt, system_prompt)
        else:
            request_data = self._build_custom_request(prompt, system_prompt)

        # Build headers
        headers = {"Content-Type": "application/json", **self.headers}
        if self.api_key:
            if self.api_type == "anthropic":
                headers["x-api-key"] = self.api_key
                headers["anthropic-version"] = "2023-06-01"
            elif self.api_type == "azure":
                headers["api-key"] = self.api_key
            else:
                headers["Authorization"] = f"Bearer {self.api_key}"

        # Make request
        try:
            response = await self.client.post(
                self.api_url,
                json=request_data,
                headers=headers,
            )
            response.raise_for_status()
            result = response.json()

            # Extract content based on API type
            if self.api_type == "openai":
                content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            elif self.api_type == "anthropic":
                content = result.get("content", [{}])[0].get("text", "")
            elif self.api_type == "azure":
                content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            else:
                # Try common patterns
                content = (
                    result.get("choices", [{}])[0].get("message", {}).get("content", "")
                    or result.get("content", "")
                    or result.get("text", "")
                    or str(result)
                )

            return content or "No response content"

        except httpx.HTTPStatusError as e:
            return f"API Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error calling API: {str(e)}"

    def generate(self, prompt: str) -> TargetResponse:
        """Synchronous generate method (required by Target interface)."""
        import asyncio

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        content = loop.run_until_complete(self.generate_async(prompt))
        return TargetResponse(content=content, blocked=False)

    def __del__(self):
        """Cleanup client on deletion."""
        if hasattr(self, "client"):
            try:
                import asyncio

                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # Schedule cleanup
                    asyncio.create_task(self.client.aclose())
                else:
                    loop.run_until_complete(self.client.aclose())
            except Exception:
                pass

