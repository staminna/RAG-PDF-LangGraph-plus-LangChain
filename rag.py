from typing import Dict, List, Tuple
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langgraph.graph import StateGraph
import os
from dotenv import load_dotenv

# Set environment variable to avoid tokenizer warnings
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Load environment variables
load_dotenv()

# Initialize embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Initialize text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len
)

# Initialize vector store
vectorstore = Chroma(
    persist_directory="./data",
    embedding_function=embeddings
)

def retrieve(state: Dict) -> Dict:
    """Retrieve relevant documents based on the query."""
    query = state["query"]
    docs = vectorstore.similarity_search(query, k=3)
    state["context"] = docs
    return state

def generate(state: Dict) -> Dict:
    """Generate response using the retrieved context."""
    context = state["context"]
    query = state["query"]
    
    # Format context for prompt
    context_text = "\n".join([doc.page_content for doc in context])
    
    # Create a more detailed response based on the context
    response = f"Based on the retrieved documents related to '{query}':\n\n"
    
    # Add full content from the context
    for i, doc in enumerate(context, 1):
        # Get metadata if available
        source = doc.metadata.get('source', 'Unknown source')
        page = doc.metadata.get('page', 'Unknown page')
        
        response += f"--- Document {i} (Source: {source}, Page: {page}) ---\n\n"
        response += f"{doc.page_content}\n\n"
    
    # Add a summary section
    response += "--- Summary ---\n\n"
    response += f"The documents above contain information related to '{query}'. "
    response += "They cover topics including " + ", ".join([doc.page_content.split('.')[0] for doc in context[:3]]) + ". "
    response += "For more specific information, please ask a more targeted question."
    
    state["response"] = response
    return state

# Create the graph
workflow = StateGraph(Dict)

# Add nodes
workflow.add_node("retrieve", retrieve)
workflow.add_node("generate", generate)

# Add edges
workflow.add_edge("retrieve", "generate")

# Set entry point
workflow.set_entry_point("retrieve")

# Compile the graph
app = workflow.compile()

def ingest_documents(documents: List[Document]) -> None:
    """Ingest documents into the vector store."""
    # Split documents into chunks
    chunks = text_splitter.split_documents(documents)
    
    # Add chunks to vector store
    vectorstore.add_documents(chunks)
    # No need to call persist() as Chroma 0.4.x automatically persists

def process_query(query: str) -> str:
    """Process a query through the RAG pipeline."""
    state = {"query": query}
    final_state = app.invoke(state)
    return final_state["response"]

if __name__ == "__main__":
    # Example usage
    query = "What is the capital of France?"
    response = process_query(query)
    print(f"Query: {query}")
    print(f"Response: {response}") 