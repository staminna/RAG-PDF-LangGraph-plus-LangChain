"""Command-line interface for the RAG application."""
import os
import sys
import argparse
from typing import List, Optional

from rag_app.agent import ingest_documents, process_query
from rag_app.utils.tools import load_pdf_from_path, load_pdf_from_url


def process_pdf(pdf_path: str, is_url: bool = False, query: Optional[str] = None) -> None:
    """Process a PDF file and run queries against it."""
    try:
        # Load documents
        if is_url:
            print(f"Loading PDF from URL: {pdf_path}")
            documents = load_pdf_from_url(pdf_path)
        else:
            print(f"Loading PDF from file: {pdf_path}")
            documents = load_pdf_from_path(pdf_path)
        
        print(f"Loaded {len(documents)} pages")
        
        # Ingest documents
        print(f"Ingesting {len(documents)} documents...")
        ingest_documents(documents)
        print("Documents ingested successfully!")
        
        # Process queries
        if query:
            queries = [query]
        else:
            # Default example queries
            queries = [
                "Summarize the key points from this document",
                "What are the main topics covered in this document?",
                "What are the most important concepts in this document?"
            ]
        
        for q in queries:
            print(f"\nQuery: {q}")
            try:
                response = process_query(q)
                print(f"Response: {response}")
            except Exception as e:
                print(f"Error processing query: {e}")
                
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def main() -> None:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description="RAG application for PDF documents")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # File command
    file_parser = subparsers.add_parser("file", help="Process a local PDF file")
    file_parser.add_argument("path", help="Path to the PDF file")
    file_parser.add_argument("--query", "-q", help="Custom query to run")
    
    # URL command
    url_parser = subparsers.add_parser("url", help="Process a PDF from a URL")
    url_parser.add_argument("url", help="URL of the PDF file")
    url_parser.add_argument("--query", "-q", help="Custom query to run")
    
    args = parser.parse_args()
    
    if args.command == "file":
        process_pdf(args.path, is_url=False, query=args.query)
    elif args.command == "url":
        process_pdf(args.url, is_url=True, query=args.query)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main() 