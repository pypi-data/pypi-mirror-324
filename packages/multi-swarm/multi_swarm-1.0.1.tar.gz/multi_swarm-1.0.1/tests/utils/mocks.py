from unittest.mock import AsyncMock, MagicMock, patch
import asyncio
from typing import Any, Dict, List
import httpx
import grpc

class MockClaudeMessage:
    def __init__(self, content: str):
        self.content = [MagicMock(text=content)]

class MockClaudeResponse:
    def __init__(self, content: str):
        self.content = [MagicMock(text=content)]

class MockGeminiResponse:
    def __init__(self, text: str):
        self.text = text

class MockResponse:
    def __init__(self, content: str = "Mock response"):
        self.content = [MagicMock(text=content)]
        self.text = content

class MockClaudeClient:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API key is required")
        self.messages = MagicMock()
        self.messages.create = AsyncMock(return_value=MockResponse())

class MockGeminiClient:
    def __init__(self, api_key: str = None, model_name: str = None):
        if not api_key:
            raise ValueError("API key is required")
        self.model_name = model_name
        self.generate_content_async = AsyncMock(return_value=MockResponse())

class MockHttpxClient:
    def __init__(self, *args, **kwargs):
        self.send = AsyncMock(return_value=MockResponse(
            json_data={
                "content": [{"text": "Mock response"}]
            }
        ))

class MockGrpcChannel:
    def __init__(self, *args, **kwargs):
        self._unary_unary_interceptors = []
        self._unary_stream_interceptors = []
        self._logged_channel = self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def close(self):
        pass

    def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    def unary_unary(self, *args, **kwargs):
        return AsyncMock()

    def unary_stream(self, *args, **kwargs):
        return AsyncMock()

    def stream_stream(self, *args, **kwargs):
        return AsyncMock()

    def stream_unary(self, *args, **kwargs):
        return AsyncMock()

def patch_providers(monkeypatch: Any, mock_env_vars: Dict[str, str]):
    """Patch the LLM providers for testing."""
    # Mock environment variables
    for key, value in mock_env_vars.items():
        monkeypatch.setenv(key, value)

    # Mock Anthropic client
    def mock_anthropic_init(self, api_key: str):
        if not api_key:
            raise ValueError("API key is required")
        self.messages = MagicMock()
        self.messages.create = AsyncMock(return_value=MockResponse())

    monkeypatch.setattr("anthropic.Anthropic.__init__", mock_anthropic_init)

    # Mock Gemini client
    def mock_genai_configure(api_key: str):
        if not api_key:
            raise ValueError("API key is required")

    monkeypatch.setattr("google.generativeai.configure", mock_genai_configure)
    monkeypatch.setattr("google.generativeai.GenerativeModel", MockGeminiClient) 