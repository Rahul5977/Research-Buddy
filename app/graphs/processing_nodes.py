from .state import GraphState
from ..utils import parser
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from agents import summarizer, citations, visualizer, pdf_compiler
def parse_document_node(state: GraphState)->GraphState:
    print("---NODE: Parsing Document---")
    try:
        path=state["new_document_path"]
        state["parsed_data"] = parser.parse_document(path)
    except Exception as e:
       state["error_message"] = f"Failed during PDF parsing: {e}"
    return state

def chunk_and_embed_node(state: GraphState)->GraphState:
    print("---NODE: Chunking and Embedding---")
    job_id = state["job_id"]
    full_text=state["parsed_data"].get("full_text","")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=400)
    chunks = text_splitter.split_text(full_text)
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store_path=f"vector_stores/{job_id}.chroma_db"
    Chroma.from_texts(chunks, embedding_model, collection_name=job_id, persist_directory=vector_store_path)
    state["rag_collection_name"]=vector_store_path
    print(f"---SUCCESS: RAG knowledge base created.---")
    return state

def summary_node(state: GraphState)->GraphState:
    print("---NODE: Creating Summary---")
    full_text=state["parsed_data"].get("full_text","")
    summary=summarizer.summarize_text(full_text)
    state["summary"] = summary
    return state

def citations(state: GraphState)->GraphState:
    print("---NODE: Creating Citations---")
    try:
        state["citations"] = citations.citations(state["summary"])
    except Exception as e:
       state["error_message"] = f"failed to create citations: {e}"
    return state

def visualizer(state: GraphState)->GraphState:
    print("---NODE: Creating Visualizer---")
    try:
        state["diagram_dotcode"] = visualizer.create_diagram_from_text(state["parsed_data"]["full_text"])
    except Exception as e:
       state["error_message"] = f"Failed during visualizer: {e}"
    return state
    
    
def compile_booklet_node(state: GraphState) -> GraphState:
    print("---NODE: Compiling PDF Booklet---")
    try:
        pdf_path = pdf_compiler.compile_booklet_from_data(
            job_id=state["job_id"],
            summary=state["summary"],
            citations=state["citations"],
            dot_code=state["diagram_dot_code"]
        )
        state["booklet_path"] = pdf_path
    except Exception as e:
        state["error_message"] = f"Failed during PDF compilation: {e}"
    return state