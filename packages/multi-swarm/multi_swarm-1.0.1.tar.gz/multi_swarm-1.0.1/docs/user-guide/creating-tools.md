# Creating Tools

Tools are the specific actions that agents can perform. Each tool is defined using Pydantic for input validation and clear interfaces.

## Basic Tool Structure

```python
from multi_swarm.tools import BaseTool
from pydantic import Field
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

class DataVisualizationTool(BaseTool):
    """
    Create data visualizations using various plotting libraries.
    Supports multiple chart types and customization options.
    """
    data_path: str = Field(
        ..., description="Path to the data file to visualize"
    )
    chart_type: str = Field(
        ..., description="Type of chart to create (line, bar, scatter, etc.)"
    )
    title: str = Field(
        default="", description="Title for the visualization"
    )

    def run(self):
        """Execute the visualization logic."""
        # Implementation using plotting libraries
        return f"Created {self.chart_type} chart from {self.data_path}"
```

## Tool Components

1. **Class Definition**
   - Inherit from `BaseTool`
   - Clear docstring explaining purpose
   - Input validation with Pydantic

2. **Fields**
   - Use Pydantic's `Field` for validation
   - Clear descriptions for each field
   - Appropriate default values

3. **Run Method**
   - Main execution logic
   - Return results as string
   - Handle errors appropriately

## Best Practices

### 1. Environment Variables

```python
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")

class APITool(BaseTool):
    endpoint: str = Field(..., description="API endpoint to call")
    
    def run(self):
        """Make API call using environment variables."""
        # Use API_KEY and BASE_URL from environment
        return "API response"
```

### 2. Error Handling

```python
from multi_swarm.exceptions import ToolError

class RiskySQLTool(BaseTool):
    query: str = Field(..., description="SQL query to execute")
    
    def run(self):
        """Execute SQL query with error handling."""
        try:
            # Execute query
            return "Query results"
        except Exception as e:
            raise ToolError(f"SQL execution failed: {str(e)}")
```

### 3. Resource Management

```python
class FileProcessingTool(BaseTool):
    file_path: str = Field(..., description="Path to file to process")
    
    def run(self):
        """Process file with proper resource management."""
        try:
            with open(self.file_path, 'r') as f:
                # Process file
                return "Processing results"
        finally:
            # Cleanup if needed
            pass
```

## Advanced Features

### 1. Async Support

```python
class AsyncAPITool(BaseTool):
    endpoint: str = Field(..., description="API endpoint")
    
    async def run(self):
        """Asynchronous API call."""
        async with aiohttp.ClientSession() as session:
            async with session.get(self.endpoint) as response:
                return await response.text()
```

### 2. Progress Tracking

```python
class LongRunningTool(BaseTool):
    steps: int = Field(..., description="Number of steps")
    
    def run(self):
        """Execute with progress updates."""
        for i in range(self.steps):
            self.update_progress(i / self.steps)
            # Do work
        return "Task completed"
```

### 3. File Storage Integration

```python
class DataStorageTool(BaseTool):
    data: str = Field(..., description="Data to store")
    
    def run(self):
        """Store data with file system integration."""
        storage = self.get_file_storage()
        path = storage.save_file("data.txt", self.data)
        return f"Data stored at {path}"
```

## Example Tools

### 1. API Integration

```python
class OpenAITool(BaseTool):
    """
    Interact with OpenAI's API for specific tasks.
    """
    prompt: str = Field(..., description="Prompt for the API")
    model: str = Field(default="gpt-4", description="Model to use")
    
    def run(self):
        """Execute OpenAI API call."""
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": self.prompt}]
        )
        return response.choices[0].message.content
```

### 2. Data Processing

```python
class DataFrameTool(BaseTool):
    """
    Process data using pandas DataFrame operations.
    """
    csv_path: str = Field(..., description="Path to CSV file")
    operation: str = Field(..., description="Operation to perform")
    
    def run(self):
        """Execute DataFrame operation."""
        import pandas as pd
        df = pd.read_csv(self.csv_path)
        
        if self.operation == "summary":
            return df.describe().to_string()
        elif self.operation == "head":
            return df.head().to_string()
        else:
            raise ToolError(f"Unknown operation: {self.operation}")
```

### 3. File Operations

```python
class FileAnalyzerTool(BaseTool):
    """
    Analyze file contents and structure.
    """
    file_path: str = Field(..., description="Path to file")
    analysis_type: str = Field(..., description="Type of analysis")
    
    def run(self):
        """Perform file analysis."""
        if not os.path.exists(self.file_path):
            raise ToolError(f"File not found: {self.file_path}")
            
        stats = os.stat(self.file_path)
        return {
            "size": stats.st_size,
            "created": stats.st_ctime,
            "modified": stats.st_mtime
        }
```

## Testing Tools

```python
if __name__ == "__main__":
    # Test visualization tool
    viz_tool = DataVisualizationTool(
        data_path="data.csv",
        chart_type="line",
        title="Test Chart"
    )
    print(viz_tool.run())
    
    # Test API tool
    api_tool = OpenAITool(
        prompt="Hello, world!",
        model="gpt-4"
    )
    print(api_tool.run())
```

## Learn More

- [Creating Agents](creating-agents.md)
- [Communication Flows](communication-flows.md)
- [API Reference](../api/tools.md) 