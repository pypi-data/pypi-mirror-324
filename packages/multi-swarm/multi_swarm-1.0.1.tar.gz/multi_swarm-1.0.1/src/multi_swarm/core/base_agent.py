import os
import google.generativeai as genai
from anthropic import Anthropic
from typing import Optional, Dict, Any, List
from pathlib import Path
from datetime import datetime
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from .thread import Thread, ThreadManager, Message
from .file import FileManager
from .interpreter import CodeInterpreter
from .rag import RAGSystem

# Load environment variables
load_dotenv()

class AgentConfig(BaseModel):
    """
    Configuration for an agent.
    
    Attributes:
        name: Name of the agent
        description: Description of the agent's role
        instructions_path: Path to the agent's instructions file
        tools_folder: Path to the agent's tools folder
        llm_provider: LLM provider to use
        provider_config: Provider-specific configuration
        temperature: Temperature for LLM sampling
        max_prompt_tokens: Maximum tokens in conversation history
        storage_path: Path for persistent storage
        use_code_interpreter: Whether to enable code interpreter
        use_rag: Whether to enable RAG capabilities
        use_file_storage: Whether to enable file storage
    """
    name: str
    description: str
    instructions_path: str
    tools_folder: str
    llm_provider: str = "claude"
    provider_config: Dict = Field(default_factory=dict)
    temperature: float = 0.7
    max_prompt_tokens: int = 4096
    storage_path: Optional[str] = None
    use_code_interpreter: bool = False
    use_rag: bool = False
    use_file_storage: bool = False

class Agent:
    """
    Base class for all agents in the Multi-Swarm framework.
    
    This class provides core functionality for agents, including:
    - Thread management for conversations
    - File storage and retrieval
    - Code execution in a secure environment
    - RAG capabilities for knowledge retrieval
    - Tool management and execution
    - Automatic LLM provider selection
    """
    
    # Latest model configurations
    CLAUDE_CONFIG = {
        "model": "claude-3-5-sonnet-latest",
        "max_tokens": 4096,
        "api_version": "2024-03"
    }
    
    GEMINI_CONFIG = {
        "model": "gemini-2.0-flash-exp",
        "max_tokens": 4096,
        "api_version": "2024-01"
    }
    
    # Task categories and their preferred providers
    TASK_PREFERENCES = {
        "code": "claude",  # Code generation and review
        "research": "claude",  # Research and analysis
        "planning": "claude",  # Strategic planning
        "documentation": "claude",  # Documentation generation
        "data": "gemini",  # Data processing and analysis
        "integration": "gemini",  # API and system integration
        "operations": "gemini",  # System operations
        "monitoring": "gemini"  # System monitoring
    }
    
    def __init__(
        self,
        name: str,
        description: str,
        instructions: str,
        tools_folder: str,
        llm_provider: Optional[str] = None,
        provider_config: Optional[Dict[str, Any]] = None,
        temperature: float = 0.7,
        storage_path: Optional[str] = None,
        use_file_storage: bool = False,
        use_rag: bool = False,
        use_code_interpreter: bool = False
    ):
        self.name = name
        self.description = description
        self.instructions = self._load_instructions(instructions)
        self.tools_folder = tools_folder
        self.temperature = temperature
        
        # Initialize storage and features
        self.storage_path = storage_path or "./storage"
        self.use_file_storage = use_file_storage
        self.use_rag = use_rag
        self.use_code_interpreter = use_code_interpreter
        
        # Set up LLM provider
        self.llm_provider = llm_provider or self._determine_provider()
        self.provider_config = self._get_provider_config(provider_config)
        
        # Load tools
        self.tools = self._load_tools()
        
        # Validate environment
        self._validate_environment()
    
    def _determine_provider(self) -> str:
        """Automatically determine the best LLM provider based on agent description."""
        description_lower = self.description.lower()
        
        # Check description against task preferences
        for task, provider in self.TASK_PREFERENCES.items():
            if task in description_lower:
                return provider
        
        # Default to Claude for complex/unknown tasks
        return "claude"
    
    def _get_provider_config(self, custom_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get the configuration for the selected LLM provider."""
        if self.llm_provider == "claude":
            base_config = self.CLAUDE_CONFIG.copy()
        else:
            base_config = self.GEMINI_CONFIG.copy()
        
        if custom_config:
            base_config.update(custom_config)
        
        return base_config
    
    def _validate_environment(self):
        """Validate that necessary environment variables are set."""
        if self.llm_provider == "claude" and not os.getenv("ANTHROPIC_API_KEY"):
            raise ValueError("ANTHROPIC_API_KEY environment variable is required for Claude")
        elif self.llm_provider == "gemini" and not os.getenv("GOOGLE_API_KEY"):
            raise ValueError("GOOGLE_API_KEY environment variable is required for Gemini")
    
    def _load_instructions(self, instructions_path: str) -> str:
        """Load agent instructions from file."""
        path = Path(instructions_path)
        if not path.exists():
            raise FileNotFoundError(f"Instructions file not found: {instructions_path}")
        
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _load_tools(self) -> List[Any]:
        """Load tools from the tools folder."""
        tools = []
        tools_path = Path(self.tools_folder)
        
        if tools_path.exists() and tools_path.is_dir():
            # Load tools implementation here
            pass
        
        return tools
    
    async def generate_response(self, message: str) -> str:
        """Generate a response using the configured LLM provider."""
        # Implementation will vary based on provider
        if self.llm_provider == "claude":
            return await self._generate_claude_response(message)
        else:
            return await self._generate_gemini_response(message)
    
    async def _generate_claude_response(self, message: str) -> str:
        """Generate a response using Claude."""
        # Claude-specific implementation
        pass
    
    async def _generate_gemini_response(self, message: str) -> str:
        """Generate a response using Gemini."""
        # Gemini-specific implementation
        pass
    
    def _init_components(self):
        """Initialize agent components based on configuration."""
        # Initialize thread manager
        thread_storage = self.storage_path / "threads" if self.storage_path else None
        self.thread_manager = ThreadManager(storage_path=thread_storage)
        
        # Initialize file manager if enabled
        self.file_manager = None
        if self.use_file_storage:
            file_storage = self.storage_path / "files" if self.storage_path else None
            self.file_manager = FileManager(storage_path=file_storage)
        
        # Initialize code interpreter if enabled
        self.code_interpreter = None
        if self.use_code_interpreter:
            interpreter_workspace = self.storage_path / "workspace" if self.storage_path else None
            self.code_interpreter = CodeInterpreter(workspace_dir=interpreter_workspace)
        
        # Initialize RAG system if enabled
        self.rag_system = None
        if self.use_rag:
            rag_storage = self.storage_path / "rag" if self.storage_path else None
            self.rag_system = RAGSystem(storage_path=rag_storage)
    
    def create_thread(self, metadata: Dict = None) -> Thread:
        """Create a new conversation thread."""
        return self.thread_manager.create_thread(metadata)
    
    def get_thread(self, thread_id: str) -> Optional[Thread]:
        """Get a thread by ID."""
        return self.thread_manager.get_thread(thread_id)
    
    def process_message(
        self,
        thread_id: str,
        content: str,
        role: str = "user",
        metadata: Dict = None
    ) -> Message:
        """
        Process a message in a thread.
        
        Args:
            thread_id: ID of the thread
            content: Message content
            role: Role of the message sender
            metadata: Additional metadata
            
        Returns:
            The created Message instance
        """
        thread = self.get_thread(thread_id)
        if not thread:
            raise ValueError(f"Thread {thread_id} not found")
            
        # Add message to thread
        message = thread.add_message(
            role=role,
            content=content,
            agent_name=self.name,
            metadata=metadata
        )
        
        # Process message using LLM
        response = self._process_with_llm(thread)
        
        # Add response to thread
        thread.add_message(
            role="assistant",
            content=response,
            agent_name=self.name
        )
        
        return message
    
    def _process_with_llm(self, thread: Thread) -> str:
        """
        Process a thread with the LLM provider.
        
        This method should be implemented by specific provider implementations.
        """
        raise NotImplementedError
    
    def upload_file(
        self,
        file: Any,
        filename: str,
        purpose: str = "attachment",
        metadata: Dict = None
    ):
        """Upload a file to storage."""
        if not self.file_manager:
            raise RuntimeError("File storage not enabled for this agent")
        return self.file_manager.upload_file(file, filename, purpose, metadata)
    
    def execute_code(
        self,
        code: str,
        language: str = "python",
        additional_files: Dict[str, str] = None,
        environment: Dict[str, str] = None
    ):
        """Execute code in the secure environment."""
        if not self.code_interpreter:
            raise RuntimeError("Code interpreter not enabled for this agent")
        return self.code_interpreter.execute(code, language, additional_files, environment)
    
    def search_knowledge(
        self,
        query: str,
        k: int = 5,
        threshold: float = None
    ):
        """Search the knowledge base using RAG."""
        if not self.rag_system:
            raise RuntimeError("RAG not enabled for this agent")
        return self.rag_system.search(query, k, threshold)
    
    def add_to_knowledge(
        self,
        content: str,
        metadata: Dict = None
    ):
        """Add content to the knowledge base."""
        if not self.rag_system:
            raise RuntimeError("RAG not enabled for this agent")
        return self.rag_system.add_document(content, metadata)
    
    def get_tool(self, tool_name: str) -> Optional[Any]:
        """Get a tool by name."""
        return self.tools.get(tool_name)
    
    def list_tools(self) -> List[str]:
        """List available tools."""
        return list(self.tools.keys())
    
    def save_state(self):
        """Save agent state to storage."""
        if not self.storage_path:
            return
            
        self.thread_manager.save_all_threads()
        if self.file_manager:
            self.file_manager._save_index()
        if self.rag_system:
            self.rag_system._save_state()
    
    def load_state(self):
        """Load agent state from storage."""
        if not self.storage_path:
            return
            
        self.thread_manager.load_all_threads()
        if self.file_manager:
            self.file_manager._load_index()
        if self.rag_system:
            self.rag_system._load_state() 