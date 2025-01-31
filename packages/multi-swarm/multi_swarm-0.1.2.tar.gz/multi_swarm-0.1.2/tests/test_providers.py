import pytest
from multi_swarm.core import BaseAgent
from typing import Dict, Any

class TestProviders:
    """Test suite for Multi-Swarm LLM providers integration."""

    @pytest.mark.asyncio
    async def test_claude_provider(self, mock_env_vars, mock_provider_config: Dict[str, Any]):
        """Test that Claude provider works correctly."""
        agent = BaseAgent(
            name="ClaudeAgent",
            description="Test Claude Agent",
            instructions="Test instructions",
            tools_folder="./tools",
            model="claude-3-sonnet",
            temperature=0.7
        )
        
        # Test response generation
        response = await agent.generate_response("Test message")
        assert isinstance(response, str)
        assert len(response) > 0
    
    @pytest.mark.asyncio
    async def test_gemini_provider(self, mock_env_vars, mock_provider_config: Dict[str, Any]):
        """Test that Gemini provider works correctly."""
        agent = BaseAgent(
            name="GeminiAgent",
            description="Test Gemini Agent",
            instructions="Test instructions",
            tools_folder="./tools",
            model="gemini-2.0-pro",
            temperature=0.7
        )
        
        # Test response generation
        response = await agent.generate_response("Test message")
        assert isinstance(response, str)
        assert len(response) > 0
    
    def test_invalid_provider(self):
        """Test that initialization fails with invalid provider."""
        with pytest.raises(ValueError):
            BaseAgent(
                name="InvalidAgent",
                description="Test Invalid Agent",
                instructions="Test instructions",
                tools_folder="./tools",
                model="invalid-model",
                temperature=0.7
            )
    
    @pytest.mark.asyncio
    async def test_provider_error_handling(self, mock_env_vars):
        """Test that provider errors are handled correctly."""
        # Test with invalid API key
        with pytest.raises(Exception):
            agent = BaseAgent(
                name="ErrorAgent",
                description="Test Error Agent",
                instructions="Test instructions",
                tools_folder="./tools",
                model="claude-3-sonnet",
                temperature=0.7
            )
            await agent.generate_response("Test message")
    
    def test_provider_config_validation(self, mock_provider_config: Dict[str, Any]):
        """Test that provider configuration is validated correctly."""
        # Test valid Claude config
        agent = BaseAgent(
            name="ValidClaudeAgent",
            description="Test Valid Claude Agent",
            instructions="Test instructions",
            tools_folder="./tools",
            model="claude-3-sonnet",
            temperature=0.7
        )
        assert agent.model == "claude-3-sonnet"
        
        # Test valid Gemini config
        agent = BaseAgent(
            name="ValidGeminiAgent",
            description="Test Valid Gemini Agent",
            instructions="Test instructions",
            tools_folder="./tools",
            model="gemini-2.0-pro",
            temperature=0.7
        )
        assert agent.model == "gemini-2.0-pro" 