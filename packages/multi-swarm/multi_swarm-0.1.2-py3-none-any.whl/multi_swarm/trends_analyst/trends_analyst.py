from multi_swarm.core import BaseAgent

class TrendsAnalyst(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Trends Analyst",
            description="Data analyst specialized in Google Trends analysis and insights generation.",
            instructions="./instructions.md",
            tools_folder="./tools",
            model="claude-3.5-sonnet",
            temperature=0.5
        ) 