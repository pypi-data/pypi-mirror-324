# Claude Integration

Multi-Swarm provides seamless integration with Anthropic's Claude models, particularly suited for complex reasoning, code generation, and technical analysis.

## Model Configuration

```python
CLAUDE_CONFIG = {
    "model": "claude-3-5-sonnet-latest",
    "max_tokens": 4096,
    "api_version": "2024-03"
}
```

## Task Preferences

Claude is automatically selected for the following task types:
- Code generation and review
- Research and analysis
- Strategic planning
- Technical documentation
- Complex reasoning
- Multi-step problem solving

## Usage

### Basic Implementation

```python
from multi_swarm import Agent

class TechnicalAgent(Agent):
    def __init__(self):
        super().__init__(
            name="Technical Expert",
            description="Code generation and technical analysis specialist",
            instructions="technical_instructions.md",
            tools_folder="./tools",
            # Framework will automatically select Claude based on description
            temperature=0.5,  # Lower temperature for technical tasks
            use_code_interpreter=True  # Enable code execution
        )
```

### Manual Configuration

```python
class CustomAgent(Agent):
    def __init__(self):
        super().__init__(
            name="Custom Agent",
            description="Specialized technical tasks",
            instructions="instructions.md",
            tools_folder="./tools",
            llm_provider="claude",  # Manually specify Claude
            provider_config={
                "model": "claude-3-5-sonnet-latest",
                "max_tokens": 4096,
                "api_version": "2024-03",
                "temperature": 0.5
            }
        )
```

## Best Practices

1. **Task Description**
   - Include relevant keywords in agent description
   - Let framework handle model selection
   - Be specific about technical requirements

2. **Temperature Settings**
   - 0.3-0.5: Code generation, technical analysis
   - 0.5-0.7: Technical writing, documentation
   - 0.7-0.9: Creative technical tasks

3. **Context Management**
   - Provide clear, structured instructions
   - Include relevant technical context
   - Use code blocks for examples

4. **Resource Management**
   - Enable code interpreter for technical tasks
   - Use RAG for knowledge-intensive tasks
   - Implement proper error handling

## Error Handling

```python
from multi_swarm.exceptions import ProviderError

try:
    response = await agent.process_message(message)
except ProviderError as e:
    if "rate_limit" in str(e):
        # Handle rate limiting
        await asyncio.sleep(60)
        response = await agent.process_message(message)
    elif "context_length" in str(e):
        # Handle context length error
        shortened = summarize_message(message)
        response = await agent.process_message(shortened)
    else:
        # Handle other provider errors
        raise
```

## Environment Setup

1. Get your API key from [Anthropic's Console](https://console.anthropic.com/)

2. Set the environment variable:
```bash
export ANTHROPIC_API_KEY=your_api_key
```

3. Or add to your `.env` file:
```env
ANTHROPIC_API_KEY=your_api_key
```

## Performance Optimization

1. **Token Management**
   - Use concise, focused prompts
   - Implement response caching
   - Monitor token usage

2. **Cost Optimization**
   - Use appropriate temperature settings
   - Enable streaming for long responses
   - Implement request batching

3. **Response Handling**
   ```python
   # Enable streaming for long responses
   async for chunk in agent.stream_message(message):
       process_chunk(chunk)
   ```

## Monitoring

The framework provides built-in monitoring for:
- Request success/failure rates
- Response latency
- Token usage
- Cost per request
- Rate limit status

Access metrics:
```python
metrics = agent.get_provider_metrics()
print(f"Total tokens used: {metrics['total_tokens']}")
print(f"Average latency: {metrics['avg_latency']}ms")
```

## Learn More

- [Anthropic Documentation](https://docs.anthropic.com/claude/docs)
- [Multi-Swarm Examples](../examples/dev-agency.md)
- [Advanced Configuration](../user-guide/creating-agents.md) 