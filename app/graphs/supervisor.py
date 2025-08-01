from .state import GraphState
from langgraph.graph import StateGraph,END
from . import processing_nodes

def supervisor_router(state: GraphState)->str:
    """Supervisor for the GraphState"""
    
    print(f"------Supervisor is running : Current state:{state['current_mode']}-----")
    
    if state['error_message']:
        return "handele error"
    
    if state["current_mode"] == "idle":
        if state["new_document_path"]:
            print("Supervisor: New document detected. Routing to processing pipeline.")
            return "processing_pipeline"
        else:
            return "wait_for_input" # A loop back to the supervisor
    elif state["current_mode"] == "chatting":
        if state["user_query"]:
            print("Supervisor: User query detected. Routing to chatbot.")
            return "chatbot"
        else:
            return "wait_for_input"
    return "wait_for_input"

# dummy graph
def start_workflow_node(state: GraphState)->GraphState:
    state["current_mode"] = "idle"
    state["error_message"]=None
    print(f"------Starting workflow----- mode set to idle")
    return state

def wait_for_input_node(state: GraphState)->GraphState:
    print("------Waiting for input-----")
    return state

workflow=StateGraph(GraphState)
workflow.add_node("start_workflow",start_workflow_node)
workflow.add_node("wait_for_input",wait_for_input_node)
workflow.add_node("parse_document",processing_nodes.parse_document_node)
workflow.add_node("chunk_and_embed",processing_nodes.chunk_and_embed_node)



workflow.set_entry_point("start_workflow")
workflow.add_edge("start_workflow","wait_for_input")

workflow.add_conditional_edges(
    "wait_for_input",
    supervisor_router,
    {
        "wait_for_input": "wait_for_input",
        "processing_pipeline": "parse_document",
    }
)
workflow.add_edge("parse_document","chunk_and_embed")
workflow.add_edge("chunk_and_embed", "wait_for_input")
app=workflow.compile()



