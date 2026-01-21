# BEGIN CODE

import chromadb
import json
from tqdm import tqdm # i love progress bars
from sentence_transformers import SentenceTransformer

def create_vector_store(input_file, db_path, collection_name):
    with open(input_file, "r", encoding="utf-8") as f:
        chunks = json.load(f)
    # 2. Create ChromaDB client with db_path
    client = chromadb.PersistentClient(path=db_path)
    # 3. Create or get collection
    collection = client.get_or_create_collection(collection_name)
    # 4. Loop through chunks and add to collection
    for chunk in tqdm(chunks, desc="Adding chunks to vector store"):
        collection.add(
            ids=[chunk['chunk_id']],
            embeddings=[chunk['embedding']],
            documents=[chunk['content']],
            metadatas=[chunk['metadata']],
            
        )
    print(f"Added {len(chunks)} chunks to collection '{collection_name}'")

def search(query, db_path, collection_name, n_results=5):
    # 1. Open ChromaDB client and collection
    client = chromadb.PersistentClient(path=db_path)
    collection = client.get_or_create_collection(collection_name)
    # 2. Embed the query (need to load the model)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_embedding = model.encode(query).tolist()
    # 3. Search: collection.query(query_embeddings=[...], n_results=n_results)
    results = collection.query(
        query_embeddings = [query_embedding],
        n_results = n_results
    )
    # 4. Return results
    return results

#    
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
