
def format_chunk_content(chunks):
    """
    Converts retrieved chunks into clean, readable text with proper
    chapter/section/subsection metadata for citation-friendly MCQ generation.
    """

    content_blocks = []

    for c in chunks:
        chapter = c.get("chapter_id", "")
        section = c.get("section_id", "")
        subsection = c.get("subsection_id", "")
        name = (
            c.get("subsection_name")
            or c.get("section_name")
            or c.get("chapter_name")
            or "Untitled Section"
        )
        text = c.get("text", "").strip()

        citation = f"(Chapter {chapter}, Section {section}, Subsection {subsection})"

        block = f"""{name} {citation}:
{text}"""

        content_blocks.append(block)

    return "\n\n".join(content_blocks)


def create_gemini_prompt(chunks, query, difficulty):
    """
    Creates a detailed MCQ generation prompt for Gemini API
    enforcing strict JSON output and mathematically relevant questions.
    """
    content = format_chunk_content(chunks)

    prompt = f"""
You are an expert Mathematics Exam Setter for HSSC Pre-Engineering (Class 11).
Your task is to generate **mathematical problems** based on the provided content.

**TASK:**
Generate EXACTLY the number of MCQs requested in the query.
Query Context: {query}
Target Difficulty: {difficulty}

=====================================================
**CRITICAL RULES (READ CAREFULLY)**

1. **NO METADATA QUESTIONS:** 
   - NEVER ask questions about the document structure, chapter numbers, section titles, or citations. 
   - BAD: "Which chapter discusses Trigonometry?" or "What is the title of Section 10.1?"
   - GOOD: "What is the value of sin(60)?" or "Solve the equation..."

2. **INTERPRETATION OF CONTENT:**
   - The provided content may contain syllabus outlines or headers. Use these headers to identify the *topic*, then generate a **mathematical problem** relevant to that topic.
   - If the content says "Topic: Quadratic Equations", do NOT ask "Is Quadratic Equations in the text?". Instead, ask: "If alpha and beta are roots of x^2 - x + 1 = 0, find..."

3. **DIFFICULTY CALIBRATION ({difficulty}):**
   - **Easy:** Direct application of formulas, definitions, or basic calculation.
   - **Medium:** Multi-step problems, conceptual understanding, simplifying expressions.
   - **Hard:** Complex synthesis, application problems, linking two concepts together.

4. **LATEX HANDLING:**
   - The context contains raw LaTeX. Interpret it correctly.
   - Dont use LATEX to return equations return in such a format a browesr can render it

=====================================================
**OUTPUT FORMAT: STRICT JSON ARRAY**

Produce ONLY a JSON array of objects. No markdown formatting (```json), no preamble.

Each object MUST use this exact schema:
{{
  "question": "<The mathematical problem text>",
  "A": "<Option A>",
  "B": "<Option B>",
  "C": "<Option C>",
  "D": "<Option D>",
  "correct": "A", 
  "citation": "(Chapter X, Section Y) - strictly from metadata provided",
  "reasoning": "<Mathematical step-by-step solution>",
  "isLatex": "True" 
}}

**DISTRACTOR GUIDELINES:**
- Distractors must be mathematically plausible (common calculation errors).
- Do NOT use "None of the above" or "All of the above".
- Options must be similar in length and formatting.

=====================================================
**SOURCE CONTENT:**

{content}

=====================================================
Generate the JSON array now.
"""
    return prompt
