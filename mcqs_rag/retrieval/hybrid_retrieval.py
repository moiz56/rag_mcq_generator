import re
import numpy as np
from argparse import ArgumentParser
from utility import load_chunks, load_index
from model.embedding_model import load_model

def extract_numbers(query):
    """
    Extract numeric patterns from the query, e.g., 2, 3.1.1, 1.2.3.
    Returns a list of strings.
    """
    pattern = r'\d+(?:\.\d+)*'
    return re.findall(pattern, query)


def filter_by_numbers(chunks, numbers):
    """
    Filter chunks based on numeric patterns in chapter/section/subsection.
    Matches exact IDs and parent hierarchy.
    """
    filtered = []
    for c in chunks:
        chapter_id = str(c.get("chapter_id", ""))
        section_id = str(c.get("section_id", ""))
        subsection_id = str(c.get("subsection_id", ""))

        chunk_numbers = []
        if chapter_id: chunk_numbers.append(chapter_id)
        if section_id: chunk_numbers.append(section_id)
        if subsection_id: chunk_numbers.append(subsection_id)

        hierarchical_numbers = set()
        for num in chunk_numbers:
            parts = num.split(".")
            for i in range(1, len(parts)+1):
                hierarchical_numbers.add(".".join(parts[:i]))

        for num in numbers:
            if num in hierarchical_numbers:
                filtered.append(c)
                break
    return filtered

def retrieve_chunks(query, chunks, index, model, k_dense=10, min_similarity=0.8):
    """
    Perform dense (semantic) and numeric/metadata retrieval in parallel,
    then remove duplicates.
    Only includes dense results above a similarity threshold.
    Returns a list of unique chunks sorted by chunk_index.
    """
    # --- Dense retrieval ---
    query_vec = model.encode([query])
    D, I = index.search(query_vec.reshape(1, -1), k=k_dense)

    dense_results = []
    for i, score in zip(I[0], D[0]):
        if score >= min_similarity:  # apply threshold
            dense_results.append(chunks[i])

    # --- Numeric/metadata retrieval ---
    numbers = extract_numbers(query)
    numeric_results = filter_by_numbers(chunks, numbers) if numbers else []

    # --- Merge & deduplicate by chunk_index ---
    combined = dense_results + numeric_results
    unique_chunks = {c['chunk_index']: c for c in combined}  # deduplicate

    # Convert chunk_index to int for sorting, fallback to 0 if invalid
    def chunk_index_int(c):
        try:
            return int(c['chunk_index'])
        except (ValueError, TypeError):
            return 0

    unique_chunks_list = sorted(unique_chunks.values(), key=chunk_index_int)

    return unique_chunks_list

if __name__ == "__main__":
    
    parser = ArgumentParser(description="Hybrid Retrieval of Chunks based on Query")
    
    parser.add_argument(
        "--chunks_path",
        type=str,
        default="embeddings\math11.json",
        help="Path to the processed chunks JSON file."
    )
    
    parser.add_argument(
        "--index_path",
        type=str,
        default="index\syllabus.index",
        help="Path to the FAISS index file."
    )
    
    parser.add_argument(
        "--query",
        type=str,
        default= "questions about 3.1 about quadratic functions",
        help="Query to retrieve relevant chunks."
    )
    
    args = parser.parse_args()
    
    chunks = load_chunks(args.chunks_path)
    index = load_index(args.index_path)
    query = args.query
    model = load_model()
    
    top_chunks = retrieve_chunks(query, chunks, index, model)

    for c in top_chunks:
        name = c.get('subsection_name') or c.get('section_name') or c.get('chapter_name') or ""
        ids = f"Chapter: {c.get('chapter_id', '')}, Section: {c.get('section_id', '')}, Subsection: {c.get('subsection_id', '')}"
        print(f"Chunk {c['chunk_index']}: {name} | {ids}")
