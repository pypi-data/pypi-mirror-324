# Core API Reference

This document provides detailed information about the core classes and functions in Multi-Swarm.

## Agent

The foundation class for all agents in Multi-Swarm.

### Constructor

```python
def __init__(
    self,
    name: str,
    description: str,
    instructions: str,
    tools_folder: str,
    llm_provider: Optional[str] = None,
    provider_config: Optional[Dict[str, Any]] = None,
    temperature: float = 0.7,
    storage_path: Optional[str] = None,
    use_file_storage: bool = False,
    use_rag: bool = False,
    use_code_interpreter: bool = False
)
```

#### Parameters

- **name** (str): Unique identifier for the agent
- **description** (str): Description of the agent's role and capabilities
- **instructions** (str): Path to instructions file
- **tools_folder** (str): Path to tools directory
- **llm_provider** (str, optional): LLM provider to use ("claude" or "gemini")
- **provider_config** (Dict, optional): Provider-specific settings
- **temperature** (float, optional): Response randomness (0.0-1.0)
- **storage_path** (str, optional): Path for persistent storage
- **use_file_storage** (bool): Enable file storage capabilities
- **use_rag** (bool): Enable RAG capabilities
- **use_code_interpreter** (bool): Enable code interpreter

### Automatic Model Selection

The framework automatically selects the most appropriate LLM model based on the agent's description:

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

### Methods

#### process_message

```python
def process_message(
    self,
    thread_id: str,
    content: str,
    role: str = "user",
    metadata: Dict = None
) -> Message:
    """Process a message in a thread."""
```

#### create_thread

```python
def create_thread(
    self,
    metadata: Dict = None
) -> Thread:
    """Create a new conversation thread."""
```

#### upload_file

```python
def upload_file(
    self,
    file: Any,
    filename: str,
    purpose: str = "attachment",
    metadata: Dict = None
):
    """Upload a file to storage."""
```

#### execute_code

```python
def execute_code(
    self,
    code: str,
    language: str = "python",
    additional_files: Dict[str, str] = None,
    environment: Dict[str, str] = None
):
    """Execute code in the secure environment."""
```

#### search_knowledge

```python
def search_knowledge(
    self,
    query: str,
    k: int = 5,
    threshold: float = None
):
    """Search the knowledge base using RAG."""
```

## Agency

The main class for managing agent interactions.

### Constructor

```python
def __init__(
    self,
    name: str,
    description: str,
    agents: List[Agent],
    flows: List[Tuple[str, str]],
    storage_path: Optional[str] = None,
    shared_instructions: Optional[str] = None,
    default_temperature: float = 0.7,
    default_max_tokens: int = 4096,
    use_code_interpreter: bool = False,
    use_rag: bool = False,
    use_file_storage: bool = False
)
```

#### Parameters

- **name** (str): Name of the agency
- **description** (str): Description of the agency's purpose
- **agents** (List[Agent]): List of agents in the agency
- **flows** (List[Tuple[str, str]]): Communication flows between agents
- **storage_path** (str, optional): Path for persistent storage
- **shared_instructions** (str, optional): Path to shared instructions
- **default_temperature** (float): Default temperature for agents
- **default_max_tokens** (int): Default max tokens for agents
- **use_code_interpreter** (bool): Enable code interpreter
- **use_rag** (bool): Enable RAG capabilities
- **use_file_storage** (bool): Enable file storage

### Methods

#### send_message

```python
def send_message(
    self,
    source: str,
    target: str,
    content: str,
    metadata: Dict = None
) -> Message:
    """Send a message from one agent to another."""
```

#### broadcast_message

```python
def broadcast_message(
    self,
    source: str,
    content: str,
    metadata: Dict = None
) -> List[Message]:
    """Broadcast a message to all connected agents."""
```

#### run_demo

```python
def run_demo(self):
    """Run an interactive demo of the agency."""
```

## Thread

Represents a conversation thread between agents.

```python
class Thread(BaseModel):
    id: str
    messages: List[Message]
    metadata: Dict
    created_at: datetime
    last_active_at: datetime
    status: str
```

## Message

Represents a message in a conversation thread.

```python
class Message(BaseModel):
    role: str
    content: str
    agent_name: str
    file_ids: List[str]
    metadata: Dict
    created_at: datetime
```

## Configuration

### Environment Variables

```bash
# Required for Claude
ANTHROPIC_API_KEY=your_claude_key

# Required for Gemini
GOOGLE_API_KEY=your_gemini_key
```

### Default Configurations

```python
# Claude Configuration
CLAUDE_CONFIG = {
    "model": "claude-3-5-sonnet-latest",
    "max_tokens": 4096,
    "api_version": "2024-03"
}

# Gemini Configuration
GEMINI_CONFIG = {
    "model": "gemini-2.0-flash-exp",
    "max_tokens": 4096,
    "api_version": "2024-01"
}
```

## Usage Example

```python
from multi_swarm import Agency, Agent

# Create custom agent
class DevelopmentAgent(Agent):
    def __init__(self):
        super().__init__(
            name="Developer",
            description="Code generation and review specialist",
            instructions="instructions.md",
            tools_folder="./tools",
            # Let the framework choose between Claude and Gemini
            temperature=0.7,
            use_code_interpreter=True
        )

# Create agency
dev_agent = DevelopmentAgent()
qa_agent = QAAgent()

agency = Agency(
    name="Development Team",
    description="Software development team simulation",
    agents=[dev_agent, qa_agent],
    flows=[
        (dev_agent.name, qa_agent.name),
        (qa_agent.name, dev_agent.name)
    ],
    shared_instructions="manifesto.md",
    use_code_interpreter=True
)

# Run interactive demo
agency.run_demo()
```

## Learn More

- [Agent API](agents.md)
- [Tool API](tools.md)
- [Agency API](agency.md)
- [User Guide](../user-guide/creating-agents.md) 