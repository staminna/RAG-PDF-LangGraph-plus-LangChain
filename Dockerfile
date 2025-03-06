FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY setup.py .
COPY rag_app ./rag_app

# Install the package
RUN pip install --no-cache-dir -e .

# Create data directory
RUN mkdir -p data

# Copy configuration files
COPY langgraph.json .
COPY .env .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV TOKENIZERS_PARALLELISM=false

# Expose the port for LangGraph server
EXPOSE 8000

# Command to run the LangGraph server
CMD ["langgraph", "serve", "-t", "rag", "--host", "0.0.0.0", "--port", "8000"] 