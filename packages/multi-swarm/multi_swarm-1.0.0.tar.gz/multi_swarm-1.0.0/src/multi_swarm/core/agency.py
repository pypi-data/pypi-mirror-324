import os
import asyncio
from typing import List, Tuple, Optional
from multi_swarm.core.base_agent import BaseAgent

class Agency:
    def __init__(
        self,
        agents: List[BaseAgent | List[BaseAgent]],
        shared_instructions: Optional[str] = None,
    ):
        if not agents:
            raise ValueError("Agents list cannot be empty")

        # Extract the entry point agent (first agent)
        try:
            if isinstance(agents[0], list):
                raise ValueError("First agent must be the entry point, not a communication flow")
            self.entry_point = agents[0]
        except IndexError:
            raise ValueError("Agents list cannot be empty")

        # Extract communication flows
        self.communication_flows = []
        for item in agents[1:]:
            if isinstance(item, list):
                if len(item) != 2:
                    raise ValueError("Communication flows must be pairs of agents")
                self.communication_flows.append((item[0], item[1]))
            else:
                # If it's a single agent, it can communicate with the entry point
                self.communication_flows.append((self.entry_point, item))

        # Set shared instructions
        self.shared_instructions = shared_instructions or ""

    def run_demo(self):
        """Print welcome message and instructions for the demo."""
        print(f"\nWelcome to the {self.entry_point.name} Agency Demo!")
        print("\nType 'exit' to end the conversation.")
        print("\nEnter your message:")
        asyncio.run(self.demo_loop())
    
    async def demo_loop(self):
        """Run the interactive demo loop."""
        try:
            while True:
                user_input = input("> ")
                if user_input.lower() == 'exit':
                    print("\nThank you for using the agency. Goodbye!")
                    break
                
                response = await self.process_message(user_input)
                print(f"\n{self.entry_point.name}: {response}")
        
        except KeyboardInterrupt:
            print("\n\nDemo terminated by user. Goodbye!")
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
    
    async def process_message(self, message: str) -> str:
        """Process a message through the agency."""
        response = await self.entry_point.generate_response(message)
        return response 