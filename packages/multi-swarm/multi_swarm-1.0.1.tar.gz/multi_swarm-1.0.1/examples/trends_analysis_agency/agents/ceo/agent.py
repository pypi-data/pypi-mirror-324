"""Example CEO agent implementation for the Google Trends Analysis Agency."""

from multi_swarm.core import BaseAgent

class CEOAgent(BaseAgent):
    """
    Example CEO agent that coordinates Google Trends analysis.
    
    This is a template implementation to demonstrate agent creation.
    In a real implementation, you would add actual tools and functionality.
    """
    
    def __init__(self):
        super().__init__(
            name="CEO",
            description="Strategic leader responsible for high-level decision making and coordinating with other agents.",
            instructions="./instructions.md",
            tools_folder="./tools",
            model="gemini-2.0-pro",
            temperature=0.7
        ) 