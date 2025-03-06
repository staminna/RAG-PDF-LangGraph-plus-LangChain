# LangGraph RAG Application

This is a Retrieval-Augmented Generation (RAG) application built using LangGraph and LangChain.

## Project Structure

```
rag_app/
├── utils/                # Utilities for the graph
│   ├── __init__.py
│   ├── tools.py          # Tools for document loading and processing
│   ├── nodes.py          # Node functions for the graph
│   └── state.py          # State definition for the graph
├── __init__.py
├── agent.py              # Graph construction code
└── cli.py                # Command-line interface
```

## Setup

### Local Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install the package in development mode:
```bash
pip install -e .
```

3. Create a `.env` file with your API keys (if needed):
```
HUGGINGFACEHUB_API_TOKEN=your_token_here
```

4. Create a `data` directory for storing your documents:
```bash
mkdir -p data
```

### Using Docker

1. Build and start the Docker container:
```bash
docker-compose up -d
```

2. Stop the container:
```bash
docker-compose down
```

## Usage

### Command-line Interface

Process a local PDF file:
```bash
rag-app file path/to/your/file.pdf --query "Your query here"
```

Process a PDF from a URL:
```bash
rag-app url "https://example.com/document.pdf" --query "Your query here"
```

If you don't provide a query, the system will run default queries to summarize the document.

### LangGraph Server

Start the LangGraph server:
```bash
langgraph serve -t rag
```

Or using Docker:
```bash
docker-compose up -d
```

Then you can interact with the server using HTTP requests:
```bash
curl -X POST http://localhost:8000/rag/invoke \
  -H "Content-Type: application/json" \
  -d '{"query": "What is systems engineering?"}'
```

## Development

### Running Tests

```bash
pytest
```

### Building the Package

```bash
python setup.py sdist bdist_wheel
```

## License

MIT