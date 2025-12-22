import faiss
import numpy as np
import os
import argparse 

from utility import load_chunks

def build_index(embedding_path, out_path="index\syllabus.index"):
    chunks = load_chunks(embedding_path)
    assert isinstance(chunks, list), "load_file() should return a list"
    assert len(chunks) > 0, "No chunks loaded from file"

    vectors = np.array([chunk["embedding"] for chunk in chunks], dtype=np.float32)

    assert vectors.ndim == 2, f"Expected 2D array (n, dim), got shape {vectors.shape}"
    assert vectors.shape[0] == len(chunks), "Vector count mismatch"
    assert np.isfinite(vectors).all(), "Found NaN/Inf in embeddings"

    dim = vectors.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(vectors)

    print(f"Built index: ntotal={index.ntotal}, dim={dim}")
    
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    faiss.write_index(index, out_path)
    print(f"Saved index to: {out_path}")

    return index, vectors

if __name__ == "__main__":
    embedding_file = "embeddings\math11.json"
    build_index(embedding_file)
