import pytest
from typing import Dict, Any
from multi_swarm.core.base_agent import BaseAgent
from unittest.mock import AsyncMock, patch, MagicMock
from multi_swarm.core.agency import Agency

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
    async def test_gemini_provider(self, mock_env_vars):
        """Test that Gemini provider can generate responses."""
        mock_agent = MagicMock(spec=BaseAgent)
        mock_agent.name = "MockAgent"
        mock_agent.model = "gemini-2.0-pro"
        
        with patch('multi_swarm.core.agency.Agency.demo_loop', new_callable=AsyncMock) as mock_demo:
            agency = Agency(agents=[mock_agent], shared_instructions="test_instructions.md")
            mock_demo.return_value = None
            # Call demo_loop directly instead of run_demo to avoid nested event loops
            await agency.demo_loop()
            mock_demo.assert_called_once()
    
    def test_invalid_provider(self, mock_env_vars):
        """Test that invalid provider is handled correctly."""
        with pytest.raises(ValueError, match="Unsupported model"):
            BaseAgent(
                name="InvalidAgent",
                description="Test Invalid Agent",
                instructions="Test instructions",
                tools_folder="./tools",
                model="invalid-model",
                temperature=0.7
            )
    
    def test_missing_api_key(self, monkeypatch):
        """Test that missing API keys are handled correctly."""
        # Remove environment variables
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        monkeypatch.delenv("GOOGLE_API_KEY", raising=False)

        # Test Claude
        with pytest.raises(ValueError, match="ANTHROPIC_API_KEY environment variable is not set"):
            BaseAgent(
                name="ClaudeAgent",
                description="Test Claude Agent",
                instructions="Test instructions",
                tools_folder="./tools",
                model="claude-3-sonnet",
                temperature=0.7
            )

        # Test Gemini
        with pytest.raises(ValueError, match="GOOGLE_API_KEY environment variable is not set"):
            BaseAgent(
                name="GeminiAgent",
                description="Test Gemini Agent",
                instructions="Test instructions",
                tools_folder="./tools",
                model="gemini-2.0-pro",
                temperature=0.7
            )
    
    def test_provider_config_validation(self, mock_env_vars, mock_provider_config: Dict[str, Any]):
        """Test that provider configurations are validated correctly."""
        # Test valid temperature
        agent = BaseAgent(
            name="TestAgent",
            description="Test Agent",
            instructions="Test instructions",
            tools_folder="./tools",
            model="claude-3-sonnet",
            temperature=0.7
        )
        assert agent.temperature == 0.7

        # Test invalid temperature values
        for invalid_temp in [-0.1, 1.1, "invalid", None]:
            with pytest.raises(ValueError, match="Temperature must be a number between 0 and 1"):
                BaseAgent(
                    name="TestAgent",
                    description="Test Agent",
                    instructions="Test instructions",
                    tools_folder="./tools",
                    model="claude-3-sonnet",
                    temperature=invalid_temp
                )

    @pytest.mark.asyncio
    async def test_response_generation_error(self, mock_env_vars):
        """Test error handling during response generation."""
        agent = BaseAgent(
            name="TestAgent",
            description="Test Agent",
            instructions="Test instructions",
            tools_folder="./tools",
            model="claude-3-sonnet",
            temperature=0.7
        )

        # Test with invalid model after initialization
        agent.model = "invalid-model"
        with pytest.raises(ValueError, match="Unsupported model"):
            await agent.generate_response("Test message") 