from typing import Any, Dict, List, Optional
import docker
from docker.errors import DockerException
import tempfile
import os
import json
from pathlib import Path
import uuid
from datetime import datetime
from pydantic import BaseModel, Field

class ExecutionResult(BaseModel):
    """
    Represents the result of a code execution.
    
    Attributes:
        output: The output of the code execution
        error: Any error message if execution failed
        execution_time: Time taken to execute the code
        memory_usage: Peak memory usage during execution
        status: Status of the execution (success/error)
    """
    output: str
    error: Optional[str] = None
    execution_time: float
    memory_usage: Optional[int] = None
    status: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CodeInterpreter:
    """
    A secure code execution environment using Docker containers.
    
    This interpreter provides a sandboxed environment for executing code
    with resource limits and security constraints.
    """
    
    DEFAULT_MEMORY_LIMIT = "512m"
    DEFAULT_CPU_LIMIT = "1.0"
    DEFAULT_TIMEOUT = 30  # seconds
    
    SUPPORTED_LANGUAGES = {
        "python": {
            "image": "python:3.9-slim",
            "file_extension": ".py",
            "command": ["python", "{filename}"]
        },
        "javascript": {
            "image": "node:16-slim",
            "file_extension": ".js",
            "command": ["node", "{filename}"]
        },
        "ruby": {
            "image": "ruby:3-slim",
            "file_extension": ".rb",
            "command": ["ruby", "{filename}"]
        }
    }
    
    def __init__(
        self,
        workspace_dir: Optional[str] = None,
        memory_limit: str = DEFAULT_MEMORY_LIMIT,
        cpu_limit: str = DEFAULT_CPU_LIMIT,
        timeout: int = DEFAULT_TIMEOUT
    ):
        """
        Initialize the code interpreter.
        
        Args:
            workspace_dir: Directory for temporary files
            memory_limit: Container memory limit (e.g., "512m")
            cpu_limit: Container CPU limit (e.g., "1.0")
            timeout: Execution timeout in seconds
        """
        self.workspace_dir = Path(workspace_dir) if workspace_dir else Path(tempfile.gettempdir())
        self.memory_limit = memory_limit
        self.cpu_limit = cpu_limit
        self.timeout = timeout
        
        # Ensure workspace directory exists
        self.workspace_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            self.docker_client = docker.from_env()
        except DockerException as e:
            raise RuntimeError(f"Failed to initialize Docker client: {e}")
    
    def _prepare_container_config(self, language: str) -> Dict[str, Any]:
        """Prepare Docker container configuration."""
        if language not in self.SUPPORTED_LANGUAGES:
            raise ValueError(f"Unsupported language: {language}")
            
        lang_config = self.SUPPORTED_LANGUAGES[language]
        
        return {
            "image": lang_config["image"],
            "command": None,  # Will be set during execution
            "mem_limit": self.memory_limit,
            "cpu_quota": int(float(self.cpu_limit) * 100000),
            "cpu_period": 100000,
            "network_mode": "none",
            "security_opt": ["no-new-privileges"],
            "cap_drop": ["ALL"],
            "user": "nobody"
        }
    
    def execute(
        self,
        code: str,
        language: str = "python",
        additional_files: Dict[str, str] = None,
        environment: Dict[str, str] = None
    ) -> ExecutionResult:
        """
        Execute code in a secure container.
        
        Args:
            code: The code to execute
            language: Programming language to use
            additional_files: Additional files to include in the execution environment
            environment: Environment variables for the execution
            
        Returns:
            ExecutionResult containing the output and metadata
        """
        if language not in self.SUPPORTED_LANGUAGES:
            raise ValueError(f"Unsupported language: {language}")
        
        # Create a unique workspace for this execution
        execution_id = str(uuid.uuid4())
        workspace = self.workspace_dir / execution_id
        workspace.mkdir(parents=True)
        
        try:
            # Write the main code file
            lang_config = self.SUPPORTED_LANGUAGES[language]
            main_file = workspace / f"main{lang_config['file_extension']}"
            with open(main_file, 'w') as f:
                f.write(code)
            
            # Write additional files if provided
            if additional_files:
                for filename, content in additional_files.items():
                    file_path = workspace / filename
                    with open(file_path, 'w') as f:
                        f.write(content)
            
            # Prepare container configuration
            container_config = self._prepare_container_config(language)
            container_config["command"] = [
                cmd.format(filename=f"/workspace/main{lang_config['file_extension']}")
                for cmd in lang_config["command"]
            ]
            
            # Add workspace mount
            container_config["volumes"] = {
                str(workspace): {
                    "bind": "/workspace",
                    "mode": "ro"
                }
            }
            
            # Add environment variables
            if environment:
                container_config["environment"] = environment
            
            # Create and run container
            start_time = datetime.utcnow()
            container = self.docker_client.containers.run(
                **container_config,
                working_dir="/workspace",
                detach=True
            )
            
            try:
                container.wait(timeout=self.timeout)
                execution_time = (datetime.utcnow() - start_time).total_seconds()
                
                # Get container stats for memory usage
                stats = container.stats(stream=False)
                memory_usage = stats["memory_stats"].get("max_usage", 0)
                
                # Get output and error
                output = container.logs(stdout=True, stderr=False).decode()
                error = container.logs(stdout=False, stderr=True).decode()
                
                status = "success" if container.wait()["StatusCode"] == 0 else "error"
                
                return ExecutionResult(
                    output=output,
                    error=error if error else None,
                    execution_time=execution_time,
                    memory_usage=memory_usage,
                    status=status
                )
                
            except Exception as e:
                return ExecutionResult(
                    output="",
                    error=str(e),
                    execution_time=self.timeout,
                    status="error"
                )
                
            finally:
                try:
                    container.remove(force=True)
                except:
                    pass
                    
        finally:
            # Cleanup workspace
            try:
                import shutil
                shutil.rmtree(workspace)
            except:
                pass
    
    def list_supported_languages(self) -> List[str]:
        """Get list of supported programming languages."""
        return list(self.SUPPORTED_LANGUAGES.keys())
    
    def get_language_info(self, language: str) -> Optional[Dict[str, Any]]:
        """Get configuration information for a specific language."""
        return self.SUPPORTED_LANGUAGES.get(language)
    
    def validate_code(self, code: str, language: str) -> bool:
        """
        Basic validation of code before execution.
        
        Args:
            code: The code to validate
            language: Programming language of the code
            
        Returns:
            True if code appears valid, False otherwise
        """
        if language not in self.SUPPORTED_LANGUAGES:
            return False
            
        # Add basic validation logic here
        # For now, just check if code is not empty
        return bool(code.strip())

class CodeInterpreterTool(BaseModel):
    """
    A tool that provides secure code execution capabilities.
    
    This tool can be used by agents to execute code in various programming
    languages within a secure, sandboxed environment.
    """
    code: str = Field(..., description="The code to execute")
    language: str = Field(
        default="python",
        description="Programming language to use"
    )
    additional_files: Dict[str, str] = Field(
        default_factory=dict,
        description="Additional files to include in the execution environment"
    )
    environment: Dict[str, str] = Field(
        default_factory=dict,
        description="Environment variables for the execution"
    )
    
    def run(self) -> ExecutionResult:
        """Execute the code and return the result."""
        interpreter = CodeInterpreter()
        return interpreter.execute(
            self.code,
            self.language,
            self.additional_files,
            self.environment
        ) 