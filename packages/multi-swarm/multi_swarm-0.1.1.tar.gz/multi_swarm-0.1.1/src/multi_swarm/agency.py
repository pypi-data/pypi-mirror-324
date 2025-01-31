import os
from dotenv import load_dotenv
from multi_swarm.core import Agency
from multi_swarm.ceo.ceo_agent import CEOAgent
from multi_swarm.trends_analyst.trends_analyst import TrendsAnalyst

# Load environment variables
load_dotenv()

def create_agency():
    # Initialize agents
    ceo = CEOAgent()
    analyst = TrendsAnalyst()
    
    # Create agency with communication flows
    agency = Agency(
        agents=[
            ceo,  # CEO is the entry point
            [ceo, analyst],  # CEO can delegate to analyst
        ],
        shared_instructions="agency_manifesto.md"
    )
    
    return agency

if __name__ == "__main__":
    # Create and run the agency
    agency = create_agency()
    agency.run_demo() 