from sentence_transformers import SentenceTransformer, util

def load_model():
    # Initialize embedding model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return model