import json
import argparse
from tqdm import tqdm
from pathlib import Path
from model.embedding_model import load_model
from utility import load_chunks


def embed_chunks(chunks, model, normalize=True):
    """
    Embeds each chunk's 'content' using the provided SentenceTransformer model.
    
    Args:
        chunks (list): List of chunk dictionaries.
        model: Loaded SentenceTransformer model.
        normalize (bool): Whether to normalize embeddings (recommended for BGE models).

    Returns:
        List of updated chunks with 'embedding' field added.
    """
    for chunk in tqdm(chunks, desc="Embedding chunks"):
        text_to_embed = chunk["content"]
        emb = model.encode(
            text_to_embed,
            convert_to_numpy=True,
            normalize_embeddings=normalize
        )
        chunk["embedding"] = emb.tolist()
    
    return chunks


def main():
    parser = argparse.ArgumentParser(description="Generate MCQs from chunked content.")
    parser.add_argument(
        "--chunks",
        type=str,
        required=True,
        help="Path to the chunks JSON or JSONL file."
    )

    args = parser.parse_args()
    chunks_path = Path(args.chunks)

    if not chunks_path.exists():
        print(f"File not found: {chunks_path}")
        return

    print("Loading chunks...")
    chunks = load_chunks(chunks_path)

    model = load_model()
    
    chunks = embed_chunks(chunks,model)


if __name__ == "__main__":
    main()
