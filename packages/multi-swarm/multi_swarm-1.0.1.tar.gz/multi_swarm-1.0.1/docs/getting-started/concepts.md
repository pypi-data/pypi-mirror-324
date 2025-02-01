# Basic Concepts

Multi-Swarm is built around several core concepts that work together to create powerful AI agent collaborations.

## Core Components

### 1. Agents

Agents are autonomous AI entities with specific roles and capabilities:

- Each agent has a defined purpose and set of responsibilities
- Agents automatically use the most appropriate LLM model based on their role
- Agents can have their own tools, storage, and knowledge base
- Agents communicate through structured conversation threads

Example:
```python
class AnalystAgent(Agent):
    def __init__(self):
        super().__init__(
            name="Data Analyst",
            description="Expert in data analysis and visualization",
            instructions="analyst_instructions.md",
            tools_folder="./tools",
            # Framework will automatically select between Claude and Gemini
            temperature=0.5,
            use_code_interpreter=True
        )
```

### 2. Tools

Tools are specific actions that agents can perform:

- Tools are Python classes that inherit from `BaseTool`
- Tools use Pydantic for input validation
- Tools can access shared resources and external services
- Tools are automatically loaded from the agent's tools folder

Example:
```python
from pydantic import BaseModel, Field

class DataVisualizationTool(BaseModel):
    """Tool for creating data visualizations."""
    data: List[Dict] = Field(..., description="Data to visualize")
    chart_type: str = Field(..., description="Type of chart to create")

    def run(self):
        # Tool implementation
        return "Visualization created"
```

### 3. Agencies

Agencies are collections of agents working together:

- Agencies define communication flows between agents
- Agencies can share resources (files, code interpreter, knowledge base)
- Agencies manage conversation threads and message routing
- Agencies provide monitoring and state management

Example:
```python
agency = Agency(
    name="Development Team",
    description="Software development team simulation",
    agents=[manager, developer, tester],
    flows=[
        (manager.name, developer.name),   # Manager can talk to developer
        (developer.name, tester.name),    # Developer can talk to tester
    ],
    shared_instructions="manifesto.md",
    use_code_interpreter=True
)
```

## Key Concepts

### 1. Communication Flows

- **Thread-Based**: All communication happens in conversation threads
- **Directional**: Agents can only communicate in defined directions
- **Metadata Support**: Messages can include metadata and file attachments
- **History Tracking**: Full conversation history is maintained

### 2. Automatic Model Selection

The framework automatically selects the best model based on the agent's role:

```python
TASK_PREFERENCES = {
    "code": "claude",      # Code generation and review
    "research": "claude",  # Research and analysis
    "planning": "claude",  # Strategic planning
    "documentation": "claude",  # Documentation generation
    "data": "gemini",     # Data processing and analysis
    "integration": "gemini",  # API and system integration
    "operations": "gemini",  # System operations
    "monitoring": "gemini"  # System monitoring
}
```

### 3. Instructions

Instructions are markdown files that define agent behavior:

```markdown
# Agent Role
Detailed description of the agent's role and purpose.

# Goals
1. Primary objective
2. Secondary objectives
3. Success criteria

# Process Workflow
1. Step-by-step process
2. Decision points
3. Interaction guidelines

# Communication Guidelines
1. How to interact with other agents
2. Message formatting
3. Response expectations
```

### 4. Advanced Features

- **File Storage**: Agents can store and share files
- **Code Interpreter**: Secure Python code execution environment
- **RAG System**: Knowledge base with semantic search
- **State Management**: Persistent storage of conversations and data

## Design Patterns

### 1. Hierarchical Organization

```python
# Manager delegates to specialists
agency = Agency(
    name="Management Team",
    description="Hierarchical team structure",
    agents=[manager, specialist1, specialist2],
    flows=[
        (manager.name, specialist1.name),
        (manager.name, specialist2.name)
    ]
)
```

### 2. Peer Collaboration

```python
# Agents work together as peers
agency = Agency(
    name="Research Team",
    description="Collaborative research team",
    agents=[coordinator, peer1, peer2],
    flows=[
        (peer1.name, peer2.name),
        (peer2.name, peer1.name)
    ]
)
```

### 3. Pipeline Processing

```python
# Sequential processing chain
agency = Agency(
    name="Content Pipeline",
    description="Content processing workflow",
    agents=[intake, processor, reviewer, publisher],
    flows=[
        (intake.name, processor.name),
        (processor.name, reviewer.name),
        (reviewer.name, publisher.name)
    ]
)
```

## Best Practices

1. **Agent Design**
   - Write clear, task-focused descriptions
   - Let the framework handle model selection
   - Enable only needed features (RAG, code interpreter, etc.)
   - Implement proper error handling

2. **Tool Implementation**
   - Create focused, reusable tools
   - Use Pydantic for input validation
   - Handle errors gracefully
   - Document tool functionality clearly

3. **Agency Structure**
   - Define minimal necessary communication paths
   - Group related agents together
   - Share resources appropriately
   - Monitor performance and usage

4. **Resource Management**
   - Use appropriate storage paths
   - Clean up temporary files
   - Manage memory usage
   - Handle concurrent access

## Learn More

- [Creating Agents](../user-guide/creating-agents.md)
- [Creating Tools](../user-guide/creating-tools.md)
- [Agency Patterns](../user-guide/creating-agencies.md)
- [API Reference](../api/core.md) 