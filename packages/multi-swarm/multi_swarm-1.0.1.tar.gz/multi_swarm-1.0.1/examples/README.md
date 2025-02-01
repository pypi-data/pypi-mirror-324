# Multi-Swarm Examples

This directory contains example implementations of Multi-Swarm agencies and agents. These examples demonstrate different use cases and features of the framework.

## Directory Structure

```
examples/
├── auto_select_agency/     # Demonstrates automatic model selection
├── research_assistant/     # Research assistant with multiple specialized agents
├── dev_agency/            # Development team simulation
└── trends_analysis/       # Google Trends analysis agency
```

## Using the Examples

Each example directory contains:
- A complete agency implementation
- Custom agent definitions
- Required instructions and tools
- A README with specific setup instructions

### Running an Example

1. Install Multi-Swarm:
```bash
pip install multi-swarm
```

2. Set up environment variables:
```bash
# .env
ANTHROPIC_API_KEY=your_claude_api_key
GOOGLE_API_KEY=your_gemini_api_key
```

3. Navigate to an example directory:
```bash
cd examples/auto_select_agency
```

4. Run the example:
```bash
python agency.py
```

## Example Descriptions

### Auto-Select Agency
Demonstrates how Multi-Swarm automatically selects the most appropriate LLM model based on agent roles:
- Code Reviewer (Claude) for complex reasoning
- Data Analyst (Gemini) for data processing
- System Monitor (Gemini) for operations

### Research Assistant Agency
A collaborative agency for research tasks:
- Research Manager for coordination
- Data Analyst for numerical analysis
- Document Processor for text analysis

### Development Agency
Simulates a development team:
- Project Manager for coordination
- Backend Developer for server-side tasks
- Frontend Developer for client-side tasks

### Trends Analysis Agency
Analyzes Google Trends data:
- CEO for strategic decisions
- Trends Analyst for data processing
- Report Generator for visualization

## Creating Your Own Agency

Use these examples as templates for creating your own agencies. Key steps:

1. Define your agents:
```python
from multi_swarm import Agent

class MyAgent(Agent):
    def __init__(self):
        super().__init__(
            name="MyAgent",
            description="Description that determines model selection",
            instructions="path/to/instructions.md",
            tools_folder="path/to/tools"
        )
```

2. Create your agency:
```python
from multi_swarm import Agency

agency = Agency(
    agents=[
        my_agent,  # Entry point
        [my_agent, other_agent]  # Communication flow
    ],
    shared_instructions="agency_manifesto.md"
)
```

3. Run your agency:
```python
agency.run_demo()
```

## Best Practices

1. **Agent Design**
   - Give clear, specific descriptions
   - Let the framework handle model selection
   - Keep agents focused on single responsibilities

2. **Communication Flows**
   - Define clear hierarchies
   - Minimize unnecessary connections
   - Document flow purposes

3. **Instructions**
   - Provide detailed agent instructions
   - Include example interactions
   - Define clear boundaries

4. **Tools**
   - Create focused, reusable tools
   - Handle errors gracefully
   - Document tool purposes and usage 