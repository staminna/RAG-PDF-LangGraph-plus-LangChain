import os
import sys
import requests
import tempfile
import shlex
from urllib.parse import urlparse, quote
from langchain_community.document_loaders import PyPDFLoader
from rag import ingest_documents, process_query

def download_pdf(url):
    """Download a PDF from a URL and save it to a temporary file."""
    try:
        print(f"Downloading PDF from {url}...")
        # Handle URL encoding for special characters
        if '!' in url and not url.startswith('http'):
            # If URL was passed without quotes and has special chars
            url = quote(url, safe=':/?&=')
            
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Check if the content is a PDF
        content_type = response.headers.get('Content-Type', '')
        if 'application/pdf' not in content_type and not url.lower().endswith('.pdf'):
            print(f"Warning: URL might not be a PDF. Content-Type: {content_type}")
        
        # Create a temporary file to store the PDF
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        temp_path = temp_file.name
        
        # Write the PDF content to the temporary file
        with open(temp_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"PDF downloaded and saved to temporary file: {temp_path}")
        return temp_path
    except Exception as e:
        print(f"Error downloading PDF: {e}")
        return None

def load_pdf(pdf_path):
    """Load a PDF file and return the documents."""
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
        print("Usage: python url_loader.py <pdf_url> [custom_query]")
        return
    
    url = sys.argv[1]
    
    # Download the PDF from the URL
    pdf_path = download_pdf(url)
    if not pdf_path:
        print("Failed to download PDF. Exiting.")
        return
    
    try:
        # Load the PDF
        documents = load_pdf(pdf_path)
        
        if not documents:
            print("No documents were loaded. Exiting.")
            return
        
        # Ingest the documents
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
        
        # Process queries
        for query in queries:
            print(f"\nQuery: {query}")
            try:
                response = process_query(query)
                print(f"Response: {response}")
            except Exception as e:
                print(f"Error processing query: {e}")
    except Exception as e:
        print(f"Error during document processing: {e}")
    finally:
        # Clean up the temporary file
        if pdf_path and os.path.exists(pdf_path):
            try:
                os.remove(pdf_path)
                print(f"Temporary file {pdf_path} removed.")
            except Exception as e:
                print(f"Error removing temporary file: {e}")

if __name__ == "__main__":
    main() 