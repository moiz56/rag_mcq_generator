from model.semantic_uniqueness_model import load_model
from sentence_transformers import util

def check_semantic_uniqueness(mcq_list, threshold=0.85, verbose=True):
    """
    Flags near-duplicate STEM MCQs using semantic similarity and prints similarity scores.

    Args:
        mcq_list (list of dict): Each dict has keys "question", "A", "B", "C", "D", "correct", etc.
        threshold (float): Cosine similarity threshold above which questions are considered duplicates.
        verbose (bool): If True, prints near-duplicate pairs and their similarity.

    Returns:
        list of dict: Updated MCQs with "valid_uniqueness" and "issues" fields.
    """
    
    model = load_model()
    
    # Generate embeddings for all question stems
    questions = [mcq["question"] for mcq in mcq_list]
    embeddings = model.encode(questions, convert_to_tensor=True)

    n = len(mcq_list)

    # Initialize issues and validity
    for mcq in mcq_list:
        mcq.setdefault("issues", [])
        mcq["valid_uniqueness"] = True

    # Compare each pair for similarity
    for i in range(n):
        for j in range(i + 1, n):
            sim = util.cos_sim(embeddings[i], embeddings[j]).item()
            if sim >= threshold:
                # Flag both questions as near-duplicates
                mcq_list[i]["issues"].append(f"near_duplicate_with_question_{j} (sim={sim:.2f})")
                mcq_list[j]["issues"].append(f"near_duplicate_with_question_{i} (sim={sim:.2f})")
                mcq_list[i]["valid_uniqueness"] = False
                mcq_list[j]["valid_uniqueness"] = False
                if verbose:
                    print(f"Near-duplicate detected (sim={sim:.2f}):")
                    print(f"Q{i}: {mcq_list[i]['question']}")
                    print(f"Q{j}: {mcq_list[j]['question']}\n")

    return mcq_list
