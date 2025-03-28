from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json

# Load cleaned data
with open("college_scraper/cleaned_data.json", "r", encoding="utf-8") as f:
    documents = json.load(f)

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Generate embeddings
texts = [doc["text"] for doc in documents]
embeddings = model.encode(texts, convert_to_numpy=True)

# Store in FAISS
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(np.array(embeddings))

# Save index
faiss.write_index(index, "faiss_index.bin")

# Save metadata (mapping index to URLs)
metadata = [{"url": doc["url"], "text": doc["text"]} for doc in documents]
with open("metadata.json", "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=4)
