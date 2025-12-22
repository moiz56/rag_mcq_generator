from argparse import ArgumentParser
import regex as re
import os
import json

from chunking.create_chunks import chunk_pipeline
from chunking.constants import MATH_11_CHAPTERS
from chunking.blueprint import build_blueprint, print_blueprint
from utility import load_index,load_chunks
from retrieval.hybrid_retrieval import retrieve_chunks
from model.embedding_model import load_model 
from model.generate_mcqs import generate_valid_mcqs
from validation_suites.uniqueness import check_semantic_uniqueness
from validation_suites.distractors import critique_distractors

def main():
    parser = ArgumentParser(description="Main pipeline code")

    parser.add_argument(
        "--file_path",
        type=str,
        default= "markdown\MATH 11.md",   # raw string for Windows paths
        help="Path to the markdown file to read",
    )
    
    parser.add_argument(
        "--query",
        type=str,
        default= "questions about 3.1 about quadratic functions",
        help="Query to retrieve relevant chunks."
    )
    

    args = parser.parse_args()
    file_path = args.file_path

    chunks = chunk_pipeline(MATH_11_CHAPTERS, file_path)
    print(f"Created {len(chunks)} chunks")
    
    blueprint = build_blueprint(chunks)
    
    chunks = load_chunks("embeddings\math11.json")
    
    index = load_index("index\syllabus.index")
    
    query = args.query
    model = load_model()
    
    top_chunks = retrieve_chunks(query, chunks, index, model)

    for c in top_chunks:
        name = c.get('subsection_name') or c.get('section_name') or c.get('chapter_name') or ""
        ids = f"Chapter: {c.get('chapter_id', '')}, Section: {c.get('section_id', '')}, Subsection: {c.get('subsection_id', '')}"
        print(f"Chunk {c['chunk_index']}: {name} | {ids}")


    _, mcq_objects = generate_valid_mcqs(top_chunks,query,"medium")

    # Convert each MCQ to a dict and pretty-print
    
    mcq_dicts = [mcq.dict() for mcq in mcq_objects]
    
    # validated_mcqs = check_semantic_uniqueness(mcq_dicts, threshold=0.8)

    # for mcq in validated_mcqs:
    #     print(mcq["question"])
    #     print("Valid uniqueness:", mcq["valid_uniqueness"])
    #     print("Issues:", mcq["issues"])
    #     print()
    
    # critiques = critique_distractors(mcq_dicts)

    # for mcq, critique in zip(mcq_dicts, critiques):
    #     mcq["distractor_critique"] = critique
    #     print(mcq)
        
    print(json.dumps(mcq_dicts, indent=4))


if __name__ == "__main__":
    main()
