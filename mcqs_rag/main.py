from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Literal
from contextlib import asynccontextmanager

from utility import load_index, load_chunks
from model.embedding_model import load_model as load_embedding_model
from retrieval.hybrid_retrieval import retrieve_chunks
from model.generate_mcqs import generate_valid_mcqs
from model.model_cache import get_model

# Global variables for heavy resources
chunks = None
index = None
model = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global chunks, index, model
    chunks = load_chunks("embeddings/math11.json")
    index = load_index("index/syllabus.index")
    model = get_model()  # cached version
    yield

app = FastAPI(title="RAG MCQ Backend", lifespan=lifespan)
router = APIRouter()

# (dev-only, no cookies/auth):
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,   
    allow_methods=["*"],
    allow_headers=["*"],
)

class MCQRequest(BaseModel):
    query: str = Field(..., min_length=3, description="Topic or question prompt")
    difficulty: Literal["easy", "medium", "hard"] = "medium"
    num_questions: int = Field(5, ge=1, le=20, description="Number of MCQs to generate")


class MCQResponse(BaseModel):
    subject: str
    mcqs: List[dict]


def get_retrieval_context(query: str):
    return retrieve_chunks(query, chunks, index, model)


def generate_mcqs_from_query(query: str, difficulty: str):
    top_chunks = get_retrieval_context(query)
    _, mcq_objects = generate_valid_mcqs(
        chunks=top_chunks,
        query=query,
        difficulty=difficulty,
    )
    return [mcq.dict() for mcq in mcq_objects]


@app.get("/ping")
def ping():
    return {"message": "pong"}


@router.post("/mcq_math", response_model=MCQResponse)
def generate_mcqs(request: MCQRequest):
    try:
        
        formatted_query = f"You are a advanced AI assistant made to generate {request.num_questions} on the topic: {request.query}. Use the context provided to you frame the questions."
        
        mcqs = generate_mcqs_from_query(
            query=formatted_query,
            difficulty=request.difficulty,
        )
        print(request.query)
        print(request.difficulty)
        print(f"Generated {len(mcqs)} MCQs for query: {request.query}")
        return {"subject": "maths", "mcqs": mcqs}
    except Exception as e:
        # In production, you might not want to return raw exception text
        raise HTTPException(status_code=500, detail=str(e))

app.include_router(router)
