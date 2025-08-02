from .state import GraphState
from langgraph.graph import StateGraph,END
from . import processing_nodes,chat_nodes, error_nodes

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

def start_processing_node(state: GraphState)->GraphState:
    state["current_mode"] = "processing"
    return state

workflow=StateGraph(GraphState)
# processing nodes
workflow.add_node("start_workflow",start_workflow_node)
workflow.add_node("wait_for_input",wait_for_input_node)
workflow.add_node("parse_document",processing_nodes.parse_document_node)
workflow.add_node("chunk_and_embed",processing_nodes.chunk_and_embed_node)
workflow.add_node("summary",processing_nodes.summary_node)
workflow.add_node("citations",processing_nodes.citations)
workflow.add_node("visualizer",processing_nodes.visualizer)
workflow.add_node("compile_booklet",processing_nodes.compile_booklet_node)

# chat nodes
workflow.add_node("chatbot",chat_nodes.chatbot_node)
workflow.add_node("chatbot_response",chat_nodes.chatbot_response_node)

# handle errors nodes
workflow.add_node("handle_error",error_nodes.handle_error_node)

# edges
workflow.set_entry_point("start_workflow")
workflow.add_edge("start_workflow","wait_for_input")

# Conditional entry into the processing pipeline or chat
workflow.add_conditional_edges(
    "wait_for_input",
    lambda s: "start_processing" if s.get("new_document_path") else ("chatbot" if s.get("user_query") else "wait_for_input"),
    {
        "start_processing": "start_processing",
        "chatbot": "chatbot",
        "wait_for_input": "wait_for_input"
    }
)

# error handleing 
def add_checked_edge(from_node,to_node):
    def check_error(state: GraphState)->str:
        return "handle_error" if state.get("error_message") else to_node
    return workflow.add_conditional_edges(from_node,check_error,{"handle_error":"handle_error",to_node:to_node})


app=workflow.compile()



