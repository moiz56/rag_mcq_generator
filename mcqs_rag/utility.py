import json
import os
import faiss

def load_chunks(path):
    """
    Loads a chunks JSON file and returns the list of chunk dicts.
    
    Args:
        path (str): Path to the chunks JSON file.
    
    Returns:
        list: List of chunk dictionaries.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Chunks file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("Invalid chunks file: expected a list of chunk objects.")

    # Validate minimal fields
    for idx, chunk in enumerate(data):
        if "content" not in chunk:
            raise ValueError(f"Chunk at index {idx} missing required field: 'content'")

    return data

def load_index(path):
    """
    Loads a FAISS index from the specified path.
    
    Args:
        path (str): Path to the FAISS index file.
    """
    
    index = faiss.read_index(path)
    
    return index

    
    