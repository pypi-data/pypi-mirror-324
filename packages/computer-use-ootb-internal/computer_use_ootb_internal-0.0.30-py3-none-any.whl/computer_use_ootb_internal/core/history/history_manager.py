import os
import re
import json
from typing import List, Dict, Optional
from importlib import resources, util
from pathlib import Path

class HistoryManager:
    def __init__(self, base_path: str = None):
        """
        Initialize history manager with proper path resolution
        
        Args:
            base_path (str): Base path, if None will try to locate from package
        """
        if base_path is None:
            # Try to find the package location
            try:
                spec = util.find_spec('computer_use_ootb_internal')
                if spec is None or spec.origin is None:
                    raise ImportError("Could not find package location")
                package_root = Path(spec.origin).parent
                self.base_path = str(package_root / 'core' / 'ootbdatabase')
            except Exception as e:
                # Fallback to environment variable if available
                ootb_path = os.getenv("OOTB_PATH")
                if ootb_path:
                    self.base_path = os.path.join(ootb_path, "ootbdatabase")
                else:
                    raise ValueError("Could not determine base path. Please provide base_path or set OOTB_PATH environment variable.")
        else:
            self.base_path = os.path.abspath(base_path)
            
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path, exist_ok=True)
            
        print(f"Using database path: {self.base_path}")

    def load_trace(self, user_id: str, trace_id: str) -> Optional[Dict]:
        """
        Load trace information for specified user ID and trace ID
        
        Args:
            user_id (str): User ID
            trace_id (str): Trace ID
            
        Returns:
            Dict: Trace information dictionary, None if file doesn't exist
        """
        file_path = os.path.join(self.base_path, user_id, trace_id, "trace_information.json")
        file_path = os.path.abspath(file_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                trace_data = json.load(f)
            return trace_data
        except FileNotFoundError:
            print(f"Trace file not found: {file_path}")
            return None
        except json.JSONDecodeError:
            print(f"JSON parsing error: {file_path}")
            return None
            
    def get_user_traces(self, user_id: str) -> List[str]:
        """
        Get all trace IDs for specified user
        
        Args:
            user_id (str): User ID
            
        Returns:
            List[str]: List of trace IDs
        """
        user_path = os.path.join(self.base_path, user_id)
        user_path = os.path.abspath(user_path)
        
        if not os.path.exists(user_path):
            return []
            
        return [d for d in os.listdir(user_path) 
                if os.path.isdir(os.path.join(user_path, d))]
                
    def get_all_users(self) -> List[str]:
        """
        Get all user IDs
        
        Returns:
            List[str]: List of user IDs
        """
        if not os.path.exists(self.base_path):
            return []
            
        return [d for d in os.listdir(self.base_path) 
                if os.path.isdir(os.path.join(self.base_path, d))]
                
    def get_trace_summary(self, user_id: str, trace_id: str) -> Optional[Dict]:
        """
        Get trace summary information
        
        Args:
            user_id (str): User ID
            trace_id (str): Trace ID
            
        Returns:
            Dict: Dictionary containing task name, description and ID
        """
        trace_data = self.load_trace(user_id, trace_id)
        if not trace_data:
            return None
            
        return {
            "taskName": trace_data.get("taskName"),
            "taskDescription": trace_data.get("taskDescription"),
            "taskId": trace_data.get("taskId")
        }
        
    def get_trajectory_actions(self, user_id: str, trace_id: str) -> Optional[List[Dict]]:
        """
        Get all actions in a trace
        
        Args:
            user_id (str): User ID
            trace_id (str): Trace ID
            
        Returns:
            List[Dict]: List of actions
        """
        trace_data = self.load_trace(user_id, trace_id)
        if not trace_data:
            return None
            
        return trace_data.get("trajectory", [])
    
    def get_in_context_example(self, user_id: str, trace_id: str) -> str:
        """
        Get the in-context example for the given user and trace
        """
        trace_data = self.load_trace(user_id, trace_id)
        if not trace_data:
            return None
        
        steps = trace_data.get("trajectory", [])
        output = []

        for action in steps:
            try:
                output.append([re.split(r'[\\/]', text)[-1] for text in action["action_discription"]])
            except Exception as e:
                from IPython.core.debugger import set_trace
                set_trace()

        return self.format_json(output) 
    
    def format_json(self, data):
        """
        Format JSON data, removing [ and ], showing each group on a line
        """
        result = []
        for ix, group in enumerate(data):
            line = f"{ix+1}: {'| '.join(map(str, group))}"
            result.append(line)
        return "\n".join(result)