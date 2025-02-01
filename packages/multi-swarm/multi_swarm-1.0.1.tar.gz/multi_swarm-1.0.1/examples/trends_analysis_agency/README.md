# Google Trends Analysis Agency Example

This is an example implementation showing how to use the Multi-Swarm framework to create a specialized agency for Google Trends analysis.

## Overview

This example demonstrates:
- How to create custom agents (CEO and TrendsAnalyst)
- How to set up communication flows between agents
- How to structure agent instructions and tools
- Basic agency configuration and setup

## ⚠️ Note

This is a template/example implementation meant to demonstrate the framework's capabilities. The agents do not have actual Google Trends functionality implemented. In a real implementation, you would need to:

1. Add proper Google Trends API integration using `pytrends`
2. Implement data analysis tools
3. Add visualization capabilities
4. Handle API rate limiting and errors

## Structure

```
trends_analysis_agency/
├── agents/
│   ├── ceo/
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   ├── instructions.md
│   │   └── tools/
│   └── trends_analyst/
│       ├── __init__.py
│       ├── agent.py
│       ├── instructions.md
│       └── tools/
├── README.md
└── main.py
```

## Usage

```python
from trends_analysis_agency.agents.ceo import CEOAgent
from trends_analysis_agency.agents.trends_analyst import TrendsAnalyst
from multi_swarm import Agency

def create_agency():
    # Initialize agents
    ceo = CEOAgent()
    analyst = TrendsAnalyst()

    # Create agency with communication flows
    agency = Agency(
        agents=[
            ceo,  # Entry point for user communication
            [ceo, analyst],  # CEO can communicate with analyst
        ],
        shared_instructions="agency_manifesto.md"
    )
    
    return agency

if __name__ == "__main__":
    agency = create_agency()
    agency.run_demo()
```

## Extending This Example

To turn this into a functional implementation:

1. Add Google Trends API integration:
```python
from pytrends.request import TrendReq

class TrendsAnalysisTool(BaseTool):
    query: str
    timeframe: str
    geo: str = "US"

    def run(self):
        pytrends = TrendReq()
        pytrends.build_payload([self.query], timeframe=self.timeframe, geo=self.geo)
        return pytrends.interest_over_time()
```

2. Add data visualization tools
3. Implement proper error handling
4. Add rate limiting and caching 