# BEGIN CODE
def chunk_text(text, chunk_size, overlap):
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        # grab a chunk from start to start + chunk_size
        end = min(start + chunk_size, text_length)
        #sentance boundaires 
        chunk = text[start:end]
        # If we're not at the very end of the text, find the last sentence boundary (. ? !) in the chunk, and cut there instead
        if end < text_length:
            last_period = chunk.rfind('.')
            last_question = chunk.rfind('?')
            last_exclamation = chunk.rfind('!')
            last_boundary = max(last_period, last_question, last_exclamation)
            if last_boundary != -1 and last_boundary > chunk_size * 0.5:
                end = start + last_boundary + 1  # +1 to include the punctuation

        # append it to chunks
        chunks.append(text[start:end])
        # move start forward (chunk_size minus overlap) always by at least one
        new_start = end - overlap
        if new_start <= start:
            new_start = start + 1
        start = new_start
        
    return chunks

def chunk_document(document, chunk_size, overlap):
    doc = {'url': document['url'], 'title': document['title'], 'content': document['content']}
    chunk_texts = chunk_text(doc['content'], chunk_size, overlap)
    chunked_docs = []

    for i, text in enumerate(chunk_texts):
        chunked_doc = {
            'chunk_id': f"{doc['title']}_chunk_{i}",
            'content': text,
            'metadata': {
                'source': doc['url'],
                'title': doc['title'],
                'chunk_index': i,
                'total_chunks': len(chunk_texts)
            }
        }

        chunked_docs.append(chunked_doc)
    return chunked_docs

def chunk_all_docs(input_file, output_file, chunk_size, overlap):
    with open(input_file, "r", encoding="utf-8") as f:
        documents = json.load(f)
    all_chunked_docs = []
    for document in documents:
        chunked_docs = chunk_document(document, chunk_size, overlap)
        all_chunked_docs.extend(chunked_docs)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_chunked_docs, f, ensure_ascii=False, indent=2)
    print(f"Chunked {len(documents)} documents into {len(all_chunked_docs)} chunks.")
#TESTING
if __name__ == "__main__":
    import json
    
    chunk_all_docs(
        input_file="data/raw/fastapi_docs.json",
        output_file="data/processed/chunks.json",
        chunk_size=500,
        overlap=50
    )
