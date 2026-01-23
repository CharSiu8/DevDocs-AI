# BEGIN CODE
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from retrieval.vector_store import search
from llm.llm_service import generate_answer

app = FastAPI(title="DevDocs AI")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return FileResponse("static/index.html")

@app.get("/ask")
def ask(question: str):
    results = search(
        query=question,
        db_path="data/vectordb",
        collection_name="fastapi_docs",
        n_results=3
    )
    chunks = results['documents'][0]
    answer = generate_answer(question, chunks)
    return {
        "question": question,
        "answer": answer,
        "sources": results['metadatas'][0]
    }

@app.get("/health")
def health():
    return {"status": "ok"}
