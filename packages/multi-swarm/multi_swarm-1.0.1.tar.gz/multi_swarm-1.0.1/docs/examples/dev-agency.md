# Development Agency Example

This example demonstrates how to create a development team using Multi-Swarm, combining the strategic capabilities of Gemini with the technical expertise of Claude.

## Agency Structure

The development agency consists of three agents:

1. **Project Manager** (Gemini 2.0 Pro)
   - Handles project planning and coordination
   - Breaks down requirements into tasks
   - Assigns work to developers

2. **Backend Developer** (Claude 3.5 Sonnet)
   - Implements server-side logic
   - Designs and creates APIs
   - Manages database operations

3. **Frontend Developer** (Claude 3.5 Sonnet)
   - Creates user interfaces
   - Implements client-side features
   - Handles UI/UX concerns

## Implementation

### 1. Create the Agency

```python
from multi_swarm import Agency
from manager import ManagerAgent
from backend_developer import BackendDeveloperAgent
from frontend_developer import FrontendDeveloperAgent

def create_dev_agency():
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
```

### 2. Define Agents

#### Project Manager

```python
from multi_swarm import BaseAgent

class ManagerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Project Manager",
            description="Strategic leader responsible for project planning and coordination.",
            instructions="manager_instructions.md",
            tools_folder="./tools",
            model="gemini-2.0-pro",
            temperature=0.7
        )
```

#### Backend Developer

```python
class BackendDeveloperAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Backend Developer",
            description="Technical expert in backend development and API design.",
            instructions="backend_developer_instructions.md",
            tools_folder="./tools",
            model="claude-3.5-sonnet",
            temperature=0.5
        )
```

### 3. Create Instructions

Each agent needs clear instructions defining their role and responsibilities. Here's an example for the Project Manager:

```markdown
# Project Manager Role

You are a project manager in a development team. Your role is to:
1. Understand project requirements and user needs
2. Break down tasks into clear development assignments
3. Coordinate between backend and frontend developers
4. Ensure project goals are met efficiently

# Goals

1. Deliver high-quality software projects on time
2. Maintain clear communication between team members
3. Ensure efficient task allocation and coordination
4. Identify and resolve potential bottlenecks
5. Keep development aligned with project requirements
```

## Usage Example

```python
# Create and run the agency
agency = create_dev_agency()

# Example interaction
response = await agency.process_message("""
Create a new user registration API with the following requirements:
- Email and password authentication
- User profile information
- Email verification
- Password reset functionality
""")

print(response)
```

The Project Manager will:
1. Analyze the requirements
2. Break them down into backend and frontend tasks
3. Coordinate with both developers to implement the feature

## Best Practices

1. **Clear Communication Flows**
   - Define who can communicate with whom
   - Establish clear chains of command
   - Enable necessary cross-team collaboration

2. **Role Separation**
   - Keep agent responsibilities distinct
   - Allow specialization in specific areas
   - Minimize role overlap

3. **Temperature Settings**
   - Use higher temperature (0.7) for creative tasks
   - Use lower temperature (0.5) for technical tasks
   - Adjust based on task requirements

4. **Model Selection**
   - Use Gemini for high-level planning
   - Use Claude for technical implementation
   - Match model strengths to tasks

## Complete Example

The complete example is available in the [examples/dev_agency](https://github.com/yourusername/multi_swarm/tree/main/examples/dev_agency) directory of the Multi-Swarm repository. 