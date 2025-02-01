import os
import asyncio
from typing import List, Tuple, Optional, Dict, Union, Any
from pathlib import Path
import json
from datetime import datetime
from pydantic import BaseModel, Field

from multi_swarm.core.base_agent import BaseAgent
from .thread import Thread, ThreadManager, Message
from .file import FileManager
from .interpreter import CodeInterpreter
from .rag import RAGSystem

class AgencyConfig(BaseModel):
    """
    Configuration for an agency.
    
    Attributes:
        name: Name of the agency
        description: Description of the agency's purpose
        storage_path: Path for persistent storage
        shared_instructions: Path to shared instructions file
        default_temperature: Default temperature for agents
        default_max_tokens: Default max tokens for agents
        use_code_interpreter: Whether to enable code interpreter
        use_rag: Whether to enable RAG capabilities
        use_file_storage: Whether to enable file storage
    """
    name: str
    description: str
    storage_path: Optional[str] = None
    shared_instructions: Optional[str] = None
    default_temperature: float = 0.7
    default_max_tokens: int = 4096
    use_code_interpreter: bool = False
    use_rag: bool = False
    use_file_storage: bool = False

class CommunicationFlow(BaseModel):
    """
    Represents a communication flow between agents.
    
    Attributes:
        source: Source agent name
        target: Target agent name
        thread_id: ID of the conversation thread
        metadata: Additional metadata about the flow
    """
    source: str
    target: str
    thread_id: str
    metadata: Dict = Field(default_factory=dict)

class Agency:
    """
    Represents a collection of agents working together.
    
    This class manages:
    - Agent initialization and configuration
    - Inter-agent communication
    - Shared resources (files, knowledge base)
    - Task distribution and coordination
    """
    
    def __init__(
        self,
        name: str,
        description: str,
        agents: List[BaseAgent],
        flows: List[Tuple[str, str]],
        storage_path: Optional[str] = None,
        shared_instructions: Optional[str] = None,
        default_temperature: float = 0.7,
        default_max_tokens: int = 4096,
        use_code_interpreter: bool = False,
        use_rag: bool = False,
        use_file_storage: bool = False
    ):
        """
        Initialize the agency.
        
        Args:
            name: Name of the agency
            description: Description of the agency's purpose
            agents: List of agents in the agency
            flows: List of tuples defining communication flows (source, target)
            storage_path: Path for persistent storage
            shared_instructions: Path to shared instructions file
            default_temperature: Default temperature for agents
            default_max_tokens: Default max tokens for agents
            use_code_interpreter: Whether to enable code interpreter
            use_rag: Whether to enable RAG capabilities
            use_file_storage: Whether to enable file storage
        """
        self.config = AgencyConfig(
            name=name,
            description=description,
            storage_path=storage_path,
            shared_instructions=shared_instructions,
            default_temperature=default_temperature,
            default_max_tokens=default_max_tokens,
            use_code_interpreter=use_code_interpreter,
            use_rag=use_rag,
            use_file_storage=use_file_storage
        )
        
        # Initialize storage
        if storage_path:
            self.storage_path = Path(storage_path)
            self.storage_path.mkdir(parents=True, exist_ok=True)
        else:
            self.storage_path = None
        
        # Initialize components
        self._init_components()
        
        # Load shared instructions
        self.shared_instructions = self._load_shared_instructions()
        
        # Initialize agents
        self.agents = {agent.config.name: agent for agent in agents}
        
        # Set up communication flows
        self.flows = {}
        for source, target in flows:
            if source not in self.agents or target not in self.agents:
                raise ValueError(f"Invalid flow: {source} -> {target}")
            
            flow = CommunicationFlow(
                source=source,
                target=target,
                thread_id=self.thread_manager.create_thread().id
            )
            self.flows[(source, target)] = flow
    
    def _init_components(self):
        """Initialize agency components."""
        # Initialize thread manager
        thread_storage = self.storage_path / "threads" if self.storage_path else None
        self.thread_manager = ThreadManager(storage_path=thread_storage)
        
        # Initialize file manager if enabled
        self.file_manager = None
        if self.config.use_file_storage:
            file_storage = self.storage_path / "files" if self.storage_path else None
            self.file_manager = FileManager(storage_path=file_storage)
        
        # Initialize code interpreter if enabled
        self.code_interpreter = None
        if self.config.use_code_interpreter:
            interpreter_workspace = self.storage_path / "workspace" if self.storage_path else None
            self.code_interpreter = CodeInterpreter(workspace_dir=interpreter_workspace)
        
        # Initialize RAG system if enabled
        self.rag_system = None
        if self.config.use_rag:
            rag_storage = self.storage_path / "rag" if self.storage_path else None
            self.rag_system = RAGSystem(storage_path=rag_storage)
    
    def _load_shared_instructions(self) -> str:
        """Load shared instructions from file."""
        if not self.config.shared_instructions:
            return ""
            
        if os.path.isfile(self.config.shared_instructions):
            with open(self.config.shared_instructions, 'r') as f:
                return f.read()
        
        return self.config.shared_instructions
    
    def get_agent(self, name: str) -> Optional[BaseAgent]:
        """Get an agent by name."""
        return self.agents.get(name)
    
    def list_agents(self) -> List[str]:
        """List all agents in the agency."""
        return list(self.agents.keys())
    
    def can_communicate(self, source: str, target: str) -> bool:
        """Check if two agents can communicate."""
        return (source, target) in self.flows
    
    def get_flow(self, source: str, target: str) -> Optional[CommunicationFlow]:
        """Get communication flow between two agents."""
        return self.flows.get((source, target))
    
    def send_message(
        self,
        source: str,
        target: str,
        content: str,
        metadata: Dict = None
    ) -> Message:
        """
        Send a message from one agent to another.
        
        Args:
            source: Name of the source agent
            target: Name of the target agent
            content: Message content
            metadata: Additional metadata
            
        Returns:
            The created Message instance
        """
        # Validate communication flow
        if not self.can_communicate(source, target):
            raise ValueError(f"No communication flow from {source} to {target}")
        
        # Get the flow and thread
        flow = self.get_flow(source, target)
        thread = self.thread_manager.get_thread(flow.thread_id)
        
        # Add message to thread
        message = thread.add_message(
            role="user",
            content=content,
            agent_name=source,
            metadata=metadata
        )
        
        # Process message with target agent
        target_agent = self.get_agent(target)
        response = target_agent._process_with_llm(thread)
        
        # Add response to thread
        thread.add_message(
            role="assistant",
            content=response,
            agent_name=target
        )
        
        return message
    
    def broadcast_message(
        self,
        source: str,
        content: str,
        metadata: Dict = None
    ) -> List[Message]:
        """
        Broadcast a message to all connected agents.
        
        Args:
            source: Name of the source agent
            content: Message content
            metadata: Additional metadata
            
        Returns:
            List of created Message instances
        """
        messages = []
        for flow in self.flows.values():
            if flow.source == source:
                message = self.send_message(
                    source=source,
                    target=flow.target,
                    content=content,
                    metadata=metadata
                )
                messages.append(message)
        return messages
    
    def upload_file(
        self,
        file: Any,
        filename: str,
        purpose: str = "attachment",
        metadata: Dict = None
    ):
        """Upload a file to shared storage."""
        if not self.file_manager:
            raise RuntimeError("File storage not enabled for this agency")
        return self.file_manager.upload_file(file, filename, purpose, metadata)
    
    def execute_code(
        self,
        code: str,
        language: str = "python",
        additional_files: Dict[str, str] = None,
        environment: Dict[str, str] = None
    ):
        """Execute code in the shared secure environment."""
        if not self.code_interpreter:
            raise RuntimeError("Code interpreter not enabled for this agency")
        return self.code_interpreter.execute(code, language, additional_files, environment)
    
    def search_knowledge(
        self,
        query: str,
        k: int = 5,
        threshold: float = None
    ):
        """Search the shared knowledge base using RAG."""
        if not self.rag_system:
            raise RuntimeError("RAG not enabled for this agency")
        return self.rag_system.search(query, k, threshold)
    
    def add_to_knowledge(
        self,
        content: str,
        metadata: Dict = None
    ):
        """Add content to the shared knowledge base."""
        if not self.rag_system:
            raise RuntimeError("RAG not enabled for this agency")
        return self.rag_system.add_document(content, metadata)
    
    def save_state(self):
        """Save agency state to storage."""
        if not self.storage_path:
            return
            
        # Save components state
        self.thread_manager.save_all_threads()
        if self.file_manager:
            self.file_manager._save_index()
        if self.rag_system:
            self.rag_system._save_state()
        
        # Save flows
        flows_path = self.storage_path / "flows.json"
        with open(flows_path, 'w') as f:
            json.dump(
                {
                    f"{source}->{target}": flow.dict()
                    for (source, target), flow in self.flows.items()
                },
                f,
                indent=2
            )
        
        # Save agents state
        for agent in self.agents.values():
            agent.save_state()
    
    def load_state(self):
        """Load agency state from storage."""
        if not self.storage_path:
            return
            
        # Load components state
        self.thread_manager.load_all_threads()
        if self.file_manager:
            self.file_manager._load_index()
        if self.rag_system:
            self.rag_system._load_state()
        
        # Load flows
        flows_path = self.storage_path / "flows.json"
        if flows_path.exists():
            with open(flows_path, 'r') as f:
                flows_data = json.load(f)
                for key, flow_data in flows_data.items():
                    source, target = key.split("->")
                    self.flows[(source, target)] = CommunicationFlow(**flow_data)
        
        # Load agents state
        for agent in self.agents.values():
            agent.load_state()
    
    def run_demo(self):
        """Print welcome message and instructions for the demo."""
        print(f"\nWelcome to the {self.get_agent(self.config.name).name} Agency Demo!")
        print("\nType 'exit' to end the conversation.")
        print("\nEnter your message:")
        asyncio.run(self.demo_loop())
    
    async def demo_loop(self):
        """Run the interactive demo loop."""
        try:
            while True:
                user_input = input("> ")
                if user_input.lower() == 'exit':
                    print("\nThank you for using the agency. Goodbye!")
                    break
                
                response = await self.process_message(user_input)
                print(f"\n{self.get_agent(self.config.name).name}: {response}")
        
        except KeyboardInterrupt:
            print("\n\nDemo terminated by user. Goodbye!")
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
    
    async def process_message(self, message: str) -> str:
        """Process a message through the agency."""
        response = await self.get_agent(self.config.name)._process_with_llm(message)
        return response 