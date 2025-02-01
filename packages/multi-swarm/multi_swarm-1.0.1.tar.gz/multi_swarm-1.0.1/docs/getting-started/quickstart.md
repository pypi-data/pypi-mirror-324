# Quick Start Guide

This guide will help you create your first Multi-Swarm agency in minutes. We'll create a simple agency with two agents that collaborate to analyze data.

## 1. Basic Setup

First, make sure you have Multi-Swarm installed and your API keys configured:

```bash
pip install multi_swarm
```

Create a `.env` file with your API keys:
```env
ANTHROPIC_API_KEY=your_claude_api_key
GOOGLE_API_KEY=your_gemini_api_key
```

If using Cursor AI (recommended):
```bash
cp .cursorrules /path/to/your/project/root/
```

## 2. Create Your First Agency

Create a new file `my_agency.py`:

```python
from multi_swarm import Agency, Agent
from dotenv import load_dotenv

load_dotenv()  # Load API keys

# Create the analyst agent
class DataAnalyst(Agent):
    def __init__(self):
        super().__init__(
            name="Data Analyst",
            description="Expert in data analysis and visualization",
            instructions="analyst_instructions.md",
            tools_folder="./tools",
            # Framework will automatically select between Claude and Gemini
            temperature=0.5,
            use_code_interpreter=True,  # Enable code execution
            use_rag=True  # Enable knowledge base
        )

# Create the reporter agent
class Reporter(Agent):
    def __init__(self):
        super().__init__(
            name="Reporter",
            description="Expert in creating clear reports and visualizations",
            instructions="reporter_instructions.md",
            tools_folder="./tools",
            # Framework will automatically select between Claude and Gemini
            temperature=0.7,  # Higher for creative tasks
            use_file_storage=True  # Enable file storage
        )

# Create and configure the agency
agency = Agency(
    name="Analysis Team",
    description="Data analysis and reporting team",
    agents=[analyst, reporter],
    flows=[
        (analyst.name, reporter.name),  # Analyst can send to reporter
        (reporter.name, analyst.name)   # Reporter can ask analyst questions
    ],
    shared_instructions="agency_manifesto.md",
    use_code_interpreter=True,  # Enable code execution for all agents
    use_file_storage=True      # Enable file storage for all agents
)

# Run the agency
if __name__ == "__main__":
    agency.run_demo()
```

## 3. Create Instructions

Create `analyst_instructions.md`:
```markdown
# Data Analyst Role

Your role is to analyze data and provide insights.

# Goals
1. Process and analyze data accurately
2. Identify key patterns and trends
3. Create clear visualizations
4. Collaborate with the reporter

# Process
1. Receive data for analysis
2. Clean and preprocess data
3. Apply appropriate analytical methods
4. Create visualizations
5. Document findings
6. Share results with reporter
```

Create `reporter_instructions.md`:
```markdown
# Reporter Role

Your role is to create clear, engaging reports.

# Goals
1. Create clear, engaging reports
2. Adapt technical content for the audience
3. Create effective visualizations
4. Maintain clear communication

# Process
1. Receive analysis from analyst
2. Structure information logically
3. Create clear visualizations
4. Present findings in accessible language
5. Format report professionally
```

Create `agency_manifesto.md`:
```markdown
# Analysis Team Agency

Our mission is to transform data into clear, actionable insights.

# Operating Environment
- Collaborative analysis and reporting
- Focus on accuracy and clarity
- Data-driven decision support

# Communication Guidelines
1. Clear and professional communication
2. Regular status updates
3. Constructive feedback
4. Knowledge sharing
```

## 4. Create Tools

Create a tools directory for each agent:
```bash
mkdir -p analyst/tools reporter/tools
```

Example tool for the analyst (`analyst/tools/visualization.py`):
```python
from pydantic import BaseModel, Field
import matplotlib.pyplot as plt
import seaborn as sns

class VisualizationTool(BaseModel):
    """Create data visualizations."""
    data: dict = Field(..., description="Data to visualize")
    chart_type: str = Field(..., description="Type of chart to create")
    title: str = Field(..., description="Chart title")
    
    def run(self):
        # Tool implementation
        plt.figure(figsize=(10, 6))
        if self.chart_type == "line":
            sns.lineplot(data=self.data)
        elif self.chart_type == "bar":
            sns.barplot(data=self.data)
        plt.title(self.title)
        plt.savefig("visualization.png")
        return "Visualization saved as visualization.png"
```

## 5. Run Your Agency

Run your agency:
```bash
python my_agency.py
```

Example interaction:
```
> Analyze this quarterly revenue data and create a report:
  Q1: $1.2M
  Q2: $1.5M
  Q3: $1.8M
  Q4: $2.1M

[Data Analyst]: Analyzing quarterly revenue data...
[Data Analyst]: Creating visualization...
[Data Analyst]: Sending analysis to reporter...
[Reporter]: Creating comprehensive report...
[Reporter]: Report complete! Here are the key findings...
```

## 6. Next Steps

1. **Customize Agents**
   - Add more specialized tools
   - Refine instructions
   - Enable additional features (RAG, file storage)

2. **Enhance Communication**
   - Add more agents to the team
   - Define additional communication flows
   - Create specialized workflows

3. **Add Advanced Features**
   - Implement persistent storage
   - Add knowledge base integration
   - Create custom tools

## Best Practices

1. **Agent Design**
   - Write clear, focused descriptions
   - Let the framework handle model selection
   - Enable only needed features
   - Use appropriate temperature settings

2. **Communication Flows**
   - Define minimal necessary paths
   - Enable bi-directional when needed
   - Document flow purposes
   - Monitor interactions

3. **Resource Management**
   - Use appropriate storage paths
   - Clean up temporary files
   - Handle concurrent access
   - Monitor resource usage

## Learn More

- [Core Concepts](concepts.md)
- [Creating Agents](../user-guide/creating-agents.md)
- [Creating Tools](../user-guide/creating-tools.md)
- [Example Projects](../examples/dev-agency.md) 