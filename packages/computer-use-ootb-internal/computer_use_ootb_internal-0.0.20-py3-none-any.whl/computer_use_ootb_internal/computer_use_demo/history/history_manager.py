import os
import re
import json
from typing import List, Dict, Optional

class HistoryManager:
    def __init__(self, base_path: str = r"./computer_use_demo/ootbdatabase"):
        """
        初始化历史记录管理器
        
        Args:
            base_path (str): 基础路径，默认为'data'
        """
        self.base_path = base_path
        
    def load_trace(self, user_id: str, trace_id: str) -> Optional[Dict]:
        """
        加载指定用户ID和轨迹ID的轨迹信息
        
        Args:
            user_id (str): 用户ID
            trace_id (str): 轨迹ID
            
        Returns:
            Dict: 轨迹信息字典，如果文件不存在则返回None
        """
        file_path = os.path.join(self.base_path, user_id, trace_id, "trace_information.json")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                trace_data = json.load(f)
            return trace_data
        except FileNotFoundError:
            print(f"找不到轨迹文件: {file_path}")
            return None
        except json.JSONDecodeError:
            print(f"JSON解析错误: {file_path}")
            return None
            
    def get_user_traces(self, user_id: str) -> List[str]:
        """
        获取指定用户的所有轨迹ID
        
        Args:
            user_id (str): 用户ID
            
        Returns:
            List[str]: 轨迹ID列表
        """
        user_path = os.path.join(self.base_path, user_id)
        if not os.path.exists(user_path):
            return []
            
        return [d for d in os.listdir(user_path) 
                if os.path.isdir(os.path.join(user_path, d))]
                
    def get_all_users(self) -> List[str]:
        """
        获取所有用户ID
        
        Returns:
            List[str]: 用户ID列表
        """
        if not os.path.exists(self.base_path):
            return []
            
        return [d for d in os.listdir(self.base_path) 
                if os.path.isdir(os.path.join(self.base_path, d))]
                
    def get_trace_summary(self, user_id: str, trace_id: str) -> Optional[Dict]:
        """
        获取轨迹的摘要信息
        
        Args:
            user_id (str): 用户ID
            trace_id (str): 轨迹ID
            
        Returns:
            Dict: 包含任务名称、描述和ID的字典
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
        获取轨迹中的所有动作
        
        Args:
            user_id (str): 用户ID
            trace_id (str): 轨迹ID
            
        Returns:
            List[Dict]: 动作列表
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
        
        # only keep the action description
        steps = trace_data.get("trajectory", [])
        output = []

        for action in steps:
            try:
                # print(action["action_discription"])
                output.append([re.split(r'[\\/]', text)[-1] for text in action["action_discription"]])

            except Exception as e:
                from IPython.core.debugger import set_trace
                set_trace()

        return self.format_json(output) 
    
    def format_json(self, data):
        """
        格式化 JSON 数据，去掉 [ 和 ]，并将每组元素显示在一行。
        """
        result = []
        for ix, group in enumerate(data):
            line = f"{ix+1}: {'| '.join(map(str, group))}"  # 将每组元素转为字符串后用逗号分隔
            result.append(line)
        return "\n".join(result)  # 每组元素作为一行




        
        
