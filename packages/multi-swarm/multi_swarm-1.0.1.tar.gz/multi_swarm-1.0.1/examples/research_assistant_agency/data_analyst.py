from multi_swarm import Agent
from typing import Dict, Any, List
import json

class DataAnalyst(Agent):
    """
    Data Analyst Agent
    
    Responsible for:
    - Analyzing data using Python/R
    - Generating visualizations
    - Running statistical tests
    - Processing numerical data
    """
    
    def __init__(self, storage_path: str = "./storage/data_analyst"):
        super().__init__(
            name="Data Analyst",
            description="Analyzes data and generates insights",
            instructions="./instructions/data_analyst.md",
            tools_folder="./tools/data_analyst",
            llm_provider="claude",
            provider_config={
                "model": "claude-3-sonnet",
                "max_tokens": 4096
            },
            temperature=0.7,
            storage_path=storage_path,
            use_file_storage=True,  # For storing datasets and results
            use_rag=True,  # For maintaining analysis context
            use_code_interpreter=True  # For running analysis code
        )
    
    def analyze_dataset(
        self,
        thread_id: str,
        dataset_path: str,
        analysis_type: str,
        parameters: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Analyze a dataset using the code interpreter.
        
        Args:
            thread_id: ID of the research thread
            dataset_path: Path to the dataset file
            analysis_type: Type of analysis to perform
            parameters: Additional parameters for the analysis
        """
        # Load dataset
        with open(dataset_path, 'r') as f:
            dataset_content = f.read()
        
        # Store dataset in file manager
        dataset_file = self.upload_file(
            dataset_content,
            filename=f"dataset_{thread_id}.csv",
            purpose="analysis_input",
            metadata={
                "thread_id": thread_id,
                "analysis_type": analysis_type
            }
        )
        
        # Generate analysis code based on type
        code = self._generate_analysis_code(
            dataset_path=f"/workspace/{dataset_file.filename}",
            analysis_type=analysis_type,
            parameters=parameters
        )
        
        # Execute analysis
        result = self.execute_code(
            code=code,
            language="python",
            additional_files={
                dataset_file.filename: dataset_content
            }
        )
        
        # Parse and store results
        try:
            analysis_results = json.loads(result.output)
        except:
            analysis_results = {
                "raw_output": result.output,
                "error": result.error
            }
        
        # Store results in knowledge base
        self.add_to_knowledge(
            f"Analysis Results for Thread {thread_id}:\n" +
            f"Analysis Type: {analysis_type}\n" +
            f"Parameters: {parameters}\n" +
            f"Results: {json.dumps(analysis_results, indent=2)}"
        )
        
        return analysis_results
    
    def _generate_analysis_code(
        self,
        dataset_path: str,
        analysis_type: str,
        parameters: Dict[str, Any] = None
    ) -> str:
        """Generate Python code for the analysis."""
        code_templates = {
            "descriptive": """
                import pandas as pd
                import json
                
                # Load dataset
                df = pd.read_csv("{dataset_path}")
                
                # Compute descriptive statistics
                stats = df.describe().to_dict()
                
                # Add additional metrics
                stats.update({{
                    "missing_values": df.isnull().sum().to_dict(),
                    "data_types": df.dtypes.astype(str).to_dict()
                }})
                
                print(json.dumps(stats))
            """,
            
            "correlation": """
                import pandas as pd
                import json
                
                # Load dataset
                df = pd.read_csv("{dataset_path}")
                
                # Compute correlation matrix
                corr_matrix = df.corr().to_dict()
                
                print(json.dumps(corr_matrix))
            """,
            
            "clustering": """
                import pandas as pd
                import numpy as np
                from sklearn.cluster import KMeans
                import json
                
                # Load dataset
                df = pd.read_csv("{dataset_path}")
                
                # Prepare data
                X = df.select_dtypes(include=[np.number]).dropna()
                
                # Perform clustering
                n_clusters = {n_clusters}
                kmeans = KMeans(n_clusters=n_clusters, random_state=42)
                clusters = kmeans.fit_predict(X)
                
                # Prepare results
                results = {{
                    "cluster_centers": kmeans.cluster_centers_.tolist(),
                    "cluster_labels": clusters.tolist(),
                    "inertia": float(kmeans.inertia_)
                }}
                
                print(json.dumps(results))
            """
        }
        
        if analysis_type not in code_templates:
            raise ValueError(f"Unsupported analysis type: {analysis_type}")
        
        # Get base template
        template = code_templates[analysis_type]
        
        # Fill in parameters
        params = {
            "dataset_path": dataset_path,
            "n_clusters": parameters.get("n_clusters", 3) if parameters else 3
        }
        
        return template.format(**params)
    
    def visualize_results(
        self,
        thread_id: str,
        results: Dict[str, Any],
        plot_type: str
    ) -> str:
        """
        Generate visualizations for analysis results.
        
        Args:
            thread_id: ID of the research thread
            results: Analysis results to visualize
            plot_type: Type of plot to generate
        """
        # Generate visualization code
        code = f"""
            import pandas as pd
            import matplotlib.pyplot as plt
            import seaborn as sns
            import json
            
            # Set style
            plt.style.use('seaborn')
            
            # Create figure
            plt.figure(figsize=(10, 6))
            
            # Load results
            data = {json.dumps(results)}
            
            # Create plot
            if "{plot_type}" == "heatmap":
                sns.heatmap(pd.DataFrame(data), annot=True, cmap='coolwarm')
                plt.title("Correlation Heatmap")
            elif "{plot_type}" == "scatter":
                # Assuming 2D data
                x = data.get("x", range(len(data)))
                y = data.get("y", data)
                plt.scatter(x, y)
                plt.title("Scatter Plot")
            
            # Save plot
            plt.savefig('/workspace/plot.png')
            
            print(json.dumps({{"status": "success"}}))
        """
        
        # Execute visualization code
        result = self.execute_code(
            code=code,
            language="python"
        )
        
        # Store visualization
        if result.status == "success":
            with open("/workspace/plot.png", 'rb') as f:
                viz_file = self.upload_file(
                    f,
                    filename=f"visualization_{thread_id}.png",
                    purpose="analysis_output",
                    metadata={
                        "thread_id": thread_id,
                        "plot_type": plot_type
                    }
                )
            return viz_file.id
        
        raise RuntimeError(f"Failed to generate visualization: {result.error}")
    
    def get_analysis_history(self, thread_id: str) -> List[Dict[str, Any]]:
        """Get history of analyses for a thread."""
        results = self.search_knowledge(
            f"analysis results thread:{thread_id}",
            k=20
        )
        
        return [{
            "content": r.document.content,
            "score": r.score,
            "created_at": r.document.created_at
        } for r in results] 