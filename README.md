# DevDocs-AI v1

RAG system for querying FastAPI documentation with semantic search and LLM-generated answers.

## What it does

Ask questions about FastAPI → get answers with source citations.

Built from scratch: scraper → chunker → embedder → vector store → retrieval → LLM → API

## Stack

- **Embedding**: sentence-transformers (all-MiniLM-L6-v2)
- **Vector DB**: ChromaDB
- **LLM**: GPT-4o-mini
- **API**: FastAPI

## Stats

- 145 pages scraped
- 14,285 chunks
- Sentence-boundary chunking with overlap

## Setup
```bash
