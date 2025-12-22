import json
from model.generate_mcqs import generate_valid_mcqs

def build_dummy_chunks():
    """
    Minimal chunk objects that resemble what your pipeline produces.
    Add/remove fields as your prompt expects.
    """
    return [
        {
            "chunk_index": 39,
            "chapter_id": "3",
            "chapter_name": "Quadratic Functions",
            "section_id": "3.1",
            "section_name": "Quadratic Function",
            "subsection_id": "",
            "subsection_name": "",
            "text": (
                "A quadratic function has the form f(x)=ax^2+bx+c where a≠0. "
                "Its graph is a parabola. If a>0 it opens upward; if a<0 it opens downward. "
                "The vertex gives the maximum or minimum value."
            ),
        },
        {
            "chunk_index": 40,
            "chapter_id": "3",
            "chapter_name": "Quadratic Functions",
            "section_id": "3.1",
            "section_name": "Quadratic Function",
            "subsection_id": "3.1.1",
            "subsection_name": "Analyzing by Sketching",
            "text": (
                "To sketch a parabola, find the vertex and axis of symmetry. "
                "You can complete the square or use x = -b/(2a). "
                "Intercepts can be found by setting f(x)=0 for x-intercepts and x=0 for y-intercept."
            ),
        },
    ]


def main():
    # Dummy inputs
    chunks = build_dummy_chunks()
    query = "Make MCQs about section 3.1 quadratic functions focusing on vertex and axis of symmetry."
    difficulty = "medium"  # "easy" | "medium" | "hard"

    # Call your Gemini MCQ generator
    raw_json, mcq_objects = generate_valid_mcqs(
        chunks=chunks,
        query=query,
        difficulty=difficulty,
        model_name="gemini-2.5-flash",
        max_tokens=4096,
        attempts=3,
    )

    print("\n=== RAW MODEL JSON ===")
    # print(raw_json)

    print("\n=== PARSED MCQs (Pydantic objects) ===")
    for i, mcq in enumerate(mcq_objects, start=1):
        # Works in Pydantic v2; if you're on v1 use mcq.dict()
        data = mcq.model_dump() if hasattr(mcq, "model_dump") else mcq.dict()
        print(f"\nMCQ {i}")
        print(json.dumps(data, indent=2, ensure_ascii=False))
