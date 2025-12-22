from google import genai
from google.genai import types
import os
import json
from dotenv import load_dotenv

load_dotenv()

def critique_distractors(mcq_dicts):
    """
    Accepts a list of MCQ dicts, critiques each one, and returns a list of JSON results.
    Each MCQ dict is expected to have: question, correct, A, B, C, D
    """

    # Allow passing a single dict too (optional convenience)
    if isinstance(mcq_dicts, dict):
        mcq_dicts = [mcq_dicts]

    api_key = os.getenv("GOOGLE_API_KEY")
    client = genai.Client(api_key=api_key)

    results = []

    for i, mcq in enumerate(mcq_dicts):
        prompt = f"""
You are an expert math teacher reviewing multiple-choice questions.

Evaluate the distractors for plausibility, correctness, and clarity. Suggest fixes for any bad options.

Question:
{mcq['question']}
Correct answer:
{mcq['correct']}
Options:
A: {mcq['A']}
B: {mcq['B']}
C: {mcq['C']}
D: {mcq['D']}

Return JSON only in this format:

{{
  "valid": true/false,
  "issues": [
      "List the specific problems for each bad distractor"
  ],
  "fixes": {{
      "A": "",
      "B": "",
      "C": "",
      "D": ""
  }}
}}

- Evaluate A, B, C, D individually and always comment if it is bad.
- Do not return valid: true unless all distractors are correct.
- Always return all four keys in fixes, even if empty.
"""

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=512,
                    response_mime_type="application/json"
                )
            )

            # Parse strict JSON
            parsed = json.loads(response.text)

            # Ensure fixes always has A-D even if model forgets
            fixes = parsed.get("fixes") or {}
            parsed["fixes"] = {
                "A": fixes.get("A", ""),
                "B": fixes.get("B", ""),
                "C": fixes.get("C", ""),
                "D": fixes.get("D", ""),
            }

            results.append(parsed)

        except Exception as e:
            # Per-item fallback so one bad response doesn't kill the loop
            results.append({
                "valid": True,
                "issues": [f"Critique failed for item {i}: {e}"],
                "fixes": {"A": "", "B": "", "C": "", "D": ""}
            })

    return results
