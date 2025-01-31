# Multi-Swarm: Multi-LLM Agent Framework

A framework for creating collaborative AI agents using multiple LLM providers (Google's Gemini and Anthropic's Claude).

## Features

- Multi-LLM Support: Leverage different LLM providers for specialized tasks
- Flexible Agent Architecture: Create custom agents with specific roles and capabilities
- Structured Communication: Define clear communication flows between agents
- Easy Integration: Simple API for creating and running agent swarms

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Environment Setup

Create a `.env` file in your project root with your API keys:

```env
GOOGLE_API_KEY=your_gemini_api_key
ANTHROPIC_API_KEY=your_claude_api_key
```

## Usage

### Basic Example

```python
from multi_swarm import Agency, CEOAgent, TrendsAnalyst

# Initialize agents
ceo = CEOAgent()  # Uses Gemini 2.0 Pro
analyst = TrendsAnalyst()  # Uses Claude 3.5 Sonnet

# Create agency with communication flows
agency = Agency(
    agents=[
        ceo,  # CEO is the entry point
        [ceo, analyst],  # CEO can delegate to analyst
    ],
    shared_instructions="agency_manifesto.md"
)

# Run the agency
agency.run_demo()
```

### Custom Agent Creation

1. Create a new agent class:

```python
from multi_swarm import BaseAgent

class CustomAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Custom Agent",
            description="Description of the agent's role",
            instructions="path/to/instructions.md",
            tools_folder="path/to/tools",
            model="model-name",  # gemini-2.0-pro or claude-3.5-sonnet
            temperature=0.7
        )
```

2. Create instructions for your agent in a markdown file
3. Add any custom tools in the agent's tools folder
4. Integrate the agent into your agency's communication flow

## License

MIT License - see LICENSE file for details 