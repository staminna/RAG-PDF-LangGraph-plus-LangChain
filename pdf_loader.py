from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from rag import ingest_documents, process_query
import os
import sys

def load_pdf(pdf_path):
    """Load a PDF file and return the documents."""
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at {pdf_path}")
        return []
    
    try:
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        print(f"Loaded {len(documents)} pages from {pdf_path}")
        return documents
    except Exception as e:
        print(f"Error loading PDF: {e}")
        return []

def main():
    if len(sys.argv) < 2:
        print("Usage: python pdf_loader.py <path_to_pdf> [custom_query]")
        return
    
    pdf_path = sys.argv[1]
    documents = load_pdf(pdf_path)
    
    if not documents:
        print("No documents were loaded. Exiting.")
        return
    
    try:
        print(f"Ingesting {len(documents)} documents...")
        ingest_documents(documents)
        print("Documents ingested successfully!")
        
        # Check if a custom query was provided
        if len(sys.argv) > 2:
            custom_query = " ".join(sys.argv[2:])
            queries = [custom_query]
        else:
            # Default example queries
            queries = [
                "Summarize the key points from this document",
                "What are the main topics covered in this document?",
                "What are the most important concepts in this document?"
            ]
        
        for query in queries:
            print(f"\nQuery: {query}")
            try:
                response = process_query(query)
                print(f"Response: {response}")
            except Exception as e:
                print(f"Error processing query: {e}")
    except Exception as e:
        print(f"Error during document processing: {e}")

if __name__ == "__main__":
    main() 