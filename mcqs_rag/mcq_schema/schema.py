from pydantic import BaseModel, Field

class MCQ(BaseModel):
    question: str
    A: str
    B: str
    C: str
    D: str
    correct: str  # e.g. "A", "B", etc.
    citation: str
    explanation: str
    isLatex: bool
