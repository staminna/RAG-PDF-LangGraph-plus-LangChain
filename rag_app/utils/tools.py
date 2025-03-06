"""Utility functions for document loading and processing."""
import os
import tempfile
import requests
from urllib.parse import quote
from typing import List, Optional
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter


def load_pdf_from_path(pdf_path: str) -> List[Document]:
    """Load a PDF file from a local path and return the documents."""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found at {pdf_path}")
    
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    return documents


def download_pdf(url: str) -> Optional[str]:
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


def load_pdf_from_url(url: str) -> List[Document]:
    """Download and load a PDF from a URL."""
    pdf_path = download_pdf(url)
    if not pdf_path:
        raise ValueError(f"Failed to download PDF from {url}")
    
    try:
        documents = load_pdf_from_path(pdf_path)
        return documents
    finally:
        # Clean up the temporary file
        if os.path.exists(pdf_path):
            os.remove(pdf_path)


def split_documents(documents: List[Document], chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:
    """Split documents into chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    return text_splitter.split_documents(documents) 