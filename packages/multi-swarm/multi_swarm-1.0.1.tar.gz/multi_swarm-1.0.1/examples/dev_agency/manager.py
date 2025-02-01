from multi_swarm import BaseAgent

class ManagerAgent(BaseAgent):
    """Project manager agent that coordinates development tasks."""
    
    def __init__(self):
        super().__init__(
            name="Project Manager",
            description="Strategic leader responsible for project planning and coordination.",
            instructions="manager_instructions.md",
            tools_folder="./tools",
            model="gemini-2.0-pro",  # Using Gemini for strategic planning
            temperature=0.7
        ) 