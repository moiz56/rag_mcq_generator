import os
import json
import ast
from typing import List, Tuple, Optional

from dotenv import load_dotenv
from pydantic import ValidationError, BaseModel

from google import genai
from google.genai import types

from model.prompt import create_gemini_prompt
from mcq_schema.schema import MCQ

load_dotenv()

class MCQResponse(BaseModel):
    mcqs: List[MCQ]


def _get_api_key() -> Optional[str]:
    return os.getenv("GOOGLE_API_KEY")

# Make sure you have the MCQ class and create_gemini_prompt function defined
# from .your_utils import create_gemini_prompt, MCQ

def generate_valid_mcqs(chunks, query,difficulty ,model_name="gemini-2.5-flash", max_tokens=8192):
    """
    Generates valid MCQs using Gemini, parses them into MCQ objects using Pydantic.

    Returns:
        Tuple[str, List[MCQ]]: (raw model output, list of MCQ objects)
    """
    api_key = _get_api_key()
    client = genai.Client(api_key = api_key)

    prompt = create_gemini_prompt(chunks,query,difficulty)
    sys_instruction = (
        "You are an expert teacher. Create valid MCQs based on the provided text. "
        "Return a list of dictionaries with the keys: "
        "question, A, B, C, D, correct, citation, explanation."
        "The number of MCQs to generate will be given in the prompt. "
    )

    for attempt in range(3):
        print(f"--- Attempt {attempt + 1} ---")
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=sys_instruction,
                    temperature=0.2,
                    max_output_tokens=max_tokens,
                    response_mime_type="application/json"
                )
            )

            raw = response.text.strip()

            # Use ast.literal_eval to safely parse Python-style list/dict
            try:
                mcq_list = ast.literal_eval(raw)
            except Exception as parse_err:
                print(f"Failed to parse model output: {parse_err}")
                continue

            # Convert to MCQ objects using Pydantic
            mcq_objects = []
            for item in mcq_list:
                mcq_data = {
                    "question": item.get("question", ""),
                    "A": item.get("A", ""),
                    "B": item.get("B", ""),
                    "C": item.get("C", ""),
                    "D": item.get("D", ""),
                    "correct": item.get("correct", ""),
                    "citation": item.get("citation", ""),
                    "explanation": item.get("reasoning", ""), # map reasoning -> explanation
                    "isLatex": item.get("isLatex","")
                }
                try:
                    mcq = MCQ(**mcq_data)
                    mcq_objects.append(mcq)
                except ValidationError as ve:
                    print(f"Validation error for item: {item}")
                    print(ve)
                    continue

            return raw, mcq_objects

        except Exception as e:
            print(f"Gemini API error: {e}")
            continue

    raise ValueError("Failed to generate valid MCQs after 3 attempts.")
