from multi_swarm.core import BaseAgent

class CEOAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="CEO",
            description="Strategic leader responsible for high-level decision making and coordinating with other agents.",
            instructions="./instructions.md",
            tools_folder="./tools",
            model="gemini-2.0-pro",
            temperature=0.7
        ) 