from multi_swarm import Agency
from research_manager import ResearchManager
from data_analyst import DataAnalyst
from document_processor import DocumentProcessor
from pathlib import Path
import json

class ResearchAssistantAgency:
    """
    Research Assistant Agency
    
    A collaborative agency that helps with research tasks by coordinating:
    - Research planning and management
    - Data analysis and visualization
    - Document processing and information extraction
    """
    
    def __init__(self, storage_path: str = "./storage"):
        # Initialize storage paths
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize agents
        self.research_manager = ResearchManager(
            storage_path=str(self.storage_path / "research_manager")
        )
        self.data_analyst = DataAnalyst(
            storage_path=str(self.storage_path / "data_analyst")
        )
        self.document_processor = DocumentProcessor(
            storage_path=str(self.storage_path / "document_processor")
        )
        
        # Initialize agency
        self.agency = Agency(
            name="Research Assistant Agency",
            description="Collaborative agency for research tasks",
            agents=[
                self.research_manager,  # Entry point for user communication
                self.data_analyst,
                self.document_processor
            ],
            flows=[
                # Research Manager can communicate with both Data Analyst and Document Processor
                [self.research_manager, self.data_analyst],
                [self.research_manager, self.document_processor],
                # Data Analyst can communicate with Document Processor
                [self.data_analyst, self.document_processor]
            ],
            shared_instructions="./instructions/agency_manifesto.md",
            storage_path=storage_path,
            use_file_storage=True,
            use_rag=True,
            use_code_interpreter=True
        )
    
    def start_research(self, topic: str, requirements: dict = None) -> str:
        """Start a new research project."""
        return self.research_manager.create_research_thread(
            topic=topic,
            requirements=requirements or {}
        )
    
    def process_document(self, thread_id: str, document_path: str) -> dict:
        """Process a document for the research project."""
        # First, process the document
        doc_results = self.document_processor.process_document(
            thread_id=thread_id,
            document_path=document_path
        )
        
        # Update research status with document findings
        self.research_manager.update_research_status(
            thread_id=thread_id,
            status="document_processed",
            notes=f"Processed document: {Path(document_path).name}\n" +
                  f"Summary: {doc_results['summary']['summary']}\n" +
                  f"Key findings: {', '.join(kw['phrase'] for kw in doc_results['keywords']['keywords'])}"
        )
        
        return doc_results
    
    def analyze_data(self, thread_id: str, dataset_path: str, analysis_type: str) -> dict:
        """Analyze data for the research project."""
        # First, analyze the dataset
        analysis_results = self.data_analyst.analyze_dataset(
            thread_id=thread_id,
            dataset_path=dataset_path,
            analysis_type=analysis_type
        )
        
        # Update research status with analysis findings
        self.research_manager.update_research_status(
            thread_id=thread_id,
            status="data_analyzed",
            notes=f"Analyzed dataset: {Path(dataset_path).name}\n" +
                  f"Analysis type: {analysis_type}\n" +
                  f"Key findings: {json.dumps(analysis_results, indent=2)}"
        )
        
        return analysis_results
    
    def get_research_summary(self, thread_id: str) -> dict:
        """Get a comprehensive summary of the research project."""
        # Get research overview
        research_summary = self.research_manager.get_research_summary(thread_id)
        
        # Get document history
        doc_history = self.document_processor.get_document_history(thread_id)
        
        # Get analysis history
        analysis_history = self.data_analyst.get_analysis_history(thread_id)
        
        return {
            "research_summary": research_summary,
            "document_history": doc_history,
            "analysis_history": analysis_history
        }
    
    def search_project(self, thread_id: str, query: str) -> dict:
        """Search across all project resources."""
        return {
            "documents": self.document_processor.search_documents(
                thread_id=thread_id,
                query=query
            ),
            "analyses": self.data_analyst.search_analyses(
                thread_id=thread_id,
                query=query
            )
        }
    
    def run_demo(self):
        """Run the agency in demo mode."""
        self.agency.run_demo()

if __name__ == "__main__":
    # Create and run the agency
    agency = ResearchAssistantAgency()
    agency.run_demo() 