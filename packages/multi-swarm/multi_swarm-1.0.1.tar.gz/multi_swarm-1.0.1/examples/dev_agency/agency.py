from multi_swarm import Agency
from manager import ManagerAgent
from backend_developer import BackendDeveloperAgent
from frontend_developer import FrontendDeveloperAgent

def create_dev_agency():
    """Create a development agency with a manager and developers."""
    # Initialize agents
    manager = ManagerAgent()
    backend_dev = BackendDeveloperAgent()
    frontend_dev = FrontendDeveloperAgent()
    
    # Create agency with communication flows
    agency = Agency(
        agents=[
            manager,  # Manager is the entry point
            [manager, backend_dev],  # Manager can delegate to backend developer
            [manager, frontend_dev],  # Manager can delegate to frontend developer
            [backend_dev, frontend_dev],  # Backend dev can communicate with frontend dev
        ],
        shared_instructions="agency_manifesto.md"
    )
    
    return agency

if __name__ == "__main__":
    # Create and run the agency
    agency = create_dev_agency()
    agency.run_demo() 