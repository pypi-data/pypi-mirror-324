import os
import google.generativeai as genai
from anthropic import Anthropic
from typing import Optional, Dict, Any

class BaseAgent:
    def __init__(
        self,
        name: str,
        description: str,
        instructions: str,
        tools_folder: str,
        model: str,
        temperature: float = 0.7,
    ):
        # Validate temperature
        if not isinstance(temperature, (int, float)) or not 0 <= temperature <= 1:
            raise ValueError(f"Temperature must be between 0 and 1, got {temperature}")

        self.name = name
        self.description = description
        self.instructions = self._load_instructions(instructions)
        self.tools = self._load_tools(tools_folder)
        self.model = model
        self.temperature = temperature
        
        # Initialize LLM clients
        if "claude" in model.lower():
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY environment variable is not set")
            self.client = Anthropic(api_key=api_key)
        elif "gemini" in model.lower():
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY environment variable is not set")
            genai.configure(api_key=api_key)
            self.client = genai
        else:
            raise ValueError(f"Unsupported model: {model}")
    
    def _load_instructions(self, instructions_path: str) -> str:
        """Load agent instructions from file."""
        if not os.path.exists(instructions_path):
            return ""
        with open(instructions_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _load_tools(self, tools_folder: str) -> Dict[str, Any]:
        """Load tools from the tools folder."""
        tools = {}
        if not os.path.exists(tools_folder):
            return tools
            
        # Import all python files from tools folder
        for file in os.listdir(tools_folder):
            if file.endswith('.py') and not file.startswith('__'):
                module_name = file[:-3]
                module_path = os.path.join(tools_folder, file)
                
                # TODO: Implement tool loading logic
                
        return tools
    
    async def generate_response(self, message: str) -> str:
        """Generate a response using the appropriate LLM."""
        if "claude" in self.model.lower():
            response = await self._generate_claude_response(message)
        elif "gemini" in self.model.lower():
            response = await self._generate_gemini_response(message)
        else:
            raise ValueError(f"Unsupported model: {self.model}")
        return response
    
    async def _generate_claude_response(self, message: str) -> str:
        """Generate a response using Claude."""
        message = self.instructions + "\n\nUser: " + message
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            temperature=self.temperature,
            messages=[{"role": "user", "content": message}]
        )
        return response.content[0].text
    
    async def _generate_gemini_response(self, message: str) -> str:
        """Generate a response using Gemini."""
        message = self.instructions + "\n\nUser: " + message
        model = self.client.GenerativeModel(self.model)
        response = await model.generate_content_async(message)
        return response.text 