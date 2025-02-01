# Installation Guide

Multi-Swarm can be installed directly via pip:

```bash
pip install multi_swarm
```

## Prerequisites

1. **Python Version**
   - Python 3.9 or higher is required
   - Virtual environment recommended

2. **API Keys**
   You'll need API keys for the LLM providers you plan to use:
   
   - For Claude (Anthropic):
     - Get your API key from [Anthropic's Console](https://console.anthropic.com/)
     - Set it as an environment variable:
       ```bash
       export ANTHROPIC_API_KEY=your_api_key
       ```

   - For Gemini (Google):
     - Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
     - Set it as an environment variable:
       ```bash
       export GOOGLE_API_KEY=your_api_key
       ```

## Environment Setup

1. **Create a Virtual Environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Multi-Swarm**
   ```bash
   pip install multi_swarm
   ```

3. **Create a .env File**
   Create a `.env` file in your project root:
   ```env
   ANTHROPIC_API_KEY=your_claude_api_key
   GOOGLE_API_KEY=your_gemini_api_key
   ```

4. **Cursor AI Setup** (recommended)
   If you're using Cursor AI (recommended for development):
   ```bash
   cp .cursorrules /path/to/your/project/root/
   ```
   The `.cursorrules` file contains essential instructions for Cursor's Claude agent to better assist with Multi-Swarm development.

5. **Verify Installation**
   ```python
   from multi_swarm import Agency, Agent
   print("Multi-Swarm installed successfully!")
   ```

## Optional Dependencies

For enhanced functionality, you can install additional packages:

```bash
# For development and testing
pip install multi_swarm[dev]

# For monitoring and visualization
pip install multi_swarm[monitoring]

# For all optional dependencies
pip install multi_swarm[all]
```

## Default Model Configurations

Multi-Swarm uses the latest models from Claude and Gemini:

```python
# Claude Configuration (default)
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

The framework automatically selects the appropriate model based on the agent's role and task requirements.

## Troubleshooting

### Common Issues

1. **API Key Not Found**
   ```python
   ImportError: API key not found. Please set the ANTHROPIC_API_KEY environment variable.
   ```
   Solution: Ensure you've set up your API keys in the `.env` file or environment variables.

2. **Python Version Error**
   ```python
   ImportError: This package requires Python 3.9+
   ```
   Solution: Upgrade your Python installation or use a compatible version.

3. **Package Conflicts**
   If you encounter package conflicts, try creating a fresh virtual environment:
   ```bash
   python -m venv fresh_venv
   source fresh_venv/bin/activate
   pip install multi_swarm
   ```

For more help, check our [GitHub Issues](https://github.com/bartvanspitaels99/multi-swarm/issues) or [Documentation](https://multi-swarm.readthedocs.io/). 