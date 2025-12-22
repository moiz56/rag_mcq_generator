# model_cache.py
from model.embedding_model import load_model as load_embedding_model

_model = None

def get_model():
    global _model
    if _model is None:
        print("Loading embedding model (cached)...")
        _model = load_embedding_model()
    return _model
