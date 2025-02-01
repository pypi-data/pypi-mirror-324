import os
from dotenv import load_dotenv
from multi_swarm.core import Agency

# Load environment variables
load_dotenv()

def create_agency(agents, shared_instructions=None):
    """
    Create a new agency with the specified agents and communication flows.
    
    Args:
        agents: List of agents and their communication flows. The first item should be
               the entry point agent, followed by lists defining communication flows
               between agents (e.g. [agent1, [agent1, agent2], [agent2, agent3]])
        shared_instructions: Path to a markdown file containing shared instructions
                           for all agents in the agency
    
    Returns:
        Agency: A configured agency instance ready to run
    """
    return Agency(
        agents=agents,
        shared_instructions=shared_instructions
    )

if __name__ == "__main__":
    print("This module provides agency creation utilities.")
    print("See the examples directory for usage examples.") 