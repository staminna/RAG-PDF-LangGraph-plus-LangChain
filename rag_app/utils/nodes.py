"""Node functions for the RAG graph."""
from typing import Dict, List
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from .state import RAGState


def retrieve(state: RAGState, vectorstore: Chroma) -> RAGState:
    """Retrieve relevant documents based on the query."""
    query = state["query"]
    docs = vectorstore.similarity_search(query, k=3)
    return {"query": query, "context": docs, "response": state.get("response")}


def generate(state: RAGState) -> RAGState:
    """Generate response using the retrieved context."""
    context = state.get("context", [])
    query = state["query"]
    
    # Format context for prompt
    context_text = "\n".join([doc.page_content for doc in context])
    
    # Create a detailed response based on the context
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
    
    if context:
        response += "They cover topics including " + ", ".join([doc.page_content.split('.')[0] for doc in context[:3]]) + ". "
    
    response += "For more specific information, please ask a more targeted question."
    
    return {"query": query, "context": context, "response": response} 