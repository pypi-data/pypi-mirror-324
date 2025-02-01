from multi_swarm import Agent
from typing import Dict, Any

class ResearchManager(Agent):
    """
    Research Manager Agent
    
    Responsible for:
    - Coordinating research tasks
    - Managing workflow between agents
    - Tracking research progress
    - Providing final summaries
    """
    
    def __init__(self, storage_path: str = "./storage/research_manager"):
        super().__init__(
            name="Research Manager",
            description="Coordinates research tasks and manages the workflow",
            instructions="./instructions/research_manager.md",
            tools_folder="./tools/research_manager",
            llm_provider="claude",
            provider_config={
                "model": "claude-3-sonnet",
                "max_tokens": 4096
            },
            temperature=0.7,
            storage_path=storage_path,
            use_file_storage=True,  # For storing research artifacts
            use_rag=True,  # For maintaining research context
            use_code_interpreter=False  # Not needed for management tasks
        )
        
    def create_research_thread(self, topic: str, requirements: Dict[str, Any]) -> str:
        """Create a new research thread."""
        thread = self.create_thread({
            "topic": topic,
            "requirements": requirements,
            "status": "initiated"
        })
        
        # Add initial context to RAG system
        self.add_to_knowledge(
            f"Research Topic: {topic}\n" + 
            f"Requirements: {requirements}\n" +
            f"Thread ID: {thread.id}"
        )
        
        return thread.id
    
    def update_research_status(self, thread_id: str, status: str, notes: str = None):
        """Update research thread status."""
        thread = self.get_thread(thread_id)
        if not thread:
            raise ValueError(f"Thread {thread_id} not found")
        
        thread.metadata["status"] = status
        if notes:
            thread.metadata.setdefault("notes", []).append(notes)
        
        # Add status update to knowledge base
        self.add_to_knowledge(
            f"Thread {thread_id} Status Update:\n" +
            f"Status: {status}\n" +
            (f"Notes: {notes}\n" if notes else "")
        )
    
    def get_research_summary(self, thread_id: str) -> Dict[str, Any]:
        """Get summary of research thread."""
        thread = self.get_thread(thread_id)
        if not thread:
            raise ValueError(f"Thread {thread_id} not found")
        
        # Search knowledge base for relevant information
        results = self.search_knowledge(
            f"research summary thread:{thread_id}",
            k=10
        )
        
        # Compile summary
        return {
            "topic": thread.metadata.get("topic"),
            "status": thread.metadata.get("status"),
            "requirements": thread.metadata.get("requirements"),
            "notes": thread.metadata.get("notes", []),
            "context": [r.document.content for r in results]
        } 