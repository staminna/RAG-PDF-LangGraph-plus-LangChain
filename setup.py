"""Setup script for the rag_app package."""
from setuptools import setup, find_packages

setup(
    name="rag_app",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "langchain>=0.1.0",
        "langgraph>=0.0.10",
        "chromadb>=0.4.22",
        "python-dotenv>=1.0.0",
        "langchain_community>=0.3.19",
        "sentence-transformers>=2.2.2",
        "transformers>=4.37.2",
        "torch>=2.2.0",
        "langchain-core>=0.1.0",
        "pypdf>=3.15.1",
        "requests>=2.31.0",
    ],
    entry_points={
        "console_scripts": [
            "rag-app=rag_app.cli:main",
        ],
    },
) 