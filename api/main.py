
# BEGIN CODE
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from retrieval.vector_store import search
from llm.llm_service import generate_answer

app = FastAPI(title="DevDocs AI")

@app.get("/ask")
def ask(question: str):
    # 1. Search for relevant chunks
    results = search(
        query=question,
        db_path="data/vectordb",
        collection_name="fastapi_docs",
        n_results=3
    )
    chunks = results['documents'][0]
    
    # 2. Generate answer
    answer = generate_answer(question, chunks)
    
    # 3. Return answer and sources
    return {
        "question": question,
        "answer": answer,
        "sources": results['metadatas'][0]
    }
    
@app.get("/health")
def health():
    return {"status": "ok"}
