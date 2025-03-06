# LangGraph RAG Project

This is a Retrieval-Augmented Generation (RAG) project built using LangGraph and LangChain.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your API keys (if needed):
```
HUGGINGFACEHUB_API_TOKEN=your_token_here
```

4. Create a `data` directory for storing your documents:
```bash
mkdir data
```

## Usage

### Process a Local PDF File

```bash
python pdf_loader.py path/to/your/file.pdf "Your query here"
```

If you don't provide a query, the system will run default queries to summarize the document.

### Process a PDF from a URL

```bash
python url_loader.py "https://example.com/document.pdf" "Your query here"
```

**Note:** When using URLs with special characters (like `!`), make sure to enclose the URL in quotes.

Example:
```bash
python url_loader.py "https://sebokwiki.org/w/images/sebokwiki-farm!w/5/5c/Guide_to_the_Systems_Engineering_Body_of_Knowledge_v2.11.pdf" "What is systems engineering?"
```

## Project Structure

- `rag.py`: Main implementation of the RAG pipeline using LangGraph
- `pdf_loader.py`: Script for loading and processing local PDF files
- `url_loader.py`: Script for downloading and processing PDFs from URLs
- `requirements.txt`: Project dependencies
- `data/`: Directory for storing document embeddings
- `.env`: Environment variables (create this file with your API keys)

## How it Works

1. The system uses a vector store (ChromaDB) to store and retrieve relevant documents
2. When a query is received, the system:
   - Retrieves relevant documents based on the query
   - Uses the retrieved context to generate a response
   - Returns the generated response with full document content and metadata