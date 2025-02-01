from multi_swarm import BaseAgent

class BackendDeveloperAgent(BaseAgent):
    """Backend developer agent specialized in server-side development."""
    
    def __init__(self):
        super().__init__(
            name="Backend Developer",
            description="Technical expert in backend development and API design.",
            instructions="backend_developer_instructions.md",
            tools_folder="./tools",
            model="claude-3.5-sonnet",  # Using Claude for technical tasks
            temperature=0.5
        ) 