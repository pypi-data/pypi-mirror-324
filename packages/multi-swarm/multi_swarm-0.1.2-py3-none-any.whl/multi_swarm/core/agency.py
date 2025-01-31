import os
import asyncio
from typing import List, Tuple, Optional
from .base_agent import BaseAgent

class Agency:
    def __init__(
        self,
        agents: List[BaseAgent | List[BaseAgent]],
        shared_instructions: Optional[str] = None,
    ):
        # Extract the entry point agent (first agent)
        if isinstance(agents[0], list):
            raise ValueError("First agent must be the entry point agent, not a communication flow")
        self.entry_point = agents[0]
        
        # Process communication flows
        self.communication_flows = []
        for agent_or_flow in agents[1:]:
            if isinstance(agent_or_flow, list):
                if len(agent_or_flow) != 2:
                    raise ValueError("Communication flows must be pairs of agents")
                self.communication_flows.append(tuple(agent_or_flow))
            else:
                raise ValueError("All items after the first must be communication flows (lists of 2 agents)")
        
        # Load shared instructions
        self.shared_instructions = ""
        if shared_instructions and os.path.exists(shared_instructions):
            with open(shared_instructions, 'r', encoding='utf-8') as f:
                self.shared_instructions = f.read()
    
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
        """Process a user message through the agency."""
        # First, get response from entry point agent
        response = await self.entry_point.generate_response(message)
        
        # Process through communication flows
        for source, target in self.communication_flows:
            if source == self.entry_point:
                # Forward the task to target agent
                sub_response = await target.generate_response(response)
                # Combine responses
                response = f"{response}\n\nAnalysis from {target.name}:\n{sub_response}"
        
        return response 