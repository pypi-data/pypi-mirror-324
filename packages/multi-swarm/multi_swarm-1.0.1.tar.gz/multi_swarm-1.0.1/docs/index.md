# Multi-Swarm Framework Documentation

Multi-Swarm is a powerful framework for creating collaborative AI agent systems (Agencies). It enables automatic model selection between Claude and Gemini based on agent roles, with built-in support for advanced features like RAG, Code Interpreter, and File Storage.

## Quick Start

```python
from multi_swarm import Agency, Agent

# Create specialized agents
dev = DevAgent(
    name="Developer",
    description="Code generation and technical analysis",
    instructions="dev_instructions.md",
    tools_folder="./tools",
    # Framework automatically selects Claude for code tasks
    use_code_interpreter=True
)

analyst = DataAnalyst(
    name="Data Analyst",
    description="Data processing and visualization",
    instructions="analyst_instructions.md",
    tools_folder="./tools",
    # Framework automatically selects Gemini for data tasks
    use_rag=True
)

# Create agency with communication flows
agency = Agency([
    dev,  # Entry point
    [dev, analyst]  # Dev can communicate with Analyst
],
    shared_instructions="agency_manifesto.md"
)

# Run agency in terminal
agency.run_demo()
```

## Installation

1. Install via pip:
```bash
pip install multi-swarm
```

2. Set up environment variables:
```bash
# For Claude integration
export ANTHROPIC_API_KEY=your_api_key

# For Gemini integration
export GOOGLE_API_KEY=your_api_key
```

3. For Cursor AI users:
```bash
# Copy .cursorrules to root directory
cp path/to/multi-swarm/.cursorrules .
```

## Core Concepts

1. **Agents**: Specialized AI agents with distinct roles and capabilities
   - Automatic model selection (Claude/Gemini)
   - Role-specific tools and instructions
   - Advanced features (RAG, Code Interpreter, File Storage)

2. **Agencies**: Collections of collaborating agents
   - Structured communication flows
   - Thread-based conversations
   - Resource sharing and coordination

3. **Tools**: Custom actions agents can perform
   - Input validation with Pydantic
   - Error handling and resource management
   - Async support and progress tracking

## Model Selection

The framework automatically selects the most appropriate model based on agent roles:

### Claude (Anthropic)
- Code generation and review
- Complex reasoning tasks
- Technical documentation
- API design
- Strategic planning

### Gemini (Google)
- Data processing and analysis
- System operations
- Real-time tasks
- Pattern recognition
- Monitoring and alerting

## Documentation Sections

### Getting Started
- [Installation Guide](getting-started/installation.md)
- [Quick Start Guide](getting-started/quickstart.md)
- [Core Concepts](getting-started/concepts.md)

### User Guide
- [Creating Agents](user-guide/creating-agents.md)
- [Creating Tools](user-guide/creating-tools.md)
- [Creating Agencies](user-guide/creating-agencies.md)
- [Communication Flows](user-guide/communication-flows.md)

### LLM Providers
- [Claude Integration](providers/claude.md)
- [Gemini Integration](providers/gemini.md)

### Examples
- [Development Agency](examples/dev-agency.md)
- [Research Agency](examples/research-agency.md)
- [Data Processing Agency](examples/data-agency.md)

### API Reference
- [Agency API](api/agency.md)
- [Agent API](api/agents.md)
- [Tool API](api/tools.md)

## Advanced Features

### 1. Knowledge Base (RAG)
```python
agent = Agent(
    name="Researcher",
    use_rag=True,
    rag_config={
        "index_name": "research_data",
        "embedding_model": "all-MiniLM-L6-v2",
        "chunk_size": 1000
    }
)
```

### 2. Code Interpreter
```python
agent = Agent(
    name="Developer",
    use_code_interpreter=True,
    interpreter_config={
        "timeout": 30,
        "memory_limit": "1G"
    }
)
```

### 3. File Storage
```python
agent = Agent(
    name="Data Manager",
    use_file_storage=True,
    storage_config={
        "base_path": "./data",
        "max_size": "5G"
    }
)
```

## Best Practices

1. **Agent Design**
   - Clear, focused roles
   - Detailed descriptions for model selection
   - Comprehensive instructions
   - Appropriate tool selection

2. **Resource Management**
   - Enable RAG for knowledge-intensive tasks
   - Use Code Interpreter for development
   - Implement proper error handling
   - Monitor resource usage

3. **Performance Optimization**
   - Optimize message routing
   - Use appropriate batch sizes
   - Monitor response times
   - Cache frequently used data

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

For more details, see [CONTRIBUTING.md](CONTRIBUTING.md)

## Support

- [GitHub Issues](https://github.com/yourusername/multi-swarm/issues)
- [Documentation](https://multi-swarm.readthedocs.io)
- [Discord Community](https://discord.gg/multi-swarm)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 