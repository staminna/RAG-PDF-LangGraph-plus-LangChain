from langchain_core.documents import Document
from rag import ingest_documents, process_query

# Example documents
documents = [
    Document(
        page_content="Paris is the capital of France. It is known for its iconic Eiffel Tower and rich cultural heritage.",
        metadata={"source": "france_info"}
    ),
    Document(
        page_content="The Louvre Museum in Paris houses the famous Mona Lisa painting and is one of the world's largest museums.",
        metadata={"source": "france_info"}
    ),
    Document(
        page_content="The Eiffel Tower was completed in 1889 and is one of the most recognizable landmarks in the world.",
        metadata={"source": "france_info"}
    )
]

def main():
    # Ingest documents
    print("Ingesting documents...")
    ingest_documents(documents)
    
    # Example queries
    queries = [
        "What is the capital of France?",
        "Tell me about the Louvre Museum.",
        "When was the Eiffel Tower completed?"
    ]
    
    # Process queries
    for query in queries:
        print(f"\nQuery: {query}")
        response = process_query(query)
        print(f"Response: {response}")

if __name__ == "__main__":
    main() 