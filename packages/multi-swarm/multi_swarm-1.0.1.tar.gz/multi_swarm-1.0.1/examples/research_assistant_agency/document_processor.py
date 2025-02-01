from multi_swarm import Agent
from typing import Dict, Any, List
import json
from pathlib import Path

class DocumentProcessor(Agent):
    """
    Document Processor Agent
    
    Responsible for:
    - Processing and analyzing documents
    - Extracting key information
    - Generating summaries
    - Managing document storage
    """
    
    def __init__(self, storage_path: str = "./storage/document_processor"):
        super().__init__(
            name="Document Processor",
            description="Processes documents and extracts information",
            instructions="./instructions/document_processor.md",
            tools_folder="./tools/document_processor",
            llm_provider="claude",
            provider_config={
                "model": "claude-3-sonnet",
                "max_tokens": 4096
            },
            temperature=0.7,
            storage_path=storage_path,
            use_file_storage=True,  # For storing documents
            use_rag=True,  # For document retrieval
            use_code_interpreter=True  # For text processing tasks
        )
    
    def process_document(
        self,
        thread_id: str,
        document_path: str,
        processing_type: str = "full",
        parameters: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Process a document and extract information.
        
        Args:
            thread_id: ID of the research thread
            document_path: Path to the document file
            processing_type: Type of processing to perform
            parameters: Additional processing parameters
        """
        # Load document
        with open(document_path, 'rb') as f:
            document_file = self.upload_file(
                f,
                filename=Path(document_path).name,
                purpose="document_input",
                metadata={
                    "thread_id": thread_id,
                    "processing_type": processing_type
                }
            )
        
        # Extract text content based on file type
        text_content = self._extract_text(document_file.id)
        
        # Process the text
        if processing_type == "summary":
            results = self._generate_summary(text_content)
        elif processing_type == "keywords":
            results = self._extract_keywords(text_content)
        elif processing_type == "full":
            results = {
                "summary": self._generate_summary(text_content),
                "keywords": self._extract_keywords(text_content),
                "metadata": document_file.metadata
            }
        else:
            raise ValueError(f"Unsupported processing type: {processing_type}")
        
        # Store results in knowledge base
        self.add_to_knowledge(
            f"Document Processing Results for Thread {thread_id}:\n" +
            f"Document: {document_file.filename}\n" +
            f"Processing Type: {processing_type}\n" +
            f"Results: {json.dumps(results, indent=2)}"
        )
        
        return results
    
    def _extract_text(self, file_id: str) -> str:
        """Extract text content from a document."""
        file_obj = self.get_file(file_id)
        if not file_obj:
            raise ValueError(f"File {file_id} not found")
        
        content = self.read_file(file_id)
        
        # Generate text extraction code based on file type
        if file_obj.file_type == "application/pdf":
            code = """
                import io
                import PyPDF2
                import json
                
                # Read PDF content
                pdf_content = io.BytesIO(input_bytes)
                reader = PyPDF2.PdfReader(pdf_content)
                
                # Extract text from all pages
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
                
                print(json.dumps({"text": text}))
            """
        else:
            # Assume text file
            return content.decode('utf-8')
        
        # Execute extraction code
        result = self.execute_code(
            code=code,
            language="python",
            environment={"input_bytes": content}
        )
        
        try:
            return json.loads(result.output)["text"]
        except:
            raise RuntimeError(f"Failed to extract text: {result.error}")
    
    def _generate_summary(self, text: str) -> Dict[str, Any]:
        """Generate a summary of the text."""
        code = """
            from transformers import pipeline
            import json
            
            # Initialize summarizer
            summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
            
            # Split text into chunks (max 1024 tokens)
            max_chunk_size = 1024
            chunks = [text[i:i+max_chunk_size] for i in range(0, len(text), max_chunk_size)]
            
            # Summarize each chunk
            summaries = []
            for chunk in chunks:
                summary = summarizer(chunk, max_length=130, min_length=30)[0]
                summaries.append(summary["summary_text"])
            
            # Combine summaries
            final_summary = " ".join(summaries)
            
            print(json.dumps({
                "summary": final_summary,
                "num_chunks": len(chunks)
            }))
        """
        
        result = self.execute_code(
            code=code,
            language="python",
            environment={"text": text}
        )
        
        try:
            return json.loads(result.output)
        except:
            raise RuntimeError(f"Failed to generate summary: {result.error}")
    
    def _extract_keywords(self, text: str) -> Dict[str, Any]:
        """Extract keywords from the text."""
        code = """
            from keybert import KeyBERT
            import json
            
            # Initialize keyword extractor
            kw_model = KeyBERT()
            
            # Extract keywords
            keywords = kw_model.extract_keywords(
                text,
                keyphrase_ngram_range=(1, 2),
                stop_words="english",
                use_maxsum=True,
                nr_candidates=20,
                top_n=10
            )
            
            print(json.dumps({
                "keywords": [{"phrase": kw, "score": float(score)} for kw, score in keywords]
            }))
        """
        
        result = self.execute_code(
            code=code,
            language="python",
            environment={"text": text}
        )
        
        try:
            return json.loads(result.output)
        except:
            raise RuntimeError(f"Failed to extract keywords: {result.error}")
    
    def search_documents(
        self,
        thread_id: str,
        query: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Search for relevant documents."""
        results = self.search_knowledge(
            query=f"thread:{thread_id} {query}",
            k=limit
        )
        
        return [{
            "content": r.document.content,
            "score": r.score,
            "metadata": r.document.metadata
        } for r in results]
    
    def get_document_history(self, thread_id: str) -> List[Dict[str, Any]]:
        """Get processing history for documents in a thread."""
        # Search for document processing results
        results = self.search_knowledge(
            f"document processing results thread:{thread_id}",
            k=20
        )
        
        # Get list of processed files
        files = self.list_files(purpose="document_input")
        thread_files = [
            f for f in files
            if f.metadata.get("thread_id") == thread_id
        ]
        
        return {
            "processing_results": [{
                "content": r.document.content,
                "score": r.score,
                "created_at": r.document.created_at
            } for r in results],
            "files": [{
                "id": f.id,
                "filename": f.filename,
                "created_at": f.created_at,
                "metadata": f.metadata
            } for f in thread_files]
        } 