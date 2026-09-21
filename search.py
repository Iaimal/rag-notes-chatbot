# search.py
import os
from sentence_transformers import SentenceTransformer, util
import numpy as np

MIN_SCORE = 0.2
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

def chunk_text(text, max_chars=500, overlap=50):
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    for para in paragraphs:
        if len(para) <= max_chars:
            chunks.append(para)
        else:
            start = 0
            while start < len(para):
                end = start + max_chars
                chunks.append(para[start:end])
                start += max_chars - overlap
    return chunks

def load_and_chunk_notes(folder="notes"):
    all_chunks = []
    all_sources = []
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            filepath = os.path.join(folder, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
            chunks = chunk_text(text)
            all_chunks.extend(chunks)
            all_sources.extend([filename] * len(chunks))
    return all_chunks, all_sources

chunks, sources = load_and_chunk_notes()
chunk_embeddings = embed_model.encode(chunks)

def search(query):
    query_embedding = embed_model.encode(query)
    scores = util.cos_sim(query_embedding, chunk_embeddings)
    best_idx = int(np.argmax(scores))
    return sources[best_idx], chunks[best_idx], scores[0][best_idx].item()