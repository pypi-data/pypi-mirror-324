"""
Example agency demonstrating automatic model selection based on agent roles.
"""

from multi_swarm import Agency, Agent

class CodeReviewAgent(Agent):
    """Agent specialized in code review and documentation."""
    def __init__(self):
        super().__init__(
            name="Code Reviewer",
            description="Technical expert in code review, documentation, and best practices",
            instructions="./instructions/code_reviewer.md",
            tools_folder="./tools/code_reviewer",
            # Will automatically select Claude due to code/documentation keywords
        )

class DataAnalystAgent(Agent):
    """Agent specialized in data analysis and processing."""
    def __init__(self):
        super().__init__(
            name="Data Analyst",
            description="Expert in data processing, analysis, and visualization",
            instructions="./instructions/data_analyst.md",
            tools_folder="./tools/data_analyst",
            # Will automatically select Gemini due to data processing keywords
        )

class SystemMonitorAgent(Agent):
    """Agent specialized in system monitoring and operations."""
    def __init__(self):
        super().__init__(
            name="System Monitor",
            description="Handles system operations, monitoring, and integration tasks",
            instructions="./instructions/system_monitor.md",
            tools_folder="./tools/system_monitor",
            # Will automatically select Gemini due to operations/monitoring keywords
        )

def create_agency():
    """Create an agency with agents using different models based on their roles."""
    # Initialize agents
    code_reviewer = CodeReviewAgent()
    data_analyst = DataAnalystAgent()
    system_monitor = SystemMonitorAgent()
    
    # Create agency with communication flows
    agency = Agency(
        name="Auto-Select Demo Agency",
        description="Demonstrates automatic model selection based on agent roles",
        agents=[
            code_reviewer,  # Entry point
            [code_reviewer, data_analyst],  # Code reviewer can delegate analysis tasks
            [code_reviewer, system_monitor],  # Code reviewer can request system info
            [data_analyst, system_monitor]  # Data analyst can access system metrics
        ],
        shared_instructions="./instructions/agency_manifesto.md",
        use_code_interpreter=True,
        use_rag=True,
        use_file_storage=True
    )
    
    return agency

if __name__ == "__main__":
    print("Starting Auto-Select Demo Agency")
    print("\nThis agency demonstrates how Multi-Swarm automatically selects")
    print("the most appropriate LLM model based on each agent's role:")
    print("\n1. Code Reviewer: Uses Claude for complex reasoning and code analysis")
    print("2. Data Analyst: Uses Gemini for efficient data processing")
    print("3. System Monitor: Uses Gemini for quick operational tasks")
    print("\nType 'exit' to end the conversation.\n")
    
    agency = create_agency()
    agency.run_demo() 