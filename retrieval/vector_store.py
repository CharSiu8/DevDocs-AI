
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
