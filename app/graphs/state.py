from typing import Dict,TypedDict,Optional

class GraphState(TypedDict):
    """ The master state for the entire application. """
    job_id: Optional[str]
    current_mode: str 
    #  "idle", "processing", "chatting", "error"

    # Inputs from the user
    new_document_path: Optional[str]
    user_query: Optional[str]

    # Data from the processing pipeline
    parsed_data: Optional[Dict]
    rag_collection_name: Optional[str]
    summary: Optional[str]
    knowledge_graph: Optional[Dict]
    chat_history: Optional[Dict]
    chatbot_response: Optional[str]
    error_message: Optional[str]
    
    # Outputs
    booklet_path: Optional[str]
    chatbot_response: Optional[str]
    error_message: Optional[str]
    