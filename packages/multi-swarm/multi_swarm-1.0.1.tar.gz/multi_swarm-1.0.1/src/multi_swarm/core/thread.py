from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel, Field
import uuid
import json

class Message(BaseModel):
    """
    Represents a message in a conversation thread.
    
    Attributes:
        id: Unique identifier for the message
        role: Role of the message sender (e.g., "user", "assistant", "system")
        content: The actual message content
        created_at: Timestamp when the message was created
        agent_name: Name of the agent that created the message
        metadata: Additional metadata about the message
        file_ids: List of file IDs attached to this message
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    role: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    agent_name: str
    metadata: Dict = Field(default_factory=dict)
    file_ids: List[str] = Field(default_factory=list)

    def to_dict(self) -> Dict:
        """Convert the message to a dictionary format."""
        return {
            "id": self.id,
            "role": self.role,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "agent_name": self.agent_name,
            "metadata": self.metadata,
            "file_ids": self.file_ids
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Message":
        """Create a Message instance from a dictionary."""
        data["created_at"] = datetime.fromisoformat(data["created_at"])
        return cls(**data)

class Thread(BaseModel):
    """
    Represents a conversation thread containing messages and metadata.
    
    Attributes:
        id: Unique identifier for the thread
        messages: List of messages in the thread
        metadata: Additional metadata about the thread
        created_at: Timestamp when the thread was created
        last_active_at: Timestamp of the last activity in the thread
        status: Current status of the thread (e.g., "active", "completed")
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    messages: List[Message] = Field(default_factory=list)
    metadata: Dict = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_active_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="active")
    
    def add_message(self, role: str, content: str, agent_name: str, file_ids: List[str] = None) -> Message:
        """
        Add a new message to the thread.
        
        Args:
            role: Role of the message sender
            content: Content of the message
            agent_name: Name of the agent sending the message
            file_ids: Optional list of file IDs to attach to the message
            
        Returns:
            The created Message instance
        """
        message = Message(
            role=role, 
            content=content, 
            agent_name=agent_name,
            file_ids=file_ids or []
        )
        self.messages.append(message)
        self.last_active_at = datetime.utcnow()
        return message
    
    def get_messages(self, limit: Optional[int] = None, role: Optional[str] = None) -> List[Message]:
        """
        Get messages from the thread with optional filtering.
        
        Args:
            limit: Optional maximum number of messages to return
            role: Optional role to filter messages by
            
        Returns:
            List of messages matching the criteria
        """
        filtered_messages = self.messages
        if role:
            filtered_messages = [m for m in filtered_messages if m.role == role]
        if limit:
            filtered_messages = filtered_messages[-limit:]
        return filtered_messages
    
    def get_context_window(self, max_messages: int = 10) -> List[Message]:
        """
        Get the most recent messages as context for the next interaction.
        
        Args:
            max_messages: Maximum number of messages to include in the context
            
        Returns:
            List of most recent messages
        """
        return self.get_messages(limit=max_messages)
    
    def save_to_file(self, filepath: str):
        """
        Save the thread to a JSON file.
        
        Args:
            filepath: Path where to save the thread data
        """
        data = {
            "id": self.id,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "last_active_at": self.last_active_at.isoformat(),
            "status": self.status,
            "messages": [m.to_dict() for m in self.messages]
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    @classmethod
    def load_from_file(cls, filepath: str) -> "Thread":
        """
        Load a thread from a JSON file.
        
        Args:
            filepath: Path to the thread data file
            
        Returns:
            Thread instance loaded from the file
        """
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Convert ISO format strings back to datetime
        data["created_at"] = datetime.fromisoformat(data["created_at"])
        data["last_active_at"] = datetime.fromisoformat(data["last_active_at"])
        
        # Convert message dictionaries back to Message objects
        data["messages"] = [Message.from_dict(m) for m in data["messages"]]
        
        return cls(**data)

class ThreadManager:
    """
    Manages multiple conversation threads.
    
    Attributes:
        threads: Dictionary mapping thread IDs to Thread instances
        storage_path: Optional path for persistent storage of threads
    """
    def __init__(self, storage_path: Optional[str] = None):
        self.threads: Dict[str, Thread] = {}
        self.storage_path = storage_path
    
    def create_thread(self, metadata: Dict = None) -> Thread:
        """
        Create a new thread.
        
        Args:
            metadata: Optional metadata to associate with the thread
            
        Returns:
            The created Thread instance
        """
        thread = Thread(metadata=metadata or {})
        self.threads[thread.id] = thread
        return thread
    
    def get_thread(self, thread_id: str) -> Optional[Thread]:
        """
        Get a thread by its ID.
        
        Args:
            thread_id: ID of the thread to retrieve
            
        Returns:
            The Thread instance if found, None otherwise
        """
        return self.threads.get(thread_id)
    
    def list_threads(self, status: Optional[str] = None) -> List[Thread]:
        """
        List all threads, optionally filtered by status.
        
        Args:
            status: Optional status to filter threads by
            
        Returns:
            List of threads matching the criteria
        """
        if status:
            return [t for t in self.threads.values() if t.status == status]
        return list(self.threads.values())
    
    def delete_thread(self, thread_id: str) -> bool:
        """
        Delete a thread.
        
        Args:
            thread_id: ID of the thread to delete
            
        Returns:
            True if the thread was deleted, False if it wasn't found
        """
        if thread_id in self.threads:
            del self.threads[thread_id]
            return True
        return False
    
    def save_all_threads(self):
        """Save all threads to storage if storage_path is set."""
        if not self.storage_path:
            return
        
        for thread_id, thread in self.threads.items():
            filepath = f"{self.storage_path}/thread_{thread_id}.json"
            thread.save_to_file(filepath)
    
    def load_all_threads(self):
        """Load all threads from storage if storage_path is set."""
        if not self.storage_path:
            return
        
        import glob
        import os
        
        thread_files = glob.glob(f"{self.storage_path}/thread_*.json")
        for filepath in thread_files:
            thread = Thread.load_from_file(filepath)
            self.threads[thread.id] = thread 