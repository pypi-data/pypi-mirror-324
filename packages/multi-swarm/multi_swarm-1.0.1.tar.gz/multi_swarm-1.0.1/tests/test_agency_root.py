import pytest
from typing import Dict, Any
from unittest.mock import patch, MagicMock
from multi_swarm.agency import create_agency, create_agent_template

class TestAgencyRoot:
    def test_create_agent_template(self, tmp_path):
        """Test that agent templates are created correctly."""
        # Test with valid parameters
        agent_path = tmp_path / "test_agent"
        result = create_agent_template(
            name="TestAgent",
            description="Test Agent Description",
            path=str(agent_path)
        )
        assert result is True
        assert agent_path.exists()
        assert (agent_path / "__init__.py").exists()
        assert (agent_path / "testagent.py").exists()
        assert (agent_path / "instructions.md").exists()
        assert (agent_path / "tools").exists()

        # Test with existing path
        result = create_agent_template(
            name="TestAgent",
            description="Test Agent Description",
            path=str(agent_path)
        )
        assert result is False

        # Test with invalid path
        result = create_agent_template(
            name="TestAgent",
            description="Test Agent Description",
            path="/invalid/path"
        )
        assert result is False

        # Test with file write error
        with patch("builtins.open", side_effect=IOError):
            result = create_agent_template(
                name="TestAgent",
                description="Test Agent Description",
                path=str(tmp_path / "error_agent")
            )
            assert result is False

    def test_create_agency(self, mock_env_vars, tmp_path):
        """Test that agencies are created correctly."""
        # Test with valid parameters
        agency_path = tmp_path / "test_agency"
        result = create_agency(
            name="TestAgency",
            description="Test Agency Description",
            path=str(agency_path)
        )
        assert result is True
        assert agency_path.exists()
        assert (agency_path / "__init__.py").exists()
        assert (agency_path / "agency.py").exists()
        assert (agency_path / "agency_manifesto.md").exists()
        assert (agency_path / "requirements.txt").exists()

        # Test with existing path
        result = create_agency(
            name="TestAgency",
            description="Test Agency Description",
            path=str(agency_path)
        )
        assert result is False

        # Test with invalid path
        result = create_agency(
            name="TestAgency",
            description="Test Agency Description",
            path="/invalid/path"
        )
        assert result is False

        # Test with file write error
        with patch("builtins.open", side_effect=IOError):
            result = create_agency(
                name="TestAgency",
                description="Test Agency Description",
                path=str(tmp_path / "error_agency")
            )
            assert result is False 