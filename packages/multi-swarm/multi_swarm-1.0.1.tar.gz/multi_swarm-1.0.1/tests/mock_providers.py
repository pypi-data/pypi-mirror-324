from unittest.mock import AsyncMock, MagicMock

class MockClaudeMessage:
    def __init__(self, content):
        self.content = content

class MockClaudeResponse:
    def __init__(self, content="Mock Claude Response"):
        self.content = [MockClaudeMessage(content)]

class MockGeminiResponse:
    def __init__(self, text="Mock Gemini Response"):
        self.text = text

class MockClaudeClient:
    def __init__(self):
        self.messages = AsyncMock()
        self.messages.create = AsyncMock(return_value=MockClaudeResponse())

class MockGeminiModel:
    def __init__(self):
        self.generate_content_async = AsyncMock(return_value=MockGeminiResponse())

def mock_claude_provider():
    """Create a mock Claude provider."""
    return MockClaudeClient()

def mock_gemini_provider():
    """Create a mock Gemini provider."""
    return MockGeminiModel()

def patch_providers(monkeypatch):
    """Patch both Claude and Gemini providers."""
    # Mock Anthropic
    monkeypatch.setattr('anthropic.Anthropic', mock_claude_provider)
    
    # Mock Gemini
    mock_genai = MagicMock()
    mock_genai.GenerativeModel = mock_gemini_provider
    monkeypatch.setattr('google.generativeai', mock_genai) 