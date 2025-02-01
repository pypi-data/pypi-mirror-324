# Creating Agents

Agents are the core building blocks of Multi-Swarm. Each agent has specific roles, capabilities, and tools.

## Basic Agent Creation

```python
from multi_swarm import Agent

class DataAnalyst(Agent):
    def __init__(self):
        super().__init__(
            name="Data Analyst",
            description="Expert in data analysis and visualization",
            instructions="analyst_instructions.md",
            tools_folder="./tools",
            temperature=0.5,
            use_rag=True  # Enable knowledge base
        )
```

## Agent Parameters

- **name** (str): Unique identifier for the agent
- **description** (str): Detailed description of agent's role and capabilities
- **instructions** (str): Path to markdown file containing agent instructions
- **tools_folder** (str): Path to folder containing agent's tools
- **temperature** (float, optional): Model temperature (0.0-1.0)
- **use_rag** (bool, optional): Enable Retrieval-Augmented Generation
- **llm_provider** (str, optional): Manually specify LLM provider ("claude" or "gemini")
- **provider_config** (dict, optional): Provider-specific configuration

## Automatic Model Selection

The framework automatically selects the most appropriate model based on the agent's description and role:

### Claude (Anthropic)
- Complex reasoning tasks
- Code generation and review
- Technical writing
- API design
- Documentation

### Gemini (Google)
- Data processing
- System operations
- Real-time tasks
- Pattern recognition
- Monitoring

## Agent Instructions

Create an `instructions.md` file to define the agent's behavior:

```markdown
# Agent Role

Detailed description of the agent's role and responsibilities.

# Goals

- Goal 1: Description
- Goal 2: Description
- Goal 3: Description

# Process Workflow

1. Step 1: Description
2. Step 2: Description
3. Step 3: Description

# Guidelines

- Guideline 1
- Guideline 2
- Guideline 3
```

## Advanced Features

### 1. Knowledge Base (RAG)

```python
class ResearchAgent(Agent):
    def __init__(self):
        super().__init__(
            name="Researcher",
            description="Research and analysis specialist",
            instructions="researcher_instructions.md",
            tools_folder="./tools",
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
class DevAgent(Agent):
    def __init__(self):
        super().__init__(
            name="Developer",
            description="Software development and testing",
            instructions="dev_instructions.md",
            tools_folder="./tools",
            use_code_interpreter=True,
            interpreter_config={
                "timeout": 30,
                "memory_limit": "1G"
            }
        )
```

### 3. File Storage

```python
class DataAgent(Agent):
    def __init__(self):
        super().__init__(
            name="Data Manager",
            description="Data management and processing",
            instructions="data_instructions.md",
            tools_folder="./tools",
            use_file_storage=True,
            storage_config={
                "base_path": "./data",
                "max_size": "5G"
            }
        )
```

## Error Handling

```python
from multi_swarm.exceptions import AgentError

try:
    response = await agent.process_message(message)
except AgentError as e:
    if "tool_error" in str(e):
        # Handle tool execution error
        await handle_tool_error(e)
    elif "provider_error" in str(e):
        # Handle LLM provider error
        await handle_provider_error(e)
    else:
        # Handle other agent errors
        raise
```

## Best Practices

1. **Agent Design**
   - Clear, focused roles
   - Detailed descriptions
   - Comprehensive instructions
   - Appropriate tool selection

2. **Resource Management**
   - Enable RAG for knowledge-intensive tasks
   - Use Code Interpreter for development tasks
   - Implement proper error handling
   - Monitor resource usage

3. **Performance Optimization**
   - Optimize prompt length
   - Use appropriate batch sizes
   - Monitor response times
   - Cache frequently used data

## Examples

### 1. Development Agent

```python
class DevAgent(Agent):
    def __init__(self):
        super().__init__(
            name="Developer",
            description="Expert in software development, code review, and testing",
            instructions="dev_instructions.md",
            tools_folder="./tools",
            use_code_interpreter=True,
            use_rag=True  # For codebase knowledge
        )
```

### 2. Data Analysis Agent

```python
class AnalystAgent(Agent):
    def __init__(self):
        super().__init__(
            name="Data Analyst",
            description="Specialist in data processing and visualization",
            instructions="analyst_instructions.md",
            tools_folder="./tools",
            use_file_storage=True,
            use_rag=True
        )
```

### 3. Research Agent

```python
class ResearchAgent(Agent):
    def __init__(self):
        super().__init__(
            name="Researcher",
            description="Expert in research, analysis, and report generation",
            instructions="researcher_instructions.md",
            tools_folder="./tools",
            use_rag=True,
            use_file_storage=True
        )
```

## Learn More

- [Creating Tools](creating-tools.md)
- [Creating Agencies](creating-agencies.md)
- [Communication Flows](communication-flows.md) 