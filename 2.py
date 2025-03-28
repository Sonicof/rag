from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import json

print("Starting RAG model setup...")

# Load metadata
with open("metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

# Load FAISS index
faiss_index_path = "faiss_index.bin"
if os.path.exists(faiss_index_path):
    print("Loading FAISS index...")
    faiss_index = faiss.read_index(faiss_index_path)
else:
    raise FileNotFoundError("FAISS index file not found.")

# Load Sentence Transformer for embeddings
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# Load OPT model and tokenizer
model_name = "facebook/opt-350m"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    torch_dtype=torch.float16,
    low_cpu_mem_usage=True
)

# Text generation pipeline
pipe = pipeline(
    "text-generation", 
    model=model, 
    tokenizer=tokenizer,
    max_length=512,  # Increased for longer responses
    temperature=0.7,
    top_p=0.9,
    top_k=40,
    do_sample=True,
    num_return_sequences=1,
    pad_token_id=tokenizer.eos_token_id,
    repetition_penalty=1.2,
    no_repeat_ngram_size=3,
    early_stopping=True
)

def retrieve_documents(query, top_k=3):
    """Retrieve top_k documents from FAISS index."""
    query_embedding = embed_model.encode(query, normalize_embeddings=True)
    query_embedding = np.expand_dims(query_embedding, axis=0)
    _, indices = faiss_index.search(query_embedding, top_k)
    return [metadata[idx]["text"] for idx in indices[0]]

def generate_response(query, documents):
    """Generate a response using the retrieved documents."""
    context = "\n\n".join(documents)
    prompt = f"""Based on the following context, please answer the question. If the answer cannot be found in the context, say so.

Context:
{context}

Question: {query}

Answer:"""
    
    response = pipe(prompt, max_length=512)
    return response[0]['generated_text']

# Interactive chat loop
print("\nRAG Chatbot is ready! Type 'quit' to exit.")
while True:
    query = input("\nYour question: ")
    if query.lower() == 'quit':
        break
    
    print("\nRetrieving relevant documents...")
    retrieved_docs = retrieve_documents(query)
    
    print("\nGenerating response...")
    response = generate_response(query, retrieved_docs)
    
    print("\nResponse:", response)
