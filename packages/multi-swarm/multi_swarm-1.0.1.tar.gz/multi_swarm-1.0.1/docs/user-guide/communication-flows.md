# Communication Flows

Multi-Swarm uses a thread-based communication system that enables structured conversations between agents. Each communication flow is directional and managed through conversation threads.

## Basic Communication

```python
from multi_swarm import Agency, Agent

# Create agents
dev = DevAgent()
analyst = DataAnalyst()
researcher = ResearchAgent()

# Define communication flows
agency = Agency([
    dev,  # Entry point for user communication
    [dev, analyst],  # Dev can communicate with Analyst
    [dev, researcher],  # Dev can communicate with Researcher
    [analyst, researcher]  # Analyst can communicate with Researcher
])
```

## Thread Management

Each conversation is managed through a thread:

```python
# Start a new thread
thread = await agency.create_thread("Project Analysis")

# Send message in thread
response = await agency.send_message(
    thread_id=thread.id,
    content="Analyze project requirements",
    from_agent=dev,
    to_agent=analyst
)

# Continue conversation
follow_up = await agency.send_message(
    thread_id=thread.id,
    content="Provide more details about X",
    from_agent=analyst,
    to_agent=dev
)
```

## Message Structure

Messages contain metadata and content:

```python
class Message:
    thread_id: str  # Unique thread identifier
    content: str    # Message content
    metadata: dict  # Additional information
    from_agent: str # Sender agent name
    to_agent: str   # Recipient agent name
    timestamp: float # Message timestamp
```

## Communication Patterns

### 1. Hierarchical

```python
# Manager delegates to team
lead = DevAgent(name="Tech Lead")
dev1 = DevAgent(name="Developer 1")
dev2 = DevAgent(name="Developer 2")

agency = Agency([
    lead,  # Entry point
    [lead, dev1],  # Lead delegates to dev1
    [lead, dev2],  # Lead delegates to dev2
])
```

### 2. Pipeline

```python
# Sequential processing
collector = DataAgent(name="Data Collector")
processor = DataAgent(name="Data Processor")
analyzer = DataAnalyst(name="Data Analyzer")

agency = Agency([
    collector,  # Entry point
    [collector, processor],  # Collect -> Process
    [processor, analyzer],   # Process -> Analyze
])
```

### 3. Mesh

```python
# Full team collaboration
team_lead = DevAgent(name="Team Lead")
frontend = DevAgent(name="Frontend Dev")
backend = DevAgent(name="Backend Dev")
designer = DevAgent(name="Designer")

agency = Agency([
    team_lead,  # Entry point
    [team_lead, frontend],
    [team_lead, backend],
    [team_lead, designer],
    [frontend, backend],
    [frontend, designer],
    [backend, designer]
])
```

## Advanced Features

### 1. Message Broadcasting

```python
# Send message to multiple agents
await agency.broadcast_message(
    thread_id=thread.id,
    content="Team update: New requirements",
    from_agent=team_lead,
    to_agents=[frontend, backend, designer]
)
```

### 2. Thread Management

```python
# Thread operations
threads = await agency.list_threads()
thread = await agency.get_thread(thread_id)
messages = await agency.get_thread_messages(thread_id)
await agency.archive_thread(thread_id)
```

### 3. Message Filtering

```python
# Get filtered messages
messages = await agency.get_messages(
    thread_id=thread.id,
    filter={
        "from_agent": "dev_lead",
        "type": "code_review",
        "priority": "high"
    }
)
```

## Best Practices

1. **Thread Management**
   - Create meaningful thread names
   - Archive completed threads
   - Monitor thread lifecycle
   - Clean up old threads

2. **Message Structure**
   - Clear, focused messages
   - Appropriate metadata
   - Proper error handling
   - Message validation

3. **Flow Design**
   - Efficient routing
   - Clear responsibilities
   - Proper error handling
   - Resource management

## Error Handling

```python
from multi_swarm.exceptions import CommunicationError

try:
    response = await agency.send_message(
        thread_id=thread.id,
        content="Process this data",
        from_agent=collector,
        to_agent=processor
    )
except CommunicationError as e:
    if "routing_error" in str(e):
        # Handle routing error
        await handle_routing_error(e)
    elif "thread_error" in str(e):
        # Handle thread error
        await handle_thread_error(e)
    else:
        # Handle other communication errors
        raise
```

## Example Workflows

### 1. Code Review Process

```python
# Create code review thread
review_thread = await agency.create_thread("Code Review")

# Developer submits code
await agency.send_message(
    thread_id=review_thread.id,
    content="Please review this PR",
    from_agent=developer,
    to_agent=reviewer
)

# Reviewer provides feedback
await agency.send_message(
    thread_id=review_thread.id,
    content="Found issues in module X",
    from_agent=reviewer,
    to_agent=developer
)

# Developer addresses feedback
await agency.send_message(
    thread_id=review_thread.id,
    content="Fixed issues in module X",
    from_agent=developer,
    to_agent=reviewer
)
```

### 2. Data Analysis Pipeline

```python
# Create analysis thread
analysis_thread = await agency.create_thread("Data Analysis")

# Collect data
await agency.send_message(
    thread_id=analysis_thread.id,
    content="Collect sales data",
    from_agent=manager,
    to_agent=collector
)

# Process data
await agency.send_message(
    thread_id=analysis_thread.id,
    content="Clean and transform data",
    from_agent=collector,
    to_agent=processor
)

# Analyze results
await agency.send_message(
    thread_id=analysis_thread.id,
    content="Generate insights",
    from_agent=processor,
    to_agent=analyst
)
```

### 3. Research Collaboration

```python
# Create research thread
research_thread = await agency.create_thread("Market Research")

# Assign research tasks
await agency.broadcast_message(
    thread_id=research_thread.id,
    content="Research assigned areas",
    from_agent=lead_researcher,
    to_agents=[researcher1, researcher2]
)

# Collect findings
findings = []
for researcher in [researcher1, researcher2]:
    response = await agency.send_message(
        thread_id=research_thread.id,
        content="Submit research findings",
        from_agent=researcher,
        to_agent=lead_researcher
    )
    findings.append(response)

# Synthesize results
await agency.send_message(
    thread_id=research_thread.id,
    content="Synthesize findings",
    from_agent=lead_researcher,
    to_agent=report_writer
)
```

## Learn More

- [Creating Agents](creating-agents.md)
- [Creating Agencies](creating-agencies.md)
- [Advanced Features](advanced-features.md) 