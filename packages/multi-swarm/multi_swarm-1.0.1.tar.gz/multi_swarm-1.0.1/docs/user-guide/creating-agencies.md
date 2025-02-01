# Creating Agencies

Agencies are collections of agents that work together to achieve complex goals. Each agency has a clear structure, communication flows, and shared resources.

## Basic Agency Structure

```python
from multi_swarm import Agency, Agent

# Create agents
dev = DevAgent()
analyst = DataAnalyst()
researcher = ResearchAgent()

# Create agency with communication flows
agency = Agency([
    dev,  # Entry point for user communication
    [dev, analyst],  # Dev can communicate with Analyst
    [dev, researcher],  # Dev can communicate with Researcher
    [analyst, researcher]  # Analyst can communicate with Researcher
],
    shared_instructions="agency_manifesto.md",
    temperature=0.5
)

if __name__ == "__main__":
    agency.run_demo()  # Start agency in terminal
```

## Agency Components

1. **Agents**
   - Entry point agent for user communication
   - Specialist agents for specific tasks
   - Support agents for auxiliary functions

2. **Communication Flows**
   - Directional communication paths
   - Message routing and history
   - Thread management

3. **Shared Resources**
   - Instructions and guidelines
   - Knowledge bases
   - File storage

## Agency Manifesto

Create an `agency_manifesto.md` file:

```markdown
# Agency Mission

Clear statement of the agency's purpose and goals.

# Operating Environment

Description of the context and constraints.

# Communication Guidelines

- Message format standards
- Response expectations
- Error handling procedures

# Resource Management

- Knowledge base usage
- File storage policies
- API access guidelines
```

## Advanced Features

### 1. Custom Message Routing

```python
class CustomAgency(Agency):
    async def route_message(self, message, from_agent, to_agent):
        """Custom message routing logic."""
        # Add metadata
        message.metadata["priority"] = self._get_priority(message)
        
        # Route message
        return await super().route_message(message, from_agent, to_agent)
```

### 2. Shared State Management

```python
class StatefulAgency(Agency):
    def __init__(self, agents, **kwargs):
        super().__init__(agents, **kwargs)
        self.shared_state = {}
    
    async def process_message(self, message):
        """Process with shared state."""
        context = self.shared_state.get(message.thread_id, {})
        return await super().process_message(message, context)
```

### 3. Resource Coordination

```python
class ResourceAgency(Agency):
    def __init__(self, agents, **kwargs):
        super().__init__(agents, **kwargs)
        self.resource_pool = ResourcePool()
    
    async def allocate_resources(self, agent, request):
        """Manage resource allocation."""
        return await self.resource_pool.allocate(agent, request)
```

## Example Agencies

### 1. Development Agency

```python
# Create specialized agents
dev_lead = DevAgent(
    name="Lead Developer",
    description="Technical leadership and code review",
    instructions="lead_dev_instructions.md"
)

code_reviewer = DevAgent(
    name="Code Reviewer",
    description="Code quality and security analysis",
    instructions="reviewer_instructions.md"
)

qa_engineer = DevAgent(
    name="QA Engineer",
    description="Testing and quality assurance",
    instructions="qa_instructions.md"
)

# Create development agency
dev_agency = Agency([
    dev_lead,  # Entry point
    [dev_lead, code_reviewer],
    [dev_lead, qa_engineer],
    [code_reviewer, qa_engineer]
],
    shared_instructions="dev_agency_manifesto.md",
    use_code_interpreter=True
)
```

### 2. Research Agency

```python
# Create specialized agents
lead_researcher = ResearchAgent(
    name="Lead Researcher",
    description="Research coordination and synthesis",
    instructions="lead_researcher_instructions.md"
)

data_analyst = DataAnalyst(
    name="Data Analyst",
    description="Data analysis and visualization",
    instructions="analyst_instructions.md"
)

report_writer = ResearchAgent(
    name="Report Writer",
    description="Research documentation and reporting",
    instructions="writer_instructions.md"
)

# Create research agency
research_agency = Agency([
    lead_researcher,  # Entry point
    [lead_researcher, data_analyst],
    [lead_researcher, report_writer],
    [data_analyst, report_writer]
],
    shared_instructions="research_manifesto.md",
    use_rag=True
)
```

### 3. Data Processing Agency

```python
# Create specialized agents
data_engineer = DataAgent(
    name="Data Engineer",
    description="Data pipeline and processing",
    instructions="engineer_instructions.md"
)

data_analyst = DataAnalyst(
    name="Data Analyst",
    description="Data analysis and insights",
    instructions="analyst_instructions.md"
)

visualization_expert = DataAgent(
    name="Visualization Expert",
    description="Data visualization and reporting",
    instructions="viz_instructions.md"
)

# Create data agency
data_agency = Agency([
    data_engineer,  # Entry point
    [data_engineer, data_analyst],
    [data_engineer, visualization_expert],
    [data_analyst, visualization_expert]
],
    shared_instructions="data_agency_manifesto.md",
    use_file_storage=True
)
```

## Best Practices

1. **Agency Design**
   - Clear communication flows
   - Appropriate agent roles
   - Efficient resource sharing
   - Proper error handling

2. **Resource Management**
   - Enable RAG for knowledge-intensive tasks
   - Use file storage for data handling
   - Implement proper state management
   - Monitor resource usage

3. **Performance Optimization**
   - Optimize message routing
   - Use appropriate batch sizes
   - Monitor response times
   - Cache frequently used data

## Error Handling

```python
from multi_swarm.exceptions import AgencyError

try:
    response = await agency.process_message(message)
except AgencyError as e:
    if "routing_error" in str(e):
        # Handle routing error
        await handle_routing_error(e)
    elif "resource_error" in str(e):
        # Handle resource error
        await handle_resource_error(e)
    else:
        # Handle other agency errors
        raise
```

## Learn More

- [Creating Agents](creating-agents.md)
- [Creating Tools](creating-tools.md)
- [Communication Flows](communication-flows.md) 