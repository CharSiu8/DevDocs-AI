FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port 7860 (HF Spaces default)
EXPOSE 7860

# Run the app
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "7860"]
```

**File 2:** Update `requirements.txt` — swap `chromadb` for `pinecone`:
```
# Core API
fastapi==0.109.0
uvicorn[standard]==0.27.0
python-dotenv==1.0.0

# LLM
openai==1.10.0

# Embeddings & Vector Store
sentence-transformers==2.3.1
pinecone

# Scraping (not needed for deployment, but keep for completeness)
requests==2.31.0
beautifulsoup4==4.12.3

# Utilities
tqdm==4.66.1