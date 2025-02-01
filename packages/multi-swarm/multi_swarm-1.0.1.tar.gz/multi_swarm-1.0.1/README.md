# Multi-Swarm Framework

[![PyPI version](https://badge.fury.io/py/multi-swarm.svg)](https://badge.fury.io/py/multi-swarm)
[![CI](https://github.com/bartvanspitaels99/multi-swarm/actions/workflows/ci.yml/badge.svg)](https://github.com/bartvanspitaels99/multi-swarm/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/bartvanspitaels99/multi-swarm/branch/main/graph/badge.svg)](https://codecov.io/gh/bartvanspitaels99/multi-swarm)
[![Python Versions](https://img.shields.io/pypi/pyversions/multi-swarm.svg)](https://pypi.org/project/multi-swarm/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful framework for creating collaborative AI agent swarms, enabling complex task completion through coordinated agent interactions.

## Features

- Create specialized AI agents with distinct roles and capabilities
- Configure communication flows between agents
- Manage shared resources and knowledge
- Support for multiple LLM providers (Claude and Gemini)
- Built-in security and resource management

## Installation

Basic installation:
```bash
pip install multi-swarm
```

For development installation with testing tools:
```bash
pip install multi-swarm[dev]
```

## Environment Setup

1. Set up your environment variables:
```bash
# .env
ANTHROPIC_API_KEY=your_claude_api_key
GOOGLE_API_KEY=your_gemini_api_key
```

2. If using Cursor AI (recommended):
   - Copy the `.cursorrules` file to your project's root directory
   - This file contains essential instructions for Cursor's Claude agent to better assist with Multi-Swarm development
   - The `.cursorrules` file helps maintain consistent agent behavior and framework best practices

## Quick Start

1. Create a custom agent:
```python
from multi_swarm import Agent

class MyAgent(Agent):
    def __init__(self):
        super().__init__(
            name="MyAgent",
            description="A custom agent for specific tasks",
            instructions="path/to/instructions.md",
            tools_folder="path/to/tools",
            llm_provider="claude",  # or "gemini" - framework automatically selects best model
            provider_config={
                "model": "claude-3-5-sonnet-latest",  # Latest Claude model
                "max_tokens": 4096,
                "api_version": "2024-03"
            },
            temperature=0.7
        )
```

2. Create and run your agency:
```python
from multi_swarm import Agency

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

## LLM Provider Configuration

The framework automatically selects the most appropriate LLM model based on the agent's role:

### Claude Models (Anthropic)
- Default model: `claude-3-5-sonnet-latest`
- API version: `2024-03`
- Used for: Complex reasoning, code generation, and detailed analysis
- Best for agents handling: Research, documentation, code review, planning

### Gemini Models (Google)
- Default model: `gemini-2.0-flash-exp`
- API version: `2024-01`
- Used for: Quick responses, data processing, and technical tasks
- Best for agents handling: Data analysis, API integration, system operations

The framework intelligently switches between providers based on:
- Task complexity
- Required capabilities
- Response time needs
- Cost considerations

## Examples

Check out the `examples` directory for complete implementations:
- Research Assistant Agency
- Development Agency
- Trends Analysis Agency

## Documentation

Full documentation is available at [docs/](docs/).

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 