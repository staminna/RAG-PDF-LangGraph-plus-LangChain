"""RAG agent implementation using LangGraph."""
import os
from typing import Dict, List, Optional
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langgraph.graph import StateGraph
from dotenv import load_dotenv

from rag_app.utils.state import RAGState
from rag_app.utils.nodes import retrieve, generate
from rag_app.utils.tools import split_documents

# Set environment variable to avoid tokenizer warnings
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Load environment variables
load_dotenv()

# Initialize embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Initialize vector store
vectorstore = Chroma(
    persist_directory="./data",
    embedding_function=embeddings
)

def create_graph() -> StateGraph:
    """Create the RAG graph."""
    # Create the graph
    workflow = StateGraph(RAGState)

    # Add nodes
    workflow.add_node("retrieve", lambda state: retrieve(state, vectorstore))
    workflow.add_node("generate", generate)

    # Add edges
    workflow.add_edge("retrieve", "generate")

    # Set entry point
    workflow.set_entry_point("retrieve")

    return workflow

# Create and compile the graph
graph = create_graph()
app = graph.compile()

def ingest_documents(documents: List[Document]) -> None:
    """Ingest documents into the vector store."""
    # Split documents into chunks
    chunks = split_documents(documents)
    
    # Add chunks to vector store
    vectorstore.add_documents(chunks)
    # No need to call persist() as Chroma 0.4.x automatically persists

def process_query(query: str) -> str:
    """Process a query through the RAG pipeline."""
    state: RAGState = {"query": query, "context": None, "response": None}
    final_state = app.invoke(state)
    return final_state["response"] 