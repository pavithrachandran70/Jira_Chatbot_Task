# agents/state.py
from typing import TypedDict, Dict, Any

class State(TypedDict, total=False):
    user_input: str
    structured_query: Dict[str, Any]
    jira_data: str
    retrieved_visualization_data: Any
    visualization_path: str
