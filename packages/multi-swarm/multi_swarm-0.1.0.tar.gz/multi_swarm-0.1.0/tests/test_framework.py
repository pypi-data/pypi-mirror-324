import pytest
from multi_swarm.core import Agency, BaseAgent
from typing import Dict, Any

class TestFramework:
    """Test suite for the Multi-Swarm framework core functionality."""

    def test_base_agent_initialization(self, mock_agent_config: Dict[str, Any]):
        """Test that a base agent can be initialized with correct configuration."""
        agent = BaseAgent(
            name=mock_agent_config["name"],
            description=mock_agent_config["description"],
            instructions=mock_agent_config["instructions"],
            tools_folder=mock_agent_config["tools_folder"],
            model="claude-3-sonnet",
            temperature=mock_agent_config["temperature"]
        )
        
        assert agent.name == mock_agent_config["name"]
        assert agent.description == mock_agent_config["description"]
        assert agent.temperature == mock_agent_config["temperature"]
    
    def test_agency_initialization(self, mock_agency_config: Dict[str, Any]):
        """Test that an agency can be initialized with correct configuration."""
        # Create test agents
        agent1 = BaseAgent(
            name="Agent1",
            description="Test Agent 1",
            instructions="Test instructions",
            tools_folder="./tools",
            model="claude-3-sonnet",
            temperature=0.7
        )
        
        agent2 = BaseAgent(
            name="Agent2",
            description="Test Agent 2",
            instructions="Test instructions",
            tools_folder="./tools",
            model="gemini-2.0-pro",
            temperature=0.7
        )
        
        # Create agency with communication flows
        agency = Agency(
            agents=[
                agent1,  # Entry point
                [agent1, agent2],  # Communication flow
            ],
            shared_instructions=mock_agency_config["shared_instructions"]
        )
        
        assert agency.entry_point == agent1
        assert len(agency.communication_flows) == 1
        assert agency.communication_flows[0] == (agent1, agent2)
    
    def test_invalid_agency_initialization(self):
        """Test that agency initialization fails with invalid configuration."""
        agent1 = BaseAgent(
            name="Agent1",
            description="Test Agent 1",
            instructions="Test instructions",
            tools_folder="./tools",
            model="claude-3-sonnet",
            temperature=0.7
        )
        
        # Test invalid entry point (first item is a list)
        with pytest.raises(ValueError):
            Agency(
                agents=[
                    [agent1, agent1],  # Invalid: first item is a flow
                ],
                shared_instructions="test"
            )
        
        # Test invalid communication flow (not a pair)
        with pytest.raises(ValueError):
            Agency(
                agents=[
                    agent1,
                    [agent1],  # Invalid: not a pair
                ],
                shared_instructions="test"
            )
    
    @pytest.mark.asyncio
    async def test_message_processing(self, mock_env_vars):
        """Test that messages are processed correctly through the agency."""
        # Create test agents
        agent1 = BaseAgent(
            name="Agent1",
            description="Test Agent 1",
            instructions="Test instructions",
            tools_folder="./tools",
            model="claude-3-sonnet",
            temperature=0.7
        )
        
        agent2 = BaseAgent(
            name="Agent2",
            description="Test Agent 2",
            instructions="Test instructions",
            tools_folder="./tools",
            model="gemini-2.0-pro",
            temperature=0.7
        )
        
        # Create agency
        agency = Agency(
            agents=[
                agent1,
                [agent1, agent2],
            ],
            shared_instructions="Test shared instructions"
        )
        
        # Process a test message
        response = await agency.process_message("Test message")
        assert isinstance(response, str)
        assert len(response) > 0 