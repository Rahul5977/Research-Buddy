from .state import GraphState
from ..utils import parser
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
def parse_document_node(state: GraphState)->GraphState:
    print("---NODE: Parsing Document---")
    state["parsed_data"] = parser.parse_pdf_with_grobid(state["new_document_path"])
    state["new_document_path"] = None
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