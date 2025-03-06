"""State definition for the RAG graph."""
from typing import Dict, List, TypedDict, Optional
from langchain_core.documents import Document


class RAGState(TypedDict):
    """State for the RAG graph."""
    
    query: str
    """The user query."""
    
    context: Optional[List[Document]]
    """Retrieved documents."""
    
    response: Optional[str]
    """Generated response.""" 