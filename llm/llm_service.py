
# BEGIN CODE
from dotenv import load_dotenv
load_dotenv()
import openai
import os

def generate_answer(query, chunks, model="gpt-4o-mini"):
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    context = "\n\n---\n\n".join(chunks)
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You answer questions about FastAPI using only the provided context. Be concise. Cite which section the info comes from when possible. NEVER MAKE UP INFORMATION"
            },
            {
                "role": "user",
                "content": f"Question: {query}\n\nContext:\n{context}"
            }
        ],
        max_tokens=500
    )
    
    return response.choices[0].message.content 
    
# TEST
if __name__ == "__main__":
    from retrieval.vector_store import search
    
    query = "How do I handle errors in FastAPI?"
    
    # Get relevant chunks
    results = search(
        query=query,
        db_path="data/vectordb",
        collection_name="fastapi_docs",
        n_results=3
    )
    chunks = results['documents'][0]
    
    # Generate answer
    answer = generate_answer(query, chunks)
    print(f"Question: {query}\n")
    print(f"Answer: {answer}")
