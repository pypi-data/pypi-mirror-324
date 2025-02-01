from typing import List, Dict, Optional, Union, Any
import numpy as np
from pathlib import Path
import json
import pickle
from datetime import datetime
from pydantic import BaseModel, Field
import uuid
from sentence_transformers import SentenceTransformer
import faiss
import torch
from transformers import AutoTokenizer, AutoModel
import os
import hashlib

class Document(BaseModel):
    """
    Represents a document in the RAG system.
    
    Attributes:
        id: Unique identifier for the document
        content: The text content of the document
        metadata: Additional metadata about the document
        embedding: Pre-computed embedding vector (optional)
        created_at: Timestamp when the document was created
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content: str
    metadata: Dict = Field(default_factory=dict)
    embedding: Optional[List[float]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict:
        """Convert the document to a dictionary format."""
        return {
            "id": self.id,
            "content": self.content,
            "metadata": self.metadata,
            "embedding": self.embedding,
            "created_at": self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "Document":
        """Create a Document instance from a dictionary."""
        data["created_at"] = datetime.fromisoformat(data["created_at"])
        return cls(**data)

class SearchResult(BaseModel):
    """
    Represents a search result from the RAG system.
    
    Attributes:
        document: The matched document
        score: Similarity score of the match
        metadata: Additional metadata about the match
    """
    document: Document
    score: float
    metadata: Dict = Field(default_factory=dict)

class RAGSystem:
    """
    Advanced Retrieval-Augmented Generation system with multiple embedding models
    and sophisticated retrieval strategies.
    """
    
    DEFAULT_MODEL = "all-MiniLM-L6-v2"
    
    def __init__(
        self,
        model_name: str = DEFAULT_MODEL,
        storage_path: Optional[Union[str, Path]] = None,
        device: str = None,
        use_gpu: bool = None
    ):
        """
        Initialize the RAG system.
        
        Args:
            model_name: Name of the embedding model to use
            storage_path: Path for persistent storage
            device: Device to use for computations
            use_gpu: Whether to use GPU acceleration
        """
        self.model_name = model_name
        self.storage_path = Path(storage_path) if storage_path else None
        
        # Determine device
        if device is None:
            device = "cuda" if (use_gpu or torch.cuda.is_available()) else "cpu"
        self.device = device
        
        # Initialize embedding model
        self.model = SentenceTransformer(model_name, device=device)
        
        # Initialize FAISS index
        self.dimension = self.model.get_sentence_embedding_dimension()
        self.index = faiss.IndexFlatL2(self.dimension)
        
        if device == "cuda" and torch.cuda.is_available():
            self.index = faiss.index_cpu_to_gpu(
                faiss.StandardGpuResources(),
                0,
                self.index
            )
        
        # Initialize document storage
        self.documents: Dict[str, Document] = {}
        
        # Load existing index if available
        if self.storage_path:
            self.storage_path.mkdir(parents=True, exist_ok=True)
            self._load_state()
    
    def _compute_embedding(self, text: str) -> np.ndarray:
        """Compute embedding for a text string."""
        return self.model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True
        )
    
    def _save_state(self):
        """Save the current state to disk."""
        if not self.storage_path:
            return
            
        # Save documents
        docs_path = self.storage_path / "documents.json"
        with open(docs_path, 'w') as f:
            json.dump(
                {doc_id: doc.to_dict() for doc_id, doc in self.documents.items()},
                f,
                indent=2
            )
        
        # Save FAISS index
        index_path = self.storage_path / "index.faiss"
        if isinstance(self.index, faiss.GpuIndex):
            index_cpu = faiss.index_gpu_to_cpu(self.index)
            faiss.write_index(index_cpu, str(index_path))
        else:
            faiss.write_index(self.index, str(index_path))
    
    def _load_state(self):
        """Load the saved state from disk."""
        # Load documents
        docs_path = self.storage_path / "documents.json"
        if docs_path.exists():
            with open(docs_path, 'r') as f:
                data = json.load(f)
                self.documents = {
                    doc_id: Document.from_dict(doc_data)
                    for doc_id, doc_data in data.items()
                }
        
        # Load FAISS index
        index_path = self.storage_path / "index.faiss"
        if index_path.exists():
            self.index = faiss.read_index(str(index_path))
            if self.device == "cuda" and torch.cuda.is_available():
                self.index = faiss.index_cpu_to_gpu(
                    faiss.StandardGpuResources(),
                    0,
                    self.index
                )
    
    def add_document(
        self,
        content: str,
        metadata: Dict = None,
        compute_embedding: bool = True
    ) -> Document:
        """
        Add a document to the RAG system.
        
        Args:
            content: Text content of the document
            metadata: Additional metadata about the document
            compute_embedding: Whether to compute and store embedding
            
        Returns:
            The created Document instance
        """
        # Create document
        doc = Document(
            content=content,
            metadata=metadata or {},
            embedding=None
        )
        
        # Compute embedding if requested
        if compute_embedding:
            embedding = self._compute_embedding(content)
            doc.embedding = embedding.tolist()
            self.index.add(embedding.reshape(1, -1))
        
        # Store document
        self.documents[doc.id] = doc
        
        # Save state
        self._save_state()
        
        return doc
    
    def add_documents(
        self,
        documents: List[Union[str, Dict]],
        batch_size: int = 32
    ) -> List[Document]:
        """
        Add multiple documents in batch.
        
        Args:
            documents: List of documents (strings or dicts with content and metadata)
            batch_size: Size of batches for processing
            
        Returns:
            List of created Document instances
        """
        results = []
        batch = []
        
        for doc in documents:
            if isinstance(doc, str):
                batch.append({"content": doc, "metadata": {}})
            else:
                batch.append(doc)
                
            if len(batch) >= batch_size:
                results.extend(self._process_batch(batch))
                batch = []
        
        if batch:
            results.extend(self._process_batch(batch))
        
        return results
    
    def _process_batch(self, batch: List[Dict]) -> List[Document]:
        """Process a batch of documents."""
        # Extract content
        contents = [doc["content"] for doc in batch]
        
        # Compute embeddings
        embeddings = self.model.encode(
            contents,
            batch_size=len(batch),
            convert_to_numpy=True,
            normalize_embeddings=True
        )
        
        # Create documents
        documents = []
        for doc_dict, embedding in zip(batch, embeddings):
            doc = Document(
                content=doc_dict["content"],
                metadata=doc_dict.get("metadata", {}),
                embedding=embedding.tolist()
            )
            self.documents[doc.id] = doc
            documents.append(doc)
        
        # Add to index
        self.index.add(embeddings)
        
        # Save state
        self._save_state()
        
        return documents
    
    def search(
        self,
        query: str,
        k: int = 5,
        threshold: float = None,
        filter_fn: callable = None
    ) -> List[SearchResult]:
        """
        Search for relevant documents.
        
        Args:
            query: Search query
            k: Number of results to return
            threshold: Optional similarity threshold
            filter_fn: Optional function to filter results
            
        Returns:
            List of SearchResult instances
        """
        # Compute query embedding
        query_embedding = self._compute_embedding(query)
        
        # Search index
        D, I = self.index.search(
            query_embedding.reshape(1, -1),
            k
        )
        
        # Process results
        results = []
        for score, idx in zip(D[0], I[0]):
            if idx < 0:  # Invalid index
                continue
                
            # Get document
            doc_id = list(self.documents.keys())[idx]
            doc = self.documents[doc_id]
            
            # Apply threshold
            if threshold is not None and score > threshold:
                continue
            
            # Apply filter
            if filter_fn and not filter_fn(doc):
                continue
            
            results.append(SearchResult(
                document=doc,
                score=float(score)
            ))
        
        return results
    
    def get_document(self, doc_id: str) -> Optional[Document]:
        """Get a document by ID."""
        return self.documents.get(doc_id)
    
    def delete_document(self, doc_id: str) -> bool:
        """
        Delete a document.
        
        Note: This is a soft delete that only removes the document from storage.
        The embedding remains in the FAISS index until rebuild_index() is called.
        """
        if doc_id in self.documents:
            del self.documents[doc_id]
            self._save_state()
            return True
        return False
    
    def rebuild_index(self):
        """Rebuild the FAISS index from scratch."""
        # Create new index
        self.index = faiss.IndexFlatL2(self.dimension)
        if self.device == "cuda" and torch.cuda.is_available():
            self.index = faiss.index_cpu_to_gpu(
                faiss.StandardGpuResources(),
                0,
                self.index
            )
        
        # Add all embeddings
        embeddings = []
        for doc in self.documents.values():
            if doc.embedding:
                embeddings.append(doc.embedding)
        
        if embeddings:
            self.index.add(np.array(embeddings))
        
        # Save state
        self._save_state()
    
    def clear(self):
        """Clear all documents and reset the index."""
        self.documents.clear()
        self.rebuild_index()
        self._save_state()

class RAGTool(BaseModel):
    """
    A tool that provides RAG capabilities for agents.
    
    This tool can be used to search through a knowledge base and retrieve
    relevant information for generating responses.
    """
    query: str = Field(..., description="The search query")
    k: int = Field(default=5, description="Number of results to return")
    threshold: Optional[float] = Field(
        default=None,
        description="Optional similarity threshold"
    )
    
    def run(self) -> List[SearchResult]:
        """
        Search the knowledge base and return relevant results.
        
        Returns:
            List of search results
        """
        rag = RAGSystem()
        return rag.search(
            self.query,
            self.k,
            self.threshold
        ) 