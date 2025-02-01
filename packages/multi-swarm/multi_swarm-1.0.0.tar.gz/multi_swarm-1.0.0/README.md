# Multi-Swarm Framework

[![PyPI version](https://badge.fury.io/py/multi-swarm.svg)](https://badge.fury.io/py/multi-swarm)
[![CI](https://github.com/bartvanspitaels99/multi-swarm/actions/workflows/ci.yml/badge.svg)](https://github.com/bartvanspitaels99/multi-swarm/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/bartvanspitaels99/multi-swarm/branch/main/graph/badge.svg)](https://codecov.io/gh/bartvanspitaels99/multi-swarm)
[![Python Versions](https://img.shields.io/pypi/pyversions/multi-swarm.svg)](https://pypi.org/project/multi-swarm/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful framework for creating collaborative AI agent swarms, leveraging multiple LLM providers including Claude and Gemini.

## Features

- Create collaborative agent swarms with distinct roles and capabilities
- Support for multiple LLM providers (Claude and Gemini)
- Easy-to-use agent template creation
- Flexible agency configuration
- Built-in tools system
- Asynchronous communication between agents

## Installation

```bash
pip install multi-swarm
```

For development installation with testing tools:

```bash
pip install multi-swarm[dev]
```

## Quick Start

1. Set up your environment variables:

```bash
# .env
ANTHROPIC_API_KEY=your_claude_api_key
GOOGLE_API_KEY=your_gemini_api_key
```

2. Create a simple agency:

```python
from multi_swarm import Agency, BaseAgent

# Create custom agents
class MyAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="MyAgent",
            description="A custom agent for specific tasks",
            instructions="path/to/instructions.md",
            tools_folder="path/to/tools",
            model="claude-3-sonnet",
            temperature=0.7
        )

# Initialize agents
agent1 = MyAgent()
agent2 = MyAgent()

# Create agency with communication flows
agency = Agency(
    agents=[
        agent1,  # Entry point for user communication
        [agent1, agent2],  # agent1 can communicate with agent2
    ],
    shared_instructions="agency_manifesto.md"
)

# Run the agency
agency.run_demo()
```

## Examples

Check out our example implementations in the [examples](examples/) directory:

1. [Google Trends Analysis Agency](examples/trends_analysis_agency/): Shows how to create a specialized agency for analyzing Google Trends data. This example demonstrates:
   - Custom agent creation (CEO and TrendsAnalyst)
   - Communication flow setup
   - Agent instructions and tools structure
   - Basic agency configuration

## Documentation

For detailed documentation, please visit our [GitHub repository](https://github.com/bartvanspitaels99/multi-swarm).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. Here are some ways you can contribute:

- Add new agent types
- Implement useful tools
- Improve documentation
- Add tests
- Report bugs
- Suggest features

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 