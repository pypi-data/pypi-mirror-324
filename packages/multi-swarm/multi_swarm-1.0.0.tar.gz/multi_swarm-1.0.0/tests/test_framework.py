import pytest
import os
from typing import Dict, Any
from unittest.mock import patch, MagicMock
from multi_swarm.core.agency import Agency
from multi_swarm.core.base_agent import BaseAgent

class TestFramework:
    def test_agent_initialization(self, mock_env_vars, mock_provider_config: Dict[str, Any]):
        """Test that agents are initialized correctly."""
        agent = BaseAgent(
            name="TestAgent",
            description="Test Agent",
            instructions="Test instructions",
            tools_folder="./tools",
            model="claude-3-sonnet",
            temperature=0.7
        )
        assert agent.name == "TestAgent"
        assert agent.description == "Test Agent"
        assert agent.temperature == 0.7

    def test_instruction_loading(self, mock_env_vars, tmp_path):
        """Test that instructions are loaded correctly."""
        # Test with non-existent file
        agent = BaseAgent(
            name="TestAgent",
            description="Test Agent",
            instructions="non_existent.md",
            tools_folder="./tools",
            model="claude-3-sonnet",
            temperature=0.7
        )
        assert agent.instructions == ""

        # Test with existing file
        instructions_file = tmp_path / "instructions.md"
        instructions_file.write_text("Test instructions content")
        agent = BaseAgent(
            name="TestAgent",
            description="Test Agent",
            instructions=str(instructions_file),
            tools_folder="./tools",
            model="claude-3-sonnet",
            temperature=0.7
        )
        assert agent.instructions == "Test instructions content"

    def test_tool_loading(self, mock_env_vars, tmp_path):
        """Test that tools are loaded correctly."""
        # Test with non-existent folder
        agent = BaseAgent(
            name="TestAgent",
            description="Test Agent",
            instructions="test.md",
            tools_folder="non_existent_folder",
            model="claude-3-sonnet",
            temperature=0.7
        )
        assert agent.tools == {}

        # Test with empty folder
        tools_folder = tmp_path / "tools"
        tools_folder.mkdir()
        agent = BaseAgent(
            name="TestAgent",
            description="Test Agent",
            instructions="test.md",
            tools_folder=str(tools_folder),
            model="claude-3-sonnet",
            temperature=0.7
        )
        assert agent.tools == {}

        # Test with Python files
        tool_file = tools_folder / "test_tool.py"
        tool_file.write_text("class TestTool: pass")
        agent = BaseAgent(
            name="TestAgent",
            description="Test Agent",
            instructions="test.md",
            tools_folder=str(tools_folder),
            model="claude-3-sonnet",
            temperature=0.7
        )
        assert isinstance(agent.tools, dict)

    def test_agency_initialization(self, mock_env_vars, mock_agency_config: Dict[str, Any]):
        """Test that agencies are initialized correctly."""
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

        agency = Agency(
            agents=[
                agent1,
                [agent1, agent2],
            ],
            shared_instructions="Test shared instructions"
        )
        assert agency.entry_point == agent1
        assert len(agency.communication_flows) == 1

    def test_invalid_agency_config(self, mock_env_vars):
        """Test that invalid agency configurations are handled correctly."""
        agent = BaseAgent(
            name="TestAgent",
            description="Test Agent",
            instructions="Test instructions",
            tools_folder="./tools",
            model="claude-3-sonnet",
            temperature=0.7
        )

        # Test empty agents list
        with pytest.raises(ValueError):
            Agency(agents=[], shared_instructions="Test")

        # Test invalid communication flow (not a pair)
        with pytest.raises(ValueError):
            Agency(agents=[agent, [agent]], shared_instructions="Test")

        # Test invalid communication flow (not BaseAgent)
        with pytest.raises(ValueError):
            Agency(agents=[agent, [agent, "not an agent"]], shared_instructions="Test")

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

    @pytest.mark.asyncio
    async def test_demo_loop(self, mock_env_vars, monkeypatch):
        """Test the agency demo loop."""
        agent = BaseAgent(
            name="TestAgent",
            description="Test Agent",
            instructions="test.md",
            tools_folder="./tools",
            model="claude-3-sonnet",
            temperature=0.7
        )

        agency = Agency(agents=[agent], shared_instructions="Test")

        # Test normal exit
        with patch('builtins.input', side_effect=['test message', 'exit']), \
             patch('builtins.print') as mock_print:
            await agency.demo_loop()
            mock_print.assert_any_call("\nThank you for using the agency. Goodbye!")

        # Test keyboard interrupt
        with patch('builtins.input', side_effect=KeyboardInterrupt), \
             patch('builtins.print') as mock_print:
            await agency.demo_loop()
            mock_print.assert_any_call("\n\nDemo terminated by user. Goodbye!")

        # Test error handling
        with patch('builtins.input', side_effect=Exception("Test error")), \
             patch('builtins.print') as mock_print:
            await agency.demo_loop()
            mock_print.assert_any_call("\nAn error occurred: Test error")

    def test_run_demo(self, mock_env_vars):
        """Test the run_demo method."""
        agent = BaseAgent(
            name="TestAgent",
            description="Test Agent",
            instructions="test.md",
            tools_folder="./tools",
            model="claude-3-sonnet",
            temperature=0.7
        )

        agency = Agency(agents=[agent], shared_instructions="Test")

        with patch('asyncio.run') as mock_run, \
             patch('builtins.print') as mock_print:
            agency.run_demo()
            mock_run.assert_called_once()
            mock_print.assert_any_call("\nWelcome to the TestAgent Agency Demo!")