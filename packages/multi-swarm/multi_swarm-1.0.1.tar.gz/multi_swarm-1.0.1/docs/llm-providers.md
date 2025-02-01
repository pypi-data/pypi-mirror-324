# LLM Provider Configuration Guide

## Overview

Multi-Swarm supports multiple Language Model (LLM) providers to offer the best capabilities for different types of tasks. The framework automatically selects the most appropriate provider based on the agent's role and task requirements.

## Supported Models

### Claude (Anthropic)
```python
CLAUDE_CONFIG = {
    "model": "claude-3-5-sonnet-latest",
    "max_tokens": 4096,
    "api_version": "2024-03"
}
```

#### Best For
- Complex reasoning and analysis
- Code generation and review
- Technical documentation
- Research and planning
- Long-form content generation
- Multi-step problem solving

#### Configuration Options
- `model`: Currently supports `claude-3-5-sonnet-latest`
- `max_tokens`: Maximum tokens in the response (default: 4096)
- `api_version`: API version to use (default: "2024-03")
- `temperature`: Controls randomness (0.0 to 1.0, default: 0.7)

### Gemini (Google)
```python
GEMINI_CONFIG = {
    "model": "gemini-2.0-flash-exp",
    "max_tokens": 4096,
    "api_version": "2024-01"
}
```

#### Best For
- Quick responses and real-time interactions
- Data processing and analysis
- API integration tasks
- System operations
- Monitoring and alerting
- Pattern recognition

#### Configuration Options
- `model`: Currently supports `gemini-2.0-flash-exp`
- `max_tokens`: Maximum tokens in the response (default: 4096)
- `api_version`: API version to use (default: "2024-01")
- `temperature`: Controls randomness (0.0 to 1.0, default: 0.7)

## Automatic Model Selection

The framework uses a task-based approach to automatically select the most appropriate model:

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

### Selection Process
1. The framework analyzes the agent's description
2. Matches keywords with task preferences
3. Selects the most appropriate provider
4. Falls back to Claude for complex/unknown tasks

## Manual Configuration

You can override the automatic selection by specifying the provider and configuration:

```python
class MyAgent(Agent):
    def __init__(self):
        super().__init__(
            name="MyAgent",
            description="Custom agent for specific tasks",
            instructions="path/to/instructions.md",
            tools_folder="path/to/tools",
            llm_provider="claude",  # Manually specify provider
            provider_config={
                "model": "claude-3-5-sonnet-latest",
                "max_tokens": 4096,
                "api_version": "2024-03",
                "temperature": 0.7
            }
        )
```

## Environment Setup

Required environment variables:
```bash
# For Claude
ANTHROPIC_API_KEY=your_claude_api_key

# For Gemini
GOOGLE_API_KEY=your_gemini_api_key
```

## Best Practices

1. **Task-Based Selection**
   - Let the framework choose the provider based on task type
   - Override only when necessary for specific requirements

2. **Cost Optimization**
   - Use Gemini for simple, quick tasks
   - Reserve Claude for complex reasoning tasks

3. **Performance Tuning**
   - Adjust temperature based on task requirements
   - Set appropriate max_tokens for expected response length

4. **Error Handling**
   - Always handle potential API errors
   - Implement fallback strategies for critical tasks

5. **Version Management**
   - Keep track of API versions
   - Test with new model versions before updating

## Monitoring and Metrics

The framework tracks:
- Request success/failure rates
- Response latency
- Token usage
- Cost per request
- Rate limit status

Access metrics through the agent's monitoring interface:
```python
metrics = agent.get_provider_metrics()
``` 