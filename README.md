# DevDocs-AI v1

RAG system for querying FastAPI documentation with semantic search and LLM-generated answers.

**🔗 Live Demo:** https://charsiu8-devdocs-ai.hf.space/ask?question=How do I create routes

## What it does

Ask questions about FastAPI → get answers with source citations.

Built from scratch: scraper → chunker → embedder → vector store → retrieval → LLM → API

## Stack

- **Embedding**: sentence-transformers (all-MiniLM-L6-v2)
- **Vector DB**: Pinecone
- **LLM**: GPT-4o-mini
- **API**: FastAPI
- **Hosting**: Hugging Face Spaces

## Stats

- 145 pages scraped
- 14,285 chunks
- Sentence-boundary chunking with overlap

## Setup
```bash
pip install -r requirements.txt
```

Create `.env`:
```
OPENAI_API_KEY=your_key_here
PINECONE_API_KEY=your_key_here
PINECONE_INDEX_HOST=your_host_here
```

## Run locally
```bash
uvicorn api.main:app
```

## API
```
GET /ask?question=How do I create routes in FastAPI?
```

Returns:
```json
{
  "question": "...",
  "answer": "...",
  "sources": [...]
}
```

## Project Structure
```
├── api/main.py              # FastAPI endpoint
├── data/scraper.py          # Sitemap scraping
├── data/chunking.py         # Text chunking
├── embeddings/embedding_service.py
├── retrieval/vector_store.py
└── llm/llm_service.py
```

## License

Copyright © 2025 Steven Polino - Portfolio use only. See LICENSE.
