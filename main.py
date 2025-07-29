from typing import TypedDict,List,Dict

class State(TypedDict):
    """
    Represents the state of the research process, shared across all nodes.
    """
    # --- Input & Core Document Data ---
    file_path: str  
    raw_text: str 
    text_chunks: List[Dict] # List of dictionaries, each with 'content', 'metadata' (e.g., page, section)
    
    
    