# Gemini Integration

Multi-Swarm integrates Google's Gemini models, particularly suited for data processing, system operations, and real-time tasks.

## Model Configuration

```python
GEMINI_CONFIG = {
    "model": "gemini-2.0-flash-exp",
    "max_tokens": 4096,
    "api_version": "2024-01"
}
```

## Task Preferences

Gemini is automatically selected for the following task types:
- Data processing and analysis
- API integration tasks
- System operations
- Monitoring and alerting
- Real-time interactions
- Pattern recognition

## Usage

### Basic Implementation

```python
from multi_swarm import Agent

class DataProcessor(Agent):
    def __init__(self):
        super().__init__(
            name="Data Processor",
            description="Data processing and system operations specialist",
            instructions="processor_instructions.md",
            tools_folder="./tools",
            # Framework will automatically select Gemini based on description
            temperature=0.5,
            use_rag=True  # Enable knowledge base
        )
```

### Manual Configuration

```python
class CustomAgent(Agent):
    def __init__(self):
        super().__init__(
            name="Custom Agent",
            description="Specialized data tasks",
            instructions="instructions.md",
            tools_folder="./tools",
            llm_provider="gemini",  # Manually specify Gemini
            provider_config={
                "model": "gemini-2.0-flash-exp",
                "max_tokens": 4096,
                "api_version": "2024-01",
                "temperature": 0.5
            }
        )
```

## Best Practices

1. **Task Description**
   - Include relevant keywords in agent description
   - Let framework handle model selection
   - Focus on data and system operations

2. **Temperature Settings**
   - 0.3-0.5: Data analysis, system tasks
   - 0.5-0.7: General operations
   - 0.7-0.9: Creative data presentation

3. **Resource Management**
   - Enable RAG for data-intensive tasks
   - Use file storage for data handling
   - Implement proper error handling

4. **Performance Tuning**
   - Optimize prompt length
   - Use appropriate batch sizes
   - Monitor response times

## Error Handling

```python
from multi_swarm.exceptions import ProviderError

try:
    response = await agent.process_message(message)
except ProviderError as e:
    if "rate_limit" in str(e):
        # Handle rate limiting
        await asyncio.sleep(30)
        response = await agent.process_message(message)
    elif "quota_exceeded" in str(e):
        # Handle quota issues
        await handle_quota_exceeded()
        response = await agent.process_message(message)
    else:
        # Handle other provider errors
        raise
```

## Environment Setup

1. Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

2. Set the environment variable:
```bash
export GOOGLE_API_KEY=your_api_key
```

3. Or add to your `.env` file:
```env
GOOGLE_API_KEY=your_api_key
```

## Performance Optimization

1. **Request Management**
   - Use appropriate batch sizes
   - Implement request queuing
   - Monitor API quotas

2. **Response Handling**
   - Process responses asynchronously
   - Implement proper error handling
   - Use streaming for long responses

3. **Resource Usage**
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
print(f"Total requests: {metrics['total_requests']}")
print(f"Average latency: {metrics['avg_latency']}ms")
```

## Data Processing Features

1. **Batch Processing**
   ```python
   # Process data in batches
   async def process_data_batch(data_batch):
       tasks = [agent.process_message(item) for item in data_batch]
       return await asyncio.gather(*tasks)
   ```

2. **Real-time Processing**
   ```python
   # Handle real-time data
   async def process_stream(data_stream):
       async for data in data_stream:
           result = await agent.process_message(data)
           await handle_result(result)
   ```

## Learn More

- [Gemini Documentation](https://ai.google.dev/docs)
- [Multi-Swarm Examples](../examples/trends-agency.md)
- [Advanced Configuration](../user-guide/creating-agents.md) 