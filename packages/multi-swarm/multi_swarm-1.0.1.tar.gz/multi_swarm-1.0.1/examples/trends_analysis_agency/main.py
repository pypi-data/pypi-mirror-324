"""Example script demonstrating how to create and run a Google Trends Analysis Agency."""

from multi_swarm import Agency
from agents.ceo.agent import CEOAgent
from agents.trends_analyst.agent import TrendsAnalyst

def create_agency():
    """Create an example agency with a CEO and TrendsAnalyst."""
    # Initialize agents
    ceo = CEOAgent()
    analyst = TrendsAnalyst()

    # Create agency with communication flows
    agency = Agency(
        agents=[
            ceo,  # Entry point for user communication
            [ceo, analyst],  # CEO can communicate with analyst
        ],
        shared_instructions="agency_manifesto.md"
    )
    
    return agency

def main():
    """Run the example agency."""
    print("Starting Google Trends Analysis Agency Demo")
    print("Note: This is an example implementation without actual Google Trends functionality.")
    print("In a real implementation, you would need to add pytrends integration and analysis tools.")
    print("\nType 'exit' to end the conversation.\n")
    
    agency = create_agency()
    agency.run_demo()

if __name__ == "__main__":
    main() 