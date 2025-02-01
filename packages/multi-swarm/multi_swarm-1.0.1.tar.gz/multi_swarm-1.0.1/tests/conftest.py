import pytest
import os
from typing import Dict, Any
from tests.utils.mocks import patch_providers

@pytest.fixture
def mock_env_vars() -> Dict[str, str]:
    """Provide mock environment variables for testing."""
    return {
        "ANTHROPIC_API_KEY": "mock-claude-key",
        "GOOGLE_API_KEY": "mock-gemini-key"
    }

@pytest.fixture
def mock_provider_config() -> Dict[str, Dict[str, Any]]:
    """Provide mock provider configurations for testing."""
    return {
        "claude": {
            "model": "claude-3-sonnet",
            "api_version": "2024-03",
            "max_tokens": 4096
        },
        "gemini": {
            "model": "gemini-2.0-pro",
            "api_version": "2024-01",
            "max_tokens": 4096
        }
    }

@pytest.fixture
def mock_agent_config() -> Dict[str, Any]:
    """Mock agent configuration for testing."""
    return {
        "name": "TestAgent",
        "description": "Test Agent Description",
        "instructions": "Test instructions",
        "tools_folder": "./tools",
        "temperature": 0.7
    }

@pytest.fixture
def mock_agency_config() -> Dict[str, Any]:
    """Mock agency configuration for testing."""
    return {
        "shared_instructions": "Test shared instructions",
        "temperature": 0.7,
        "max_prompt_tokens": 4096
    }

@pytest.fixture
def mock_tool_config() -> Dict[str, Any]:
    """Mock tool configuration for testing."""
    return {
        "name": "TestTool",
        "description": "Test Tool Description",
        "parameters": {
            "param1": "value1",
            "param2": "value2"
        }
    }

@pytest.fixture(autouse=True)
def mock_providers(monkeypatch, mock_env_vars):
    """Automatically mock LLM providers for all tests."""
    patch_providers(monkeypatch, mock_env_vars)
    return None 