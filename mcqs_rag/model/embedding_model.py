import torch
from sentence_transformers import SentenceTransformer

_model = None  # cache

def load_model():
    global _model
    
    # Auto-detect GPU, fallback to CPU
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    if _model is None:
        print(f"Loading BGE-M3 model on {device}...")
        _model = SentenceTransformer("BAAI/bge-m3")
    
    return _model

if __name__ == "__main__":
    model = load_model()
    sentences = ["Hello, world!", "This is a test sentence."]
    embeddings = model.encode(sentences)
    print(embeddings)
