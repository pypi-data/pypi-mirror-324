import pytest
from typing import Dict, Any
from multi_swarm.ceo.ceo_agent import CEO
from multi_swarm.trends_analyst.trends_analyst import TrendsAnalyst

class TestAgents:
    def test_ceo_initialization(self, mock_env_vars, mock_agent_config: Dict[str, Any]):
        """Test that CEO agent is initialized correctly."""
        ceo = CEO()
        assert ceo.name == "CEO"
        assert isinstance(ceo.description, str)
        assert isinstance(ceo.instructions, str)
        assert isinstance(ceo.tools_folder, str)
        assert ceo.model == "claude-3-sonnet"
        assert 0 <= ceo.temperature <= 1

    def test_trends_analyst_initialization(self, mock_env_vars, mock_agent_config: Dict[str, Any]):
        """Test that TrendsAnalyst agent is initialized correctly."""
        analyst = TrendsAnalyst()
        assert analyst.name == "TrendsAnalyst"
        assert isinstance(analyst.description, str)
        assert isinstance(analyst.instructions, str)
        assert isinstance(analyst.tools_folder, str)
        assert analyst.model == "gemini-2.0-pro"
        assert 0 <= analyst.temperature <= 1

    @pytest.mark.asyncio
    async def test_ceo_response_generation(self, mock_env_vars):
        """Test that CEO agent can generate responses."""
        ceo = CEO()
        response = await ceo.generate_response("Test message")
        assert isinstance(response, str)
        assert len(response) > 0

    @pytest.mark.asyncio
    async def test_trends_analyst_response_generation(self, mock_env_vars):
        """Test that TrendsAnalyst agent can generate responses."""
        analyst = TrendsAnalyst()
        response = await analyst.generate_response("Test message")
        assert isinstance(response, str)
        assert len(response) > 0 