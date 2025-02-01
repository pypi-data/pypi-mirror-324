from typing import BinaryIO, Dict, List, Optional, Union
from pathlib import Path
import hashlib
import shutil
import json
from datetime import datetime
from pydantic import BaseModel, Field
import uuid
import mimetypes
import os

class File(BaseModel):
    """
    Represents a file in the system.
    
    Attributes:
        id: Unique identifier for the file
        filename: Original name of the file
        purpose: Purpose of the file (e.g., "input", "output", "attachment")
        file_type: MIME type of the file
        size_bytes: Size of the file in bytes
        created_at: Timestamp when the file was created
        content_hash: SHA-256 hash of the file content
        metadata: Additional metadata about the file
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    filename: str
    purpose: str
    file_type: str
    size_bytes: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    content_hash: str
    metadata: Dict = Field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """Convert the file metadata to a dictionary format."""
        return {
            "id": self.id,
            "filename": self.filename,
            "purpose": self.purpose,
            "file_type": self.file_type,
            "size_bytes": self.size_bytes,
            "created_at": self.created_at.isoformat(),
            "content_hash": self.content_hash,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "File":
        """Create a File instance from a dictionary."""
        data["created_at"] = datetime.fromisoformat(data["created_at"])
        return cls(**data)

class FileManager:
    """
    Manages file storage and retrieval.
    
    Attributes:
        storage_path: Path where files are stored
        files: Dictionary mapping file IDs to File instances
        index_path: Path to the file index JSON
    """
    def __init__(self, storage_path: Union[str, Path]):
        self.storage_path = Path(storage_path)
        self.files: Dict[str, File] = {}
        self.index_path = self.storage_path / "file_index.json"
        
        # Create storage directory if it doesn't exist
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # Load existing file index if it exists
        if self.index_path.exists():
            self._load_index()
    
    def _load_index(self):
        """Load the file index from disk."""
        with open(self.index_path, 'r') as f:
            data = json.load(f)
            self.files = {
                file_id: File.from_dict(file_data)
                for file_id, file_data in data.items()
            }
    
    def _save_index(self):
        """Save the file index to disk."""
        with open(self.index_path, 'w') as f:
            json.dump(
                {file_id: file.to_dict() for file_id, file in self.files.items()},
                f,
                indent=2
            )
    
    def _get_file_path(self, file_id: str) -> Path:
        """Get the storage path for a file."""
        return self.storage_path / file_id
    
    def upload_file(
        self, 
        file: BinaryIO, 
        filename: str, 
        purpose: str = "attachment",
        metadata: Dict = None
    ) -> File:
        """
        Upload a file to storage.
        
        Args:
            file: File-like object to upload
            filename: Original name of the file
            purpose: Purpose of the file
            metadata: Additional metadata to store with the file
            
        Returns:
            File instance representing the uploaded file
        """
        content = file.read()
        content_hash = hashlib.sha256(content).hexdigest()
        
        # Detect file type
        file_type, _ = mimetypes.guess_type(filename)
        if file_type is None:
            file_type = "application/octet-stream"
        
        # Create file metadata
        file_obj = File(
            filename=filename,
            purpose=purpose,
            file_type=file_type,
            size_bytes=len(content),
            content_hash=content_hash,
            metadata=metadata or {}
        )
        
        # Store the file
        file_path = self._get_file_path(file_obj.id)
        with open(file_path, 'wb') as f:
            f.write(content)
        
        # Update index
        self.files[file_obj.id] = file_obj
        self._save_index()
        
        return file_obj
    
    def get_file(self, file_id: str) -> Optional[File]:
        """
        Get file metadata by ID.
        
        Args:
            file_id: ID of the file to retrieve
            
        Returns:
            File instance if found, None otherwise
        """
        return self.files.get(file_id)
    
    def read_file(self, file_id: str) -> Optional[bytes]:
        """
        Read file content by ID.
        
        Args:
            file_id: ID of the file to read
            
        Returns:
            File content as bytes if found, None otherwise
        """
        if file_id not in self.files:
            return None
        
        file_path = self._get_file_path(file_id)
        if not file_path.exists():
            return None
        
        with open(file_path, 'rb') as f:
            return f.read()
    
    def delete_file(self, file_id: str) -> bool:
        """
        Delete a file.
        
        Args:
            file_id: ID of the file to delete
            
        Returns:
            True if the file was deleted, False if it wasn't found
        """
        if file_id not in self.files:
            return False
        
        file_path = self._get_file_path(file_id)
        if file_path.exists():
            os.remove(file_path)
        
        del self.files[file_id]
        self._save_index()
        
        return True
    
    def list_files(
        self, 
        purpose: Optional[str] = None,
        file_type: Optional[str] = None
    ) -> List[File]:
        """
        List files with optional filtering.
        
        Args:
            purpose: Optional purpose to filter files by
            file_type: Optional file type to filter files by
            
        Returns:
            List of files matching the criteria
        """
        files = self.files.values()
        
        if purpose:
            files = [f for f in files if f.purpose == purpose]
        if file_type:
            files = [f for f in files if f.file_type == file_type]
            
        return list(files)
    
    def copy_file(
        self, 
        file_id: str, 
        new_filename: Optional[str] = None,
        new_purpose: Optional[str] = None,
        new_metadata: Optional[Dict] = None
    ) -> Optional[File]:
        """
        Create a copy of a file with optional modifications.
        
        Args:
            file_id: ID of the file to copy
            new_filename: Optional new filename for the copy
            new_purpose: Optional new purpose for the copy
            new_metadata: Optional new metadata for the copy
            
        Returns:
            New File instance if successful, None if source file not found
        """
        source_file = self.get_file(file_id)
        if not source_file:
            return None
        
        source_content = self.read_file(file_id)
        if not source_content:
            return None
        
        # Create new file with modified attributes
        new_file = File(
            filename=new_filename or source_file.filename,
            purpose=new_purpose or source_file.purpose,
            file_type=source_file.file_type,
            size_bytes=len(source_content),
            content_hash=source_file.content_hash,
            metadata=new_metadata or dict(source_file.metadata)
        )
        
        # Store the new file
        file_path = self._get_file_path(new_file.id)
        with open(file_path, 'wb') as f:
            f.write(source_content)
        
        # Update index
        self.files[new_file.id] = new_file
        self._save_index()
        
        return new_file 