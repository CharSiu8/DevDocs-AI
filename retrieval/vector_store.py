# BEGIN CODE
import os
import json
from dotenv import load_dotenv
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

load_dotenv()

# Connect to PineconeAPIKey
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
# Connect to index
index = pc.Index(host=os.getenv("PINECONE_INDEX_HOST"))

def create_vector_store(input_file, db_path=None, collection_name=None):
    # db_path and collection_name kept for compatibility (unused with Pinecone)

    # 1. Load chunks from input_file (same as before)
    with open(input_file, "r", encoding="utf-8") as f:
    # 2. Loop through chunks in batches of 100
        chunks = json.load(f)
    batch_size = 100
    
    # 3. For each batch, build a list of vectors with format:
    for i in tqdm(range(0, len(chunks), batch_size), desc="Upload to Pinecone"):
        batch = chunks[i:i + batch_size]
        vectors = [
            {
                "id": chunk['chunk_id'],
                "values": chunk['embedding'],
                "metadata": {
                    "content": chunk['content'],
                    **chunk['metadata']
                }
            }
            for chunk in batch
        ]
        index.upsert(vectors=vectors)
    print(f"Uploaded {len(chunks)} chunks to Pinecone")


def search(query, db_path=None, collection_name=None, n_results=5):
    # db_path and collection_name kept for compatibility (unused with Pinecone)
    # 1. Load SentenceTransformer model (same as before)
    model = SentenceTransformer('all-MiniLM-L6-v2')

    query_embedding = model.encode(query).tolist()
   
    # 3. Call index.query(vector=..., top_k=..., include_metadata=True)
    results = index.query(
        vector=query_embedding,
        top_k=n_results,
        include_metadata=True
    )
    # 4. Format results to match existing output:

    documents = [[match['metadata']['content'] for match in results['matches']]]
    metadatas = [[{k: v for k, v in match['metadata'].items() if k != 'content'} for match in results['matches']]]

    return {'documents': documents, 'metadatas': metadatas}

# TEST 
if __name__ == "__main__":
    results = search(
        query="How do I handle errors in FastAPI?",
        db_path="data/vectordb",
        collection_name="fastapi_docs",
        n_results=3
    )
    
    for i, doc in enumerate(results['documents'][0]):
        print(f"\n--- Result {i+1} ---")
        print(doc[:300])


