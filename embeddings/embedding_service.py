
# BEGIN CODE
from sentence_transformers import SentenceTransformer
import json
from tqdm import tqdm

model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_text(text, model):
    # Use model.encode(text) to get the embedding
    embedding = model.encode(text)
    return embedding

def embed_all_chunks(input_file, output_file, model):

    # 1. Load chunks from input_file
    with open(input_file, "r", encoding="utf-8") as f:
        chunks = json.load(f)
    # 2. Loop through chunks, embed each chunk's 'content'
    for chunk in tqdm(chunks, desc="Embedding chunks"):
        text = chunk['content']
        embedding = embed_text(text, model)
         # Convert to list for JSON serialization
        chunk['embedding'] = embedding.tolist()
    # 4. Save to output_file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)
    # 5. Print progress
    print(f"Saved embeddings for {len(chunks)} chunks to {output_file}")

# TEST
if __name__ == "__main__":
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    embed_all_chunks(
        input_file="data/processed/chunks.json",
        output_file="data/processed/chunks_with_embeddings.json",
        model=model
    )
